import asyncio

from config.settings import SYSTEM_PROMPT_PATH
from core.browser import create_browser
from core.agent import create_agent
from core.auth_agent import AuthAgent, AuthState


SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8") if SYSTEM_PROMPT_PATH.exists() else ""

browser = create_browser()
auth_agent = AuthAgent(browser)

async def main():
    await browser.start()

    while True:
        task = input("Введите задачу: ")

        if task == "exit":
            break

        agent = create_agent(task, browser)
        
        print("🚀 Запуск агента...")
        history = await agent.run()

        # Access useful information
        # history.urls()                    # List of visited URLs
        # history.screenshot_paths()        # List of screenshot paths  
        # history.screenshots()             # List of screenshots as base64 strings
        # history.action_names()            # Names of executed actions
        # history.extracted_content()       # List of extracted content from all actions
        # history.errors()                  # List of errors (with None for steps without errors)
        # history.model_actions()           # All actions with their parameters
        # history.model_outputs()           # All model outputs from history
        # history.last_action()             # Last action in history

        # # Analysis methods
        # history.final_result()            # Get the final extracted content (last step)
        # history.is_done()                 # Check if agent completed successfully
        # history.is_successful()           # Check if agent completed successfully (returns None if not done)
        # history.has_errors()              # Check if any errors occurred
        # history.model_thoughts()          # Get the agent's reasoning process (AgentBrain objects)
        # history.action_results()          # Get all ActionResult objects from history
        # history.action_history()          # Get truncated action history with essential fields
        # history.number_of_steps()         # Get the number of steps in the history
        # history.total_duration_seconds()  # Get total duration of all steps in seconds

        # Structured output (when using output_model_schema)
        print(history.structured_output)         # Property that returns parsed structured output
    
if __name__ == "__main__":
    asyncio.run(main())
