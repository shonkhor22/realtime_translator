import os
import asyncio
import websockets
from openai import OpenAI
from google.cloud import texttospeech
import io
import json
import ssl


# Initialize OpenAI and Google Cloud TTS clients
oai_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=oai_key)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gtt-del.json"
tts_client = texttospeech.TextToSpeechClient()

async def transcribe_audio(client, audio_buffer):
    audio_buffer.seek(0)
    file_tuple = ("audio.webm", audio_buffer, "audio/webm")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=file_tuple,
        response_format="text"
    )
    return transcription

async def translate_text(client, text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translation assistant. only return translataion."},
            {"role": "user", "content": f"Translate the following text to English: {text}"}
        ]
    )
    full_text = completion.choices[0].message.content
    parts = full_text.split('\n')
    translation_text = parts[1].strip() if len(parts) > 1 else parts[0].strip()
    return translation_text

async def synthesize_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

async def handler(websocket, path):
    try:
        chunk_count = 0  # Track the number of chunks received
        while True:
            message = await websocket.recv()
            
            
            # Create a BytesIO object for the received chunk
            audio_chunk = io.BytesIO(message)
            # Check if the audio chunk is a valid webm format
            audio_chunk.seek(0)
            if audio_chunk.read(4) != b'\x1A\x45\xDF\xA3':  # Check for EBML header
                print(f"Invalid webm format for chunk {chunk_count}")
                continue
            # Process the chunk
            transcription = await transcribe_audio(client, audio_chunk)
            if transcription.strip() and transcription!='Thank you. Bye.' and transcription!='Bye. Bye. Bye. Bye.':
                print(f"Transcription for chunk {chunk_count}: {transcription}")
                translation = await translate_text(client, transcription)
                if translation:
                    audio_response = await synthesize_speech(translation)
                    response_message = {
                        "transcription": transcription,
                        "translation": translation,
                        "audio_response": audio_response.hex()
                    }
                    await websocket.send(json.dumps(response_message))
                    print(f"Sent response for chunk {chunk_count}")
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"Error occurred: {e}")

async def main():
    
    port = 8765
    print(f"WebSocket server is starting on port {port} with SSL...")
   
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='/home/shonhor22/ssl/selfsigned.crt', keyfile='/home/shonhor22/ssl/selfsigned.key')
    async with websockets.serve(handler, "0.0.0.0", port, ssl=ssl_context):
    # async with websockets.serve(handler, "0.0.0.0", port):
        print(f"WebSocket server is listening on port {port} with SSL.")
        await asyncio.Future()  # run forever
    # async with websockets.serve(handler, "localhost", 8765):
    #     await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
