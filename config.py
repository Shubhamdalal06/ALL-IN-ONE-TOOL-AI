"""
Quick Start Configuration for AI All-in-One Tool
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_PATH = str(DATA_DIR / "ai_tool.db")

# API Configuration
API_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
API_PORT = int(os.getenv("SERVER_PORT", 8000))

# LLM Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

# Print startup info
if __name__ == "__main__":
    print("=" * 50)
    print("AI All-in-One Data Tool Configuration")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Backend Dir: {BACKEND_DIR}")
    print(f"Frontend Dir: {FRONTEND_DIR}")
    print(f"Data Dir: {DATA_DIR}")
    print(f"Database: {DATABASE_PATH}")
    print(f"\nAPI Server: {API_HOST}:{API_PORT}")
    print(f"LLM API Key: {'Set' if ANTHROPIC_API_KEY else 'NOT SET'}")
    print(f"Google Sheets: {'Configured' if GOOGLE_SHEETS_CREDENTIALS else 'Not configured'}")
    print("=" * 50)
