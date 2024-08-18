import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import openai
import constants
from elevenlabs import ElevenLabs

# Initialize the ElevenLabs client
client = ElevenLabs(api_key="2c354deb4fa84979ba691282f0c55517")

# Example of using the client
voices = client.get_voices()
print(voices)

class AI_Assistant:
    def __init__(self):
        # Replace with your API key
        aai.settings.api_key = "2c354deb4fa84979ba691282f0c55517"
        self.elevenlabs_api_key = "2c354deb4fa84979ba691282f0c55517"
        self.openai_api_key = "2c354deb4fa84979ba691282f0c55517"
        
        openai.api_key = self.openai_api_key
        
        self.transcriber = None
        
        self.full_transcript = [
            {"role": "system", "content": "You are a language model called llama 3, who is friendly to user and answers the questions given by user"}
        ]
        
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )

        self.transcriber.connect()

        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None
            
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(transcript.text, end="\r\n")
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occurred:", error)
        return

    def on_close(self):
        print("Closing Session")
        return

    def generate_ai_response(self, transcript):
        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\nuser: {transcript.text}", end="\r\n")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )
        ai_response = response.choices[0].message.content
        
        self.generate_audio(ai_response)
        self.start_transcription()

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAi: {text}")
        audio_stream = generate(
            api_key=self.elevenlabs_api_key,
            text=text,
            voice="Rachel",
            stream=True
        )
        stream(audio_stream)

# Creating an instance of the AI_Assistant class
ai_assistant = AI_Assistant()

# Generating audio for the greeting message
greeting = "Thank you for taking me as your assistant, what's your name?"
ai_assistant.generate_audio(greeting)

# Starting the transcription
ai_assistant.start_transcription()
