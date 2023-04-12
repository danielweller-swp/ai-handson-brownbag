
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chatbots
import text
from employee_db_bot import get_employee_db_completion
from transcripts import transcript_words, excerpt, Word, summary, transcript_text
from dalle import create_image
from document_db_bot import get_document_db_bot_completion

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/bot/DocumentDbBot/completion")
def get_documentdbbot_completion(query: str):
   return get_document_db_bot_completion(query)
   

@app.get("/bot/EmployeeBot/completion")
def get_employeedb_completion(query: str):
   return get_employee_db_completion(query)

@app.get("/bot/{name}/completion")
def get_completion(name: str, query: str):
    completion_function = chatbots.completion_functions[name]
    return completion_function(query)

class TextAnalysisRequest(BaseModel):
   text: str

@app.post("/text/analysis")
def post_text_analysis(req: TextAnalysisRequest):
    categorization = text.get_categorization(req.text)
    keywords = text.get_keywords(req.text)

    return {
       "categorization": categorization,
       "keywords": keywords
    }

@app.get("/transcripts/words")
def get_words():
   return transcript_words()

class ExcerptRequest(BaseModel):
    words: list[Word]

@app.post("/transcripts/excerpt")
def post_excerpt(req: ExcerptRequest):
  return excerpt(req.words)

@app.get("/transcripts/summary")
def get_summary():
   return summary()

@app.get("/transcripts/image/{style}")
def get_images(style: str):
   return create_image(transcript_text(), style)