from config.settings import SYSTEM_PROMPT_PATH
from browser_use import ChatBrowserUse

if not SYSTEM_PROMPT_PATH.exists():
    raise FileNotFoundError(f"System prompt not found: {SYSTEM_PROMPT_PATH}")

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

def create_llm():
    # Можно легко заменить на OpenAI / Gemini / Grok
    return ChatBrowserUse(system_prompt=SYSTEM_PROMPT)
