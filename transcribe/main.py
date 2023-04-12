from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

WHISPER_MODEL = "tiny"

def extract_audio(input_video_file, output_audio_file):
    import ffmpeg
    (
    ffmpeg
    .input(input_video_file)
    .output(output_audio_file)
    .run()
    )

def transcribe_with_api(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
      return openai.Audio.transcribe('whisper-1', audio_file)

def transcribe_locally(audio_file_path, initial_prompt = None):
    import whisper
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio=audio_file_path, initial_prompt=initial_prompt)
    return result["text"]


def main():
  INPUT_VIDEO_PATH='video.mp4'
  AUDIO_PATH='audio.mp3'
  TRANSCRIPT_PATH="transcript.txt"
  # INITIAL_PROMPT="Rinat and Aigiz give a talk about AI and machine learning, in particular ChatGPT."

  if not os.path.isfile(AUDIO_PATH):
    print("Extracting audio...")
    extract_audio(INPUT_VIDEO_PATH, AUDIO_PATH)
    print("Finished extracting audio.")

  if not os.path.isfile("transcript.txt"):
    print("Transcribing...")
    transcript = transcribe_locally(AUDIO_PATH)
    with open(TRANSCRIPT_PATH, "w") as transcript_file:
       transcript_file.writelines(transcript)
    print("Finished transcribing.")

main()