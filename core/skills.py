from browser_use import Tools, Browser

tools = Tools()

@tools.action(description="Save job results to a JSON file")
def save_to_json(jobs: str, filename: str = "results.json") -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(jobs)
    return f"Saved jobs to {filename}"

@tools.action(
    description="Estimate authentication confidence (0.0–1.0) using heuristic signals"
)
async def auth_confidence(url: str, browser: Browser) -> float:
    """
    Returns a confidence score:
    0.0  -> very likely NOT authenticated
    1.0  -> very likely authenticated
    """
    await browser.goto(url)

    score = 0.5  # начинаем с нейтрального состояния

    # ─────────────────────────────────────────
    # 1️⃣ URL heuristic
    # ─────────────────────────────────────────
    current_url = browser.page.url.lower()
    if any(x in current_url for x in ["login", "signin", "auth"]):
        score -= 0.4
    else:
        score += 0.1

    # ─────────────────────────────────────────
    # 2️⃣ Password input heuristic
    # ─────────────────────────────────────────
    inputs = await browser.page.get_visible_elements(tag="input")
    for el in inputs:
        if (el.get("type") or "").lower() == "password":
            score -= 0.5
            break

    # ─────────────────────────────────────────
    # 3️⃣ Login-like text heuristic (semantic)
    # ─────────────────────────────────────────
    login_keywords = ["login", "sign in", "войти", "пароль"]
    elements = await browser.page.get_visible_elements()

    for el in elements:
        text = (el.get("text") or "").lower()
        role = (el.get("role") or "").lower()

        if role in {"button", "link"} and any(k in text for k in login_keywords):
            score -= 0.3
            break

    # ─────────────────────────────────────────
    # 4️⃣ Profile / account signals (positive)
    # ─────────────────────────────────────────
    profile_keywords = [
        "profile", "account", "мой профиль",
        "настройки", "logout", "выйти"
    ]

    for el in elements:
        text = (el.get("text") or "").lower()
        aria = (el.get("aria-label") or "").lower()

        if any(k in (text + aria) for k in profile_keywords):
            score += 0.4
            break

    # ─────────────────────────────────────────
    # 5️⃣ Clamp score to [0, 1]
    # ─────────────────────────────────────────
    score = max(0.0, min(1.0, score))
    return round(score, 2)


@tools.action(description="Heuristically check if user is authenticated on a site")
async def check_authorization(url: str, browser: Browser) -> bool:
    """
    Smart, site-agnostic authorization check.
    Uses multiple weak signals instead of hardcoded selectors or texts.
    """
    await browser.goto(url)

    # 1️⃣ URL heuristic
    current_url = browser.page.url.lower()
    if any(x in current_url for x in ["login", "signin", "auth"]):
        return False

    # 2️⃣ Look for password inputs
    inputs = await browser.page.get_visible_elements(tag="input")
    for el in inputs:
        el_type = (el.get("type") or "").lower()
        if el_type == "password":
            return False

    # 3️⃣ Look for login-like forms
    forms = await browser.page.get_visible_elements(tag="form")
    for form in forms:
        text = (form.get("text") or "").lower()
        if any(x in text for x in ["login", "sign in", "войти", "пароль"]):
            return False

    # 4️⃣ Look for login buttons / links (semantic, not selectors)
    clickable = await browser.page.get_visible_elements()
    for el in clickable:
        role = (el.get("role") or "").lower()
        text = (el.get("text") or "").lower()

        if role in {"button", "link"}:
            if any(x in text for x in ["login", "sign in", "войти"]):
                return False

    # 5️⃣ Look for profile / account signals
    for el in clickable:
        text = (el.get("text") or "").lower()
        aria = (el.get("aria-label") or "").lower()

        if any(x in text + aria for x in ["profile", "account", "мой профиль", "выйти", "logout"]):
            return True

    # 6️⃣ Default: assume authenticated if no login signals found
    return True


@tools.action(description="Extract simplified page info for agent reasoning")
async def get_page_summary(browser: Browser) -> str:
    text = await browser.page.get_text()
    elems = await browser.page.get_visible_elements()
    summary = text[:2000]  # ограничение токенов
    return f"Text snippet:\n{summary}\nVisible elements count: {len(elems)}"


@tools.action(description="Ask user to manually login on a site and wait.")
def wait_for_manual_login(site_url: str):
    print(f"\n🔐 PLEASE LOGIN MANUALLY")
    print(f"🌐 Site: {site_url}")
    print("👉 Complete login in the browser window.")
    input("✅ Press ENTER after you finish login...")
