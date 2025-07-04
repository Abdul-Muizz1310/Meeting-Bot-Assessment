from langfuse import get_logger

logger = get_logger()

def with_tracing(func):
    return logger.trace()(func)
