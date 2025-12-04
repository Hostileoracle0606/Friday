"""Validate backend structure without requiring all dependencies"""
import os
import sys
from pathlib import Path

errors = []
warnings = []

# Check required files exist
required_files = [
    "app/main.py",
    "app/core/config.py",
    "app/core/database.py",
    "app/core/security.py",
    "app/models/user.py",
    "app/models/task.py",
    "app/models/journal.py",
    "app/models/oauth_token.py",
    "app/routes/auth.py",
    "app/routes/task.py",
    "app/routes/journal.py",
    "app/routes/sync.py",
    "app/services/task_service.py",
    "app/services/journal_service.py",
    "app/services/encryption_service.py",
    "alembic/env.py",
    "requirements.txt",
]

print("Validating backend structure...\n")

for file_path in required_files:
    if not Path(file_path).exists():
        errors.append(f"Missing file: {file_path}")
    else:
        print(f"✓ {file_path}")

# Check test files
test_files = [
    "tests/conftest.py",
    "tests/test_auth.py",
    "tests/test_tasks.py",
    "tests/test_journal.py",
]

print("\nValidating test files...\n")
for file_path in test_files:
    if not Path(file_path).exists():
        warnings.append(f"Missing test file: {file_path}")
    else:
        print(f"✓ {file_path}")

# Check migrations
migration_files = [
    "alembic/versions/001_initial_schema.py",
    "alembic/versions/002_add_oauth_tokens.py",
]

print("\nValidating migrations...\n")
for file_path in migration_files:
    if not Path(file_path).exists():
        warnings.append(f"Missing migration: {file_path}")
    else:
        print(f"✓ {file_path}")

# Check services directory
services_dir = Path("../services/ingestion")
if services_dir.exists():
    print(f"\n✓ Services directory exists")
    if (services_dir / "brightspace_client.py").exists():
        print(f"✓ Brightspace client exists")
    if (services_dir / "calendar_client.py").exists():
        print(f"✓ Calendar client exists")
else:
    warnings.append("Services directory not found")

print("\n" + "="*50)
if errors:
    print("ERRORS FOUND:")
    for error in errors:
        print(f"  ✗ {error}")
    sys.exit(1)
else:
    print("✓ Structure validation passed!")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    print("\nNote: Full tests require dependencies to be installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(0)

