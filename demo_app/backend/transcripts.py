import json
from pydantic import BaseModel
import ffmpeg
from fastapi.responses import FileResponse
import tempfile
from gpt import create_chat_completion

# GCP SPEECH-TO-TEXT
# # Upload MP3 to GCP bucket
#
# gsutil cp resources/audio-files/audio-files_msw_airton.mp3 gs://ai-brownbag-transcription
#
# # Transcribe the MP3
#
# gcloud beta ml speech recognize-long-running \
# gs://ai-brownbag-transcription/audio-files_msw_airton.mp3 \
# --encoding=mp3 \
# --sample-rate=44100 \
# --output-uri=gs://ai-brownbag-transcription/audio-files_msw_airton-transcript.json \
# --include-word-time-offsets \
# --language-code en-US


AUDIO_FILE="resources/audio-files/audio-files_msw_airton.mp3"
TRANSCRIPT_FILE="resources/transcripts/audio-files_msw_airton-transcript.json"

def transcript_json():
    with open(TRANSCRIPT_FILE, 'r') as f:
        return json.loads(f.read())

def transcript_words():
    json = transcript_json()
    return [
        w
        for result in json["results"]
        for w in result["alternatives"][0]["words"]
    ]

class Word(BaseModel):
    word: str
    startTime: str
    endTime: str

def temp_file_name():
    tmp_dir = tempfile._get_default_tempdir()
    return tmp_dir + "/" + next(tempfile._get_candidate_names())


def excerpt(words: list[Word]):
    start_time = float(words[0].startTime[:-1])
    end_time = float(words[-1].endTime[:-1])

    print(f"Generating excerpt from {start_time}s to {end_time}s")

    tmp_file = f"{temp_file_name()}.mp3"

    (
        ffmpeg
        .input(AUDIO_FILE, ss=start_time, to=end_time)
        .output(tmp_file)
        .run()
    )

    return FileResponse(tmp_file, media_type="audio/mpeg")

def transcript_text():
    words = transcript_words()
    return ' '.join([w["word"] for w in words])

def summary():
    text = transcript_text()
    return create_chat_completion("Please summarize the transcript of a podcast given by the user", text)