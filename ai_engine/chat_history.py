# Short-term conversation memory

MAX_HISTORY = 10

chat_history = []


def add_message(role, text): # here role will be either user and ai

    global chat_history

    chat_history.append(f"{role}: {text}")

    # keep last N messages
    chat_history = chat_history[-MAX_HISTORY:] # means last 10 messages


def get_history():
    if not chat_history:
        return ""

    return "\n".join(chat_history)


def clear_history():

    global chat_history

    chat_history = []