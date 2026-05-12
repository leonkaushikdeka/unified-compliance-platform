import hashlib
import hmac
import re
import time
from collections import defaultdict

from src.core.config import settings


def hash_pii(value: str) -> str:
    return hmac.new(
        settings.ENCRYPTION_KEY.encode(),
        value.encode(),
        hashlib.sha256,
    ).hexdigest()


def validate_password_strength(password: str) -> str | None:
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;'/`~]", password):
        return "Password must contain at least one special character"
    return None


class InMemoryRateLimiter:
    def __init__(self):
        self._attempts = defaultdict(list)

    def check(self, key: str, max_attempts: int = 5, window: int = 60) -> bool:
        now = time.time()
        self._attempts[key] = [t for t in self._attempts[key] if now - t < window]
        if len(self._attempts[key]) >= max_attempts:
            return False
        self._attempts[key].append(now)
        return True


rate_limiter = InMemoryRateLimiter()
