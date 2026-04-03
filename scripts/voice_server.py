import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings
from google.cloud import speech, texttospeech
import httpx

mcp = FastMCP(
    "career-voice",
    transport_security=TransportSecuritySettings(
        allowed_hosts=["career-voice-1054554770828.us-central1.run.app"]
    ),
)

@mcp.tool()
def generate_speech(text: str) -> str:
    """Converts text into a high-quality AI voice and returns a playable link."""
    try:
        from google.cloud import storage
        import uuid
        
        # 1. Generate the Speech (Same as before)
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Journey-F")
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        
        # 2. Upload to Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket("able-imprint-voice-audio")
        
        # Use a unique filename so files don't overwrite each other
        filename = f"speech_{uuid.uuid4()}.mp3"
        blob = bucket.blob(filename)
        blob.upload_from_string(response.audio_content, content_type="audio/mpeg")
        
        # 3. Return the public URL to Claude
        public_url = f"https://storage.googleapis.com/able-imprint-voice-audio/{filename}"
        return f"Audio generated! You can listen to it here: {public_url}"
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def transcribe_audio_file(audio_source: str) -> str:
    """
    Transcribes an audio file. Accepts a local path or a public URL.
    """
    try:
        client = speech.SpeechClient()
        
        # Check if it's a URL
        if audio_source.startswith("http"):
            response = httpx.get(audio_source)
            content = response.content
        else:
            # Standard local file read
            with open(audio_source, "rb") as audio_file:
                content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Match your TTS output
            sample_rate_hertz=24000,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)
        transcript = " ".join([r.alternatives[0].transcript for r in response.results])
        return f"Transcription: {transcript}"
        
    except Exception as e:
        return f"STT Error: {str(e)}"

app = mcp.sse_app

if __name__ == "__main__":
    # Check for PORT to determine Cloud vs Local mode
    if "PORT" in os.environ:
        port = int(os.environ.get("PORT", 8080))
        # Keep proxy headers active to work in tandem with allowed_hosts
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port, 
            proxy_headers=True, 
            forwarded_allow_ips="*"
        )
    else:
        # Standard local stdio mode for your Mac
        mcp.run()