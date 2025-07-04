from langfuse import observe, get_client
import functools

langfuse_client = get_client(public_key="pk-lf-68512509-5f31-489b-b547-fe679a736e7f")


def with_tracing(func):
    @observe(name="chatbot_trace")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper