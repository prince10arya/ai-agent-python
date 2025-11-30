"""Vercel entry point for FastAPI application."""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from main import app

# Vercel expects 'app' variable
__all__ = ['app']
