# Python implementation for Sliding Window Log Algorithm
# Single Machine with multiple threads

# Reference: https://medium.com/@saisandeepmopuri/system-design-rate-limiter-and-data-modelling-9304b0d18250

import time
import threading
from collections import deque

class RequestTimestamps:
    
    # lock is for concurrency control in a mutli-threaded environment
    # 100 req/min transaltes to requests = 100 and window_time_in_second = 60
    def __init__(self, requests, window_time_in_second):
        self.timestamps = deque()
        self.requests = requests
        self.window_time_in_second = window_time_in_second
        self.lock = threading.Lock()

    # eviction of timestamps older than the window time
    def evict_older_timestamps(self, current_timestamps):
        while len(self.timestamps) != 0 and (current_timestamps - self.timestamps[0] > self.window_time_in_second):
            self.timestamps.popleft()
    

class SlidingWindowLogRateLimiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.rate_limiter_map = {}

    # Default rate limiter is 100 requests per minute
    # Add a new user to the rate limiter with a request rate
    def add_user(self, user_id, requests=100, window_time_in_second=60):
        # hold lock to add in the user-metadata map
        with self.lock:
            if user_id in self.rate_limiter_map:
                raise Exception("User already exists")
            self.rate_limiter_map[user_id] = RequestTimestamps(requests, window_time_in_second)

    # Remove a user from the rate limiter
    def remove_user(self, user_id):
        # hold lock to remove the user-metadata map
        with self.lock:
            if user_id not in self.rate_limiter_map:
                raise Exception("User does not exist")
            del self.rate_limiter_map[user_id]

    # give current time epoch in seconds
    def current_timestamp_in_sec(self):
        return int(round(time.time()))

    # check if the user is allowed to make a request
    def is_request_allowed(self, user_id):
        # check if user exists or not
        with self.lock:
            if user_id not in self.rate_limiter_map:
                raise Exception("User does not exist")
        
        user_timestamps = self.rate_limiter_map[user_id]
        with user_timestamps.lock:
            current_timestamps  = self.current_timestamp_in_sec()
            # remove all the existing older timestamps
            user_timestamps.evict_older_timestamps(current_timestamps)
            user_timestamps.timestamps.append(current_timestamps)

            # check if the user has exceeded the request limit
            if len(user_timestamps.timestamps) > user_timestamps.requests:
                return False
            return True


# Test the rate limiter
if __name__ == "__main__":
    rate_limiter = SlidingWindowLogRateLimiter()

    rate_limiter.add_user("user1", 100, 60)
    rate_limiter.add_user("user2", 200, 60)
    rate_limiter.add_user("user3", 300, 60)
    rate_limiter.add_user("user4", 400, 60)
    rate_limiter.add_user("user5", 500, 60)
    rate_limiter.add_user("user6", 600, 60)

    print(rate_limiter.is_request_allowed("user1"))
    print(rate_limiter.is_request_allowed("user2"))
    print(rate_limiter.is_request_allowed("user3"))

    rate_limiter.remove_user("user1")
    rate_limiter.remove_user("user2")
    rate_limiter.remove_user("user3")

    # print(rate_limiter.is_request_allowed("user3"))

    print(rate_limiter.is_request_allowed("user4"))
    print(rate_limiter.is_request_allowed("user5"))
