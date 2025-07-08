import time
import random
from functools import wraps
from typing import Callable, Any, Tuple, Type

class RetryHandler:
    """Handles retry logic with exponential backoff and jitter"""
    
    def __init__(self, max_retries=3, base_delay=1, max_delay=60, backoff_factor=2, jitter=True):
        """
        Initialize retry handler
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            backoff_factor: Multiplier for exponential backoff
            jitter: Add random jitter to prevent thundering herd
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number"""
        delay = min(self.base_delay * (self.backoff_factor ** attempt), self.max_delay)
        
        if self.jitter:
            # Add random jitter (±25%)
            jitter_range = delay * 0.25
            delay += random.uniform(-jitter_range, jitter_range)
        
        return max(0, delay)
    
    def retry(self, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
        """
        Decorator for adding retry logic to functions
        
        Args:
            exceptions: Tuple of exception types to retry on
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                last_exception = None
                
                for attempt in range(self.max_retries + 1):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 0:
                            print(f"Function {func.__name__} succeeded on attempt {attempt + 1}")
                        return result
                    
                    except exceptions as e:
                        last_exception = e
                        
                        if attempt == self.max_retries:
                            print(f"Function {func.__name__} failed after {self.max_retries + 1} attempts")
                            break
                        
                        delay = self.calculate_delay(attempt)
                        print(f"Function {func.__name__} failed on attempt {attempt + 1}, retrying in {delay:.2f}s: {str(e)}")
                        time.sleep(delay)
                
                # If we get here, all retries failed
                raise last_exception
            
            return wrapper
        return decorator

# Default retry handler instances
default_retry = RetryHandler(max_retries=3, base_delay=1)
api_retry = RetryHandler(max_retries=5, base_delay=2, max_delay=30)
network_retry = RetryHandler(max_retries=2, base_delay=0.5, max_delay=10)

def with_retry(func: Callable, max_retries=3, exceptions=(Exception,)) -> Callable:
    """
    Simple retry wrapper function
    
    Args:
        func: Function to wrap with retry logic
        max_retries: Maximum number of retries
        exceptions: Exception types to retry on
        
    Returns:
        Function with retry logic applied
    """
    retry_handler = RetryHandler(max_retries=max_retries)
    return retry_handler.retry(exceptions=exceptions)(func)

def safe_execute(func: Callable, fallback_value=None, log_errors=True) -> Any:
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        fallback_value: Value to return if function fails
        log_errors: Whether to log errors
        
    Returns:
        Function result or fallback_value
    """
    try:
        return func()
    except Exception as e:
        if log_errors:
            print(f"Error in {func.__name__}: {str(e)}")
        return fallback_value

def batch_execute(functions: list, max_failures=None, continue_on_error=True) -> list:
    """
    Execute multiple functions with error handling
    
    Args:
        functions: List of functions to execute
        max_failures: Maximum allowed failures before stopping
        continue_on_error: Whether to continue if a function fails
        
    Returns:
        List of results (None for failed functions)
    """
    results = []
    failures = 0
    max_failures = max_failures or len(functions)
    
    for i, func in enumerate(functions):
        try:
            result = func()
            results.append(result)
        except Exception as e:
            failures += 1
            results.append(None)
            print(f"Function {i} failed: {str(e)}")
            
            if failures >= max_failures and not continue_on_error:
                print(f"Stopping batch execution after {failures} failures")
                break
    
    return results

# Rate limiting utilities
class RateLimiter:
    """Simple rate limiter using token bucket algorithm"""
    
    def __init__(self, calls_per_second=1):
        """
        Initialize rate limiter
        
        Args:
            calls_per_second: Maximum calls allowed per second
        """
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_called = 0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limit"""
        now = time.time()
        time_since_last = now - self.last_called
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_called = time.time()
    
    def rate_limited(self, func: Callable) -> Callable:
        """Decorator to add rate limiting to a function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper

# Global rate limiters
api_rate_limiter = RateLimiter(calls_per_second=2)  # 2 calls per second
web_rate_limiter = RateLimiter(calls_per_second=0.5)  # 1 call every 2 seconds