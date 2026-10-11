#!/usr/bin/env python
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import init_db, engine
from app.core.config import get_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    settings = get_settings()
    logger.info(f"Initializing database: {settings.database_url}")
    
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}", exc_info=True)
        sys.exit(1)
