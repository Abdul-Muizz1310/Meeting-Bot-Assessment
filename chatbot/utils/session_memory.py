from langchain.memory import ConversationBufferMemory

session_memories = {}

def get_memory_for_session(user_id):
    if user_id not in session_memories:
        session_memories[user_id] = ConversationBufferMemory(return_messages=True)
    return session_memories[user_id]
