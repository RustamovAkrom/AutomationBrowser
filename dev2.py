import asyncio
from browser_use import Agent, Browser, ChatOpenAI, ChatBrowserUse
from dotenv import load_dotenv
import os

load_dotenv()

# # macOS
# executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# user_data_dir='~/Library/Application Support/Google/Chrome'

# # Windows
# executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
# user_data_dir='%LOCALAPPDATA%\\Google\\Chrome\\User Data'

# # Linux
# executable_path='/usr/bin/google-chrome'
# user_data_dir='~/.config/google-chrome'

# Connect to your existing Chrome browser
browser = Browser(
    # Windows
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    user_data_dir='%LOCALAPPDATA%\\Google\\Chrome\\User Data',
    profile_directory='Default',
    minimum_wait_page_load_time=10,
)

# llm = ChatOpenAI(
#     # model='x-ai/grok-4',
# 	model='gemini-1.5-flash',
# 	base_url='https://openrouter.ai/api/v1',
# 	api_key=os.getenv('OPENROUTER_API_KEY'),
# )
llm = ChatBrowserUse()


async def main():
    await browser.start()
    task = input("Enter your promt:  ")
    agent = Agent(
        task=task, 
        llm=llm,
        browser=browser,
    )
    await agent.run()


if __name__=='__main__':
    asyncio.run(main())
