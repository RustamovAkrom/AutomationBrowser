import os
import platform
from browser_use import Browser
from pathlib import Path
from config.settings import (
    CHROME_PATH,
    USER_DATA_DIR,
    PROFILE,
    PAGE_LOAD_WAIT,
)

def get_chrome_config() -> dict:
    if CHROME_PATH and USER_DATA_DIR:
        return {
            "executable_path": CHROME_PATH,
            "user_data_dir": USER_DATA_DIR
        }
    
    system = platform.system()

    if system == "Darwin":  # macOS
        executable_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user_data_dir = Path.home() / "Library/Application Support/Google/Chrome"

    elif system == "Windows":
        executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        user_data_dir = Path(os.environ["LOCALAPPDATA"]) / "Google/Chrome/User Data"

    elif system == "Linux":
        executable_path = "/usr/bin/google-chrome"
        user_data_dir = Path.home() / ".config/google-chrome"

    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    return {
        "executable_path": str(executable_path),
        "user_data_dir": str(user_data_dir),
    }

def create_browser() -> Browser:
    return Browser(
        executable_path=CHROME_PATH,
        user_data_dir=USER_DATA_DIR,
        profile_directory=PROFILE,
        headless=False, # ! required
        minimum_wait_page_load_time=PAGE_LOAD_WAIT,
        ignore_default_args=True,
    )
