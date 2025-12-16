from enum import Enum
from browser_use import Browser, Tools


tools = Tools()

class AuthState(str, Enum):
    AUTHORIZED = "authorized"
    NEEDS_LOGIN = "needs_login"
    UNCERTAIN = "uncertain"


class AuthAgent:
    def __init__(self, browser: Browser):
        self.browser = browser

    async def ensure_access(
            self,
            url: str,
            low: float = 0.4,
            high: float = 0.7,
    ) -> AuthState:

        confidence = await tools.auth_confidence(url, self.browser)

        if confidence < low:
            return AuthState.NEEDS_LOGIN
        
        if confidence > high:
            return AuthState.AUTHORIZED
        
        return AuthState.UNCERTAIN
    
    async def resolve_login(self, url: str) -> None:
        """
        Blocks execution until user logs in manually.
        Enhanced: retries confidence check after manual login.
        """
        while True:
            await self.browser.goto(url)
            tools.wait_for_manual_login(url)
            confidence = await tools.auth_confidence(url, self.browser)
            if confidence > 0.7:
                break
