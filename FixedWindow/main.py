# Python implementation for Fixed Window Algorithm

import time

class FixedWindowCounter:
    def __init__(self, window_size, max_requests):
        self.window_size = window_size # size of the window in seconds
        self.max_requests = max_requests # maximum number of requests in a window
        self.current_window = time.time() // window_size
        self.request_count = 0

    def add_request(self):
        """
        Increments the counter. If the limit is reached, it raises an exception.
        """

        self.reset_if_needed()

        # check if we are still in the limit then add the request
        if self.request_count < self.max_requests:
            self.request_count += 1
            return True
        return False
    
    def reset_if_needed(self):
        """
        Resets the counter if the window has expired.
        """
        current_time = time.time()
        window = current_time // self.window_size

        # If we've moved to the new window reset the counter
        if window != self.current_window:
            self.current_window = window
            self.request_count = 0


if __name__ == "__main__":
    limiter = FixedWindowCounter(window_size=60, max_requests=5)  # 5 requests per minute

    for _ in range(10):
        print(limiter.add_request()) # Will print True for the first 5 requests, then False
        time.sleep(0.1)  # Wait a bit between requests

    time.sleep(60)  # Wait for the window to reset
    print(limiter.add_request()) # True