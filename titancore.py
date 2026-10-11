#!/usr/bin/env python
import os
import sys
import subprocess
from pathlib import Path

BACKEND_DIR = Path(__file__).parent / "backend"
FRONTEND_DIR = Path(__file__).parent / "frontend"

def validate_env():
    env_file = Path(".env")
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "ENVIRONMENT",
        "API_PREFIX",
        "LOG_LEVEL",
    ]
    
    if not env_file.exists():
        print("[TITANCORE] ❌ .env file not found")
        print("[TITANCORE] Creating .env.example-based defaults...")
        create_env_template()
        sys.exit(1)
    
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                env_vars[key] = value
    
    missing = [v for v in required_vars if v not in env_vars]
    if missing:
        print(f"[TITANCORE] ❌ Missing environment variables: {', '.join(missing)}")
        sys.exit(1)
    
    print("[TITANCORE] ✅ Environment validation passed")

def create_env_template():
    template = """DATABASE_URL=sqlite:///./data/scrapmaster.db
SECRET_KEY=change-me-in-production-with-secure-random-32-chars
ENVIRONMENT=development
API_PREFIX=/api/v1
LOG_LEVEL=INFO
DEBUG=False
MAX_UPLOAD_SIZE_MB=500
ENABLE_OPENCV=True
ENABLE_OLLAMA=False
OLLAMA_BASE_URL=http://localhost:11434
CORS_ORIGINS=*
"""
    with open(".env", "w") as f:
        f.write(template)
    print("[TITANCORE] ✅ .env template created. Edit and rerun.")

def init_database():
    print("[TITANCORE] 🗄️  Initializing database schema...")
    os.chdir(BACKEND_DIR)
    try:
        subprocess.run(
            [sys.executable, "-m", "app.core.database"],
            check=True,
            capture_output=True,
        )
        print("[TITANCORE] ✅ Database initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"[TITANCORE] ❌ Database initialization failed: {e.stderr.decode()}")
        sys.exit(1)
    finally:
        os.chdir("../..")

def main():
    if len(sys.argv) < 2:
        print("[TITANCORE] Usage: python titancore.py [init|validate|db-init|check]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        print("[TITANCORE] 🚀 Initializing ScrapMaster AI system...")
        create_env_template()
        validate_env()
        init_database()
        print("[TITANCORE] ✅ System initialization complete")
    
    elif command == "validate":
        print("[TITANCORE] 🔍 Validating environment...")
        validate_env()
    
    elif command == "db-init":
        print("[TITANCORE] 🗄️  Initializing database...")
        init_database()
    
    elif command == "check":
        print("[TITANCORE] 🏥 System health check...")
        validate_env()
        print("[TITANCORE] ✅ All checks passed")
    
    else:
        print(f"[TITANCORE] ❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
