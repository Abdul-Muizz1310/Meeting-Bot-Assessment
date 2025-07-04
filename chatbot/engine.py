from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chatbot.utils.vector_store import get_vectorstore_from_transcript
from chatbot.utils.intent_router import get_router_chain
from chatbot.utils.session_memory import get_memory_for_session

SUMMARIZATION_PROMPT_PATH = "chatbot/prompts/summarization.txt"
FOLLOWUP_PROMPT_PATH = "chatbot/prompts/followup.txt"


def respond(user_prompt, session_data):
    transcript = session_data.get("transcript", "")
    user_id = session_data.get("user_id", "anonymous")

    llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini",openai_api_key="-proj-zpClYfXcNMISkwndC5VCpVouycig2p28GUrms48exJLQ8QY12LhonSt7bgiOJ9ldMcfRk6ORk3T3BlbkFJlvEpD6nLAiUDYmaqv4giCTA2I4RL_ioASuGI4qu_XF-mYJ7W6-0bYqQyf0POdLYkjcFcjCmqIA")
    memory = get_memory_for_session(user_id)
    intent = get_router_chain(user_prompt)


    if intent == "summarize":
        with open(SUMMARIZATION_PROMPT_PATH) as f:
            template = PromptTemplate.from_template(f.read())
        return LLMChain(llm=llm, prompt=template).run(transcript)

    elif intent == "qa":
        vectorstore = get_vectorstore_from_transcript(transcript)
        retriever = vectorstore.as_retriever()
        context = retriever.get_relevant_documents(user_prompt)
        context_str = "\n\n".join([doc.page_content for doc in context])
        with open(FOLLOWUP_PROMPT_PATH) as f:
            template = PromptTemplate.from_template(f.read())
        return LLMChain(llm=llm, prompt=template).run({"context": context_str, "question": user_prompt})

    else:
        return "I'm here to help with summaries and follow-ups. Please ask a relevant question."
