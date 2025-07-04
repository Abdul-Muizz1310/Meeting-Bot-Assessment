import os
from dotenv import load_dotenv
from langfuse import observe, get_client
import functools

# Load environment variables
load_dotenv()

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")

langfuse_client = get_client(public_key=LANGFUSE_PUBLIC_KEY)


def with_tracing(func):
    @observe(name="chatbot_trace")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper