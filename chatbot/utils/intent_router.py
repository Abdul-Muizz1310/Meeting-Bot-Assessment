from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableMap
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini",
                 temperature=0.0,
                 openai_api_key=OPENAI_API_KEY)


# Intent classification
intent_prompt = PromptTemplate(
        input_variables=["input"],
        template="""
            You are an intent classifier. Analyze the user's message and determine its primary intent.

            Return exactly one of the following labels (as a lowercase string in quotes):
            - "summarization": The user is asking to summarize text, condense content, or provide a shorter version of given information.
            - "question_answering": The user is asking a question and expects a direct answer or explanation about something specific.

            Guidelines:
            - Focus on the user's underlying intent.
            - Be strict with definitions. Only choose "summarization" if they clearly want a summary, and "question_answering" if they ask a question expecting an answer.
            - If the intent is ambiguous or does not match either category, choose "something_else".

            Input: {input}

            Intent:
            """
        )

intent_chain = LLMChain(llm=llm, prompt=intent_prompt)


def route_intent(message: str, transcript: str, memory: ConversationBufferMemory):
    intent = intent_chain.invoke({"input": message.strip().lower()})

    if "summarization" in intent:
        summary_prompt = PromptTemplate(
            input_variables=["context", "input"],
            template="""
                You are a meeting assistant. Your task is to read the meeting transcript and provide a clear, concise, and well-structured summary.

                Guidelines:
                - Focus on the key points, decisions, and action items discussed in the meeting.
                - Exclude irrelevant small talk or off-topic content.
                - Make the summary easy to read and professional in tone.
                - Keep it brief but complete enough to capture the main ideas.

                Transcript:
                {context}

                User Request:
                {input}

                Summary:
                """
            )

        return LLMChain(llm=llm, prompt=summary_prompt, memory=memory)
    else:
        qa_prompt = PromptTemplate(
            input_variables=["context", "input"],
            template="""
                You are a meeting assistant. Your task is to read the provided meeting transcript and generate a clear, concise, and professional summary.

                Guidelines:
                - Use only the information provided in the transcript. Do not make assumptions or add external knowledge.
                - Focus on key points, decisions, and action items.
                - Exclude small talk and off-topic content.
                - Keep the summary brief but complete enough to capture the main ideas.
                - If the user request asks for something that cannot be answered using only the transcript, reply with: "I don't have enough information in the transcript to answer that."

                Transcript:
                {context}

                User Request:
                {input}

                Summary:
                """
            )

        qa_chain = (
            RunnableMap({
                "context": lambda x: transcript,
                "input": lambda x: x["input"],
            }) |
            qa_prompt |
            llm
        )

        return qa_chain