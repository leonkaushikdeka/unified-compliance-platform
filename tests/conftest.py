import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Set environment variables for testing
import os

os.environ["APP_ENV"] = "testing"
os.environ["APP_DEBUG"] = "true"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
