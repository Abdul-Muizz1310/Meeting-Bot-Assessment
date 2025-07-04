from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0,openai_api_key="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")

INTENT_PROMPT = PromptTemplate.from_template("""
You are an intent classifier for a meeting assistant. Classify the user's message into one of the following intents:

- summarize: If the user asks to summarize a transcript or topic.
- qa: If the user is asking a follow-up question based on a transcript.
- fallback: If the user's request doesn't match either.

Message: "{message}"
Respond with only one word: summarize, qa, or fallback.
""")

intent_chain = LLMChain(llm=llm, prompt=INTENT_PROMPT)

def get_router_chain(message: str) -> str:
    intent = intent_chain.run(message).strip().lower()
    return intent if intent in ["summarize", "qa"] else "fallback"
