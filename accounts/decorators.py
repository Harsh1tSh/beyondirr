import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_request(record_success=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                print("Request is being processed")
                response = view_func(request, *args, **kwargs)
                print("Request processed successfully")
                return response
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                logger.error(f"Error occurred: {str(e)}")
                raise
        return _wrapped_view
    return decorator
