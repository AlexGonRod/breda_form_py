import time
from collections import defaultdict
from formulari_app.lib.logger import logger

class RateLimiter:

    # Configure: max_requests per time_window (seconds)
    MAX_REQUESTS = 3
    TIME_WINDOW = 60  # 1 minute

    # Store request timestamps by IP: {ip: [timestamp1, timestamp2, ...]}
    _request_history = defaultdict(list)

    @classmethod
    def is_allowed(cls, client_ip: str) -> tuple[bool, str]:
        current_time = time.time()

        # Clean old requests outside time window
        cls._request_history[client_ip] = [
            req_time for req_time in cls._request_history[client_ip]
            if current_time - req_time < cls.TIME_WINDOW
        ]

        # Check if exceeded limit
        request_count = len(cls._request_history[client_ip])
        if request_count >= cls.MAX_REQUESTS:
            wait_time = int(cls._request_history[client_ip][0] + cls.TIME_WINDOW - current_time)
            message = f"Rate limit exceeded. Try again in {wait_time} seconds."
            logger.warning("⚠️ Rate limit exceeded for IP %s. Requests: %d/%d",
                         client_ip, request_count, cls.MAX_REQUESTS)
            return False, message
        # Add current request
        cls._request_history[client_ip].append(current_time)
        logger.debug("✅ Request allowed for IP %s. Requests: %d/%d",
                    client_ip, request_count + 1, cls.MAX_REQUESTS)
        return True, "OK"

    @classmethod
    def reset(cls, client_ip: str = None):
        if client_ip:
            cls._request_history.pop(client_ip, None)
            logger.info("Rate limit reset for IP %s", client_ip)
        else:
            cls._request_history.clear()
            logger.info("Rate limit reset for all IPs")
