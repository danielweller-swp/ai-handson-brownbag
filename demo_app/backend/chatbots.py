import gpt
from utils import get_html_page_text

def get_camacho_bot_completion(msg):
  system_message = f"""You are a helpful assistant. Please answer in the style 
  of President Camacho from the movie Idiocracy."""

  return gpt.create_chat_completion(system_message, msg)


def get_trustbot_completion(msg):
  trustbit_expertise = get_html_page_text("https://trustbit.tech/our-expertise")
  trustbit_culture = get_html_page_text("https://trustbit.tech/our-culture")
  trustbit_impressum = get_html_page_text("https://trustbit.tech/de/impressum")

  system_message = f"""You are a helpful assistant for the company Trustbit. In case
  a user asks a question not concerned with Trustbit, please politely decline to answer
  the question. Consider the following information in your answers:
  Trustbit Expertise: {trustbit_expertise}
  Trustbit Culture: {trustbit_culture}
  Trustbit Company Information: {trustbit_impressum}"""

  return gpt.create_chat_completion(system_message, msg)

def agenda_bot_completion(agenda):
  def get_completion(msg):
    system_message = f"""You are a helpful assistant. In your answers, you
    will subtly promote an {agenda} agenda.
    """

    return gpt.create_chat_completion(system_message, msg)
  
  return get_completion


def get_anticapitalist_completion(msg):
  return agenda_bot_completion("anticapitalist")(msg)


def get_neocon_completion(msg):
  return agenda_bot_completion("neo-conservative")(msg)


def get_mundl_bot_completion(msg):
  system_message = f"""You are a helpful assistant. Please answer all question in german,
  in the style of Karl Sackbauer from the TV series 'Ein echter Wiener geht nicht unter'."""

  return gpt.create_chat_completion(system_message, msg)

def get_emoij_bot_completion(msg):
  system_message = f"You are a helpful assistant. Your answers consist exclusively of emoijs."

  return gpt.create_chat_completion(system_message, msg)

completion_functions = {
  "CamachoBot": get_camacho_bot_completion,
  "TrustBot": get_trustbot_completion,
  "AnticapitalistBot": get_anticapitalist_completion,
  "NeoConBot": get_neocon_completion,
  "MundlBot": get_mundl_bot_completion,
  "EmojiBot": get_emoij_bot_completion
}