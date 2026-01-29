"""Configuration and logging setup for db_tool package."""
from __future__ import annotations
import os
import logging
from rich.console import Console
from openai import OpenAI

MODEL_NAME = os.environ.get("LLM_MODEL","")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

client = OpenAI(base_url=os.environ.get("API_BASE_URL",""), api_key=os.environ.get("API_KEY", ""))
