conversation_buffer = []

def add_to_short_term(text):
    conversation_buffer.append(text)

def get_short_term():
    return "\n".join(conversation_buffer[-5:])