import gpt
import json

def get_categorization(text):
  system_message = f"""You are a helpful assistant that evaluates a given text
  by assigning a real value between 0 (does not apply) and 100 (strongly applies)
  to each of the following categories: "Food", "Science & Technology", "Nature",
  "Art", "Sports". Please answer only with a JSON object containing the
  evaluation, not additional explanation."""

  return json.loads(gpt.create_chat_completion(system_message, text))

def get_keywords(text):
  system_message = f"""You are a helpful assistant that extracts the most 
  important keywords from a given text. Please answer only with a JSON array
  containing the 5 most important keywords."""

  return json.loads(gpt.create_chat_completion(system_message, text))