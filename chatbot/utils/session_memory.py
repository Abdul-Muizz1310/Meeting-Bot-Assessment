from langchain.memory import ConversationBufferMemory
session_memories = {}

def get_memory(session_id):
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferMemory(return_messages=True)
    return session_memories[session_id]
