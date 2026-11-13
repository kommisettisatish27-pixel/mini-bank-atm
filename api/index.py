"""
Entry point Vercel's Python runtime loads. It simply re-exposes the
Flask app object defined in app.py at the project root.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402  (Vercel's @vercel/python looks for `app`)
