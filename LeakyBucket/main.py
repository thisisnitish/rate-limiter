# Python implementation for Leaky Bucket Algorrithm

import time
from collections import deque

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity  # maximum number of requests bucket can hold
        self.leak_rate = leak_rate # rate at which requests leaks (requests/second)
        self.last_leak_time = time.time()  # last time we leaked from the bucket
        self.bucket = deque()   # using queue to simulate the bucket

    def add_request(self, current_time):
        """Add a request to the bucket."""
        # current_time = time.time()

        # leak out the old request
        self.leak(current_time)

        # check if there is a capacity in the queue and add the new request
        if len(self.bucket) < self.capacity:
            self.bucket.append(current_time)
            return True
        return False
    
    def leak(self, current_time):
        """Leak the requests from the bucket at the fixed rate."""
        # Calculate how many seconds have passed since the last leak
        elapsed_time = current_time - self.last_leak_time
        leaked_requests = int(elapsed_time * self.leak_rate)
        
        if leaked_requests > 0:
            # Remove the leaked requests from the bucket
            for _ in range(min(leaked_requests, len(self.bucket))):
                self.bucket.popleft()
            
            # Update the last leak time
            self.last_leak_time = current_time
                

if __name__ == "__main__":
    limiter = LeakyBucket(capacity=5, leak_rate=1)

    for _ in range(10):
        current_time = time.time()
        success = limiter.add_request(current_time)
        # print(limiter.add_request(current_time))
        if success:
            print("Request added: ", current_time)
        else:
            print("Request discarded: ", current_time)
        time.sleep(0.1)
    
    time.sleep(2)
    current_time = time.time()
    # print(limiter.add_request(current_time))
    success = limiter.add_request(current_time)
    if success:
        print("Request added: ", current_time)
    else:
        print("Request discarded: ", current_time)

