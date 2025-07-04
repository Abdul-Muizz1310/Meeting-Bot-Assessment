from chatbot.utils.langfuse_tracer import with_tracing
from chatbot.utils.intent_router import route_intent

from langchain.schema import AIMessage

@with_tracing
def respond(message, session_data):
    from server import sessions

    transcript = session_data.get("transcript", "")
    chat_history = session_data.get("chat_history", [])

    from langchain.memory import ConversationBufferMemory
    memory = ConversationBufferMemory(return_messages=True)
    memory.chat_memory.messages = chat_history

    chain = route_intent(message, transcript, memory)

    if hasattr(chain, "invoke"):
        result = chain.invoke({"input": message})
    else:
        result = chain.run(message)

    if isinstance(result, AIMessage):
        result = result.content

    # Update session memory
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": result})

    return result
