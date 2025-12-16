import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]

# Browser
CHROME_PATH = None
USER_DATA_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

PROFILE = "Default"
BROWSER_TIMEOUT = 30
PAGE_LOAD_WAIT = 5

# AI 
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system.txt"
