"""Quick test to verify backend structure"""
import sys
import os

# Set test environment
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("API_V1_PREFIX", "/api/v1")

try:
    from app.main import app
    from app.core.database import Base
    from app.models import User, Task, JournalEntry, OAuthToken
    from app.routes import auth, task, journal, sync
    
    print("✓ All imports successful")
    print("✓ FastAPI app initialized")
    print("✓ Models loaded: User, Task, JournalEntry, OAuthToken")
    print("✓ Routes loaded: auth, task, journal, sync")
    print("\nBackend structure is valid!")
    sys.exit(0)
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nSome dependencies may be missing. Install with: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

