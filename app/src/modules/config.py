import os
import socket

def get_api_base_url():
    # 1. Check for an explicit ENV variable
    env = os.getenv("ENV", "").lower()

    if env == "docker":
        return "http://web-api:4000"

    # 2. Use hostname to guess (optional fallback)
    hostname = socket.gethostname().lower()
    if "web-app" in hostname or "container" in hostname:
        return "http://web-api:4000"

    # 3. Fallback: assume localhost for dev
    return "http://localhost:4000"
