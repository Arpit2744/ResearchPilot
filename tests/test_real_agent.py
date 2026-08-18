import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.pipeline.paper_search import search_papers


load_dotenv()


APP_NAME = "researchpilot_real_test"
USER_ID = "test_user"


root_agent = Agent(
    name="researchpilot_real_agent",
    model=Gemini(model="gemini-3.6-flash"),
    instruction="""
    You are ResearchPilot, a research assistant.

    When the user asks to find research papers,
    use the search_papers tool.

    Do not invent papers or metadata.

    After receiving search results:
    - identify the most relevant papers
    - mention their titles and years
    - briefly explain why they are relevant
    - provide the paper URLs when available

    Keep the response concise.
    """,
    tools=[search_papers],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Find 5 research papers about Retrieval-Augmented "
                    "Generation and tell me which ones are most relevant "
                    "for someone starting research in RAG."
                )
            )
        ],
    )

    print("\n--- ResearchPilot Started ---\n")

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.content:
            for part in event.content.parts:

                if part.function_call:
                    print(
                        f"🔧 TOOL CALL: {part.function_call.name}"
                    )

                if part.function_response:
                    print(
                        f"📥 TOOL RESULT: "
                        f"{part.function_response.name}"
                    )

                if part.text:
                    print(f"\n🤖 {part.text}")

    print("\n--- ResearchPilot Finished ---\n")


if __name__ == "__main__":
    asyncio.run(main())