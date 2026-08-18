import asyncio
import uuid
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


load_dotenv()

APP_NAME = "ResearchPilot_test"
USER_ID = "test_user"

root_agent = Agent(
    name = "Researchpilot_test",
    model = Gemini(model="gemini-3.6-flash"),
    instruction = """
    you are a test agent for ResearchPilot.
    answer the user's request briefly and clearly.
"""
)

async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name = APP_NAME,
        user_id = USER_ID,
    )
    runner = Runner(
        app_name=APP_NAME,
        agent = root_agent,
        session_service = session_service,
    )
    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="Say hello to ResearchPilot and confirm that you are running through google adk."
            )
        ],
    )
    print("\n----starting ADK Agent----\n")

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(event.content.parts[0].text)
    print("\n---ADK agent finished --\n")

if __name__ == "__main__":
    asyncio.run(main())          