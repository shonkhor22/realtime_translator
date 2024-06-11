# Real-Time Audio Processing System

This repository contains the code for a real-time audio processing system that uses OpenAI's Whisper for transcription, OpenAI's GPT-3.5 for translation, and Google Cloud Text-to-Speech for synthesizing speech. The system captures audio inputs, transcribes them to text, translates the text, and then synthesizes the translated text into speech.

## Files
- `server.py`: The main server script that handles WebSocket connections, processes audio, transcribes, translates, and synthesizes speech.
- `index.html`: The client-side HTML file to capture audio and communicate with the WebSocket server.

## Prerequisites
- Python 3.7 or higher
- OpenAI API key
- Google Cloud credentials file for Text-to-Speech

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository/real-time-audio-processing.git
   cd real-time-audio-processing

Install Dependencies:**

```bash
pip install -r requirements.txt ```
```
2. **Set Environment Variables:**
```bash
export OPENAI_API_KEY='your-openai-api-key'
export GOOGLE_APPLICATION_CREDENTIALS='path-to-your-google-cloud-credentials-file.json'
```

3. **Run the Server:**

```bash
python server.py
```

**Deployment Instructions**

To run the deployed system on the cloud, follow these steps:

1. **Go to https://34.151.127.60:8765/ in your browser.** You will likely see a security warning.
In the security warning page, look for an option to proceed or add an exception. 
2. **Follow the prompts to add a security exception for your self-signed certificate.**
3. **Load your client page at https://storage.googleapis.com/del20240608nlp/index.html** and check if the WebSocket connection works.

**Usage**

Open the client page in your browser.
Click the button to start recording audio.
The audio will be sent to the WebSocket server for processing.
Transcriptions, translations, and synthesized speech will be displayed and played back on the client page.
