import openai
import os

def truncate_message(msg):
  maxChars = 100
  if len(msg) > maxChars:
    return f"{msg[:maxChars]}..."
  else:
    return msg

def create_chat_completion(system_message, user_message, retries = 0):
  print(f"System Message: {truncate_message(system_message)}")
  print(f"User Message: {user_message}")
  try:
    # https://platform.openai.com/docs/api-reference/chat/create
    response = openai.ChatCompletion.create(
      api_type=os.getenv("AZURE_OPENAI_API_TYPE"),
      api_key=os.getenv("AZURE_OPENAI_API_KEY"),
      api_base=os.getenv("AZURE_OPENAI_API_BASE"),
      api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
      deployment_id="turbo-0301",
      messages= [
        {"role": "system", "content": system_message },
        {"role": "user", "content": user_message }
      ]
    )
    print("ChatGPT response:")
    print(response)
    msg = response["choices"][0]["message"]["content"]
    return msg    
  except:
    if retries < 5:
      return create_chat_completion(system_message, user_message, retries+1)
    else:
      return None