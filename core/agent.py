from browser_use import Agent
from core.skills import tools
from core.llm import create_llm

def create_agent(task: str, browser) -> Agent:
    return Agent(
        task=task,
        browser=browser,
        llm=create_llm(),
        tools=tools,
    )
