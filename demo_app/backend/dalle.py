import openai
import os

def create_image(prompt, style):
  truncated_prompt = (f"{style}, {prompt}")[:1000]
  # https://platform.openai.com/docs/api-reference/images/create
  response = openai.Image.create(
    api_key=os.getenv("OPENAI_OPENAI_API_KEY"),    
    prompt=truncated_prompt,
    n=1,
    size="256x256"
  )
  return response["data"][0]["url"]
