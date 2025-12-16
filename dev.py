import asyncio
import os
from browser_use import Browser
from agents.email_agent import EmailAgent
from agents.jobs_agent import JobsAgent
from agents.food_agent import FoodAgent

COOKIES_PATH = "cookies.json"

async def main():
    # 1. Инициализация браузера
    browser = Browser(headless=False)

    # 2. Загрузка cookies (если есть)
    if os.path.exists(COOKIES_PATH):
        browser.load_cookies(COOKIES_PATH)

    print("Открой браузер и войди в нужный сервис. Нажми Enter, когда будешь готов запустить агента...")
    input()

    # 3. Ввод задачи для агента
    task = input("Опиши задачу для агента: ").lower()

    # 4. Выбор sub-agent по ключевым словам
    if "почта" in task or "спам" in task:
        agent = EmailAgent(task, browser)
    elif "заказ" in task or "бургер" in task or "еда" in task:
        agent = FoodAgent(task, browser)
    elif "вакансии" in task or "hh.ru" in task:
        agent = JobsAgent(task, browser)
    else:
        print("Не удалось определить тип задачи. Используется базовый агент.")
        return

    # 5. Запуск агента
    await agent.run()

    # 6. Сохранение cookies после работы
    browser.save_cookies(COOKIES_PATH)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Произошла ошибка:", e)
