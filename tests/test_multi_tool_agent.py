import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

def get_research_status() -> dict:
    """Check whether the ResearchPilot research pipeline is operational."""
    print("\n TOOL CALLED: get_research_status()")

    return {
        "status": "operational",
        "message": "ResearchPilot research pipeline is wokring."
    }

def search_papers(topic:str) -> dict:
    """Search for research papers about a given topic.

    This is a mock paper-search tool for testing the orchestration pipeline.
    """
    print(f"\n Tool called: search_papers(topic={topic!r})")

    return {
        "topic": topic,
        "papers": [
            {
                "title":"Retrieval-Augmented Generation: A Survey",
                "year": 2023,
                "relevance":"high"
            },
            {
                "title": "Self-RAG: Learning to Retrieve, Generate, and Critique",
                "year": 2023,
                "relevance": "high"
            }
        ]
    }

APP_NAME = "researchpilot_multi_tool_test"
USER_ID = "test_user"

root_agent = Agent(
    name="researchpilot_multi_tool_agent",
    model=Gemini(model="gemini-3.6-flash"),
    instruction="""
    You are the ResearchPilot orchestration agent.

    You have two tools:
    1. get_research_status - checks whether the research system is operational.
    2. search_papers - searches for papers about a research topic.

    Decide which tools are necessary based on the user's request.

    If the user asks for both system status and papers:
    - Check the system status.
    - Search for the requested papers.
    - Use the tool results to produce a concise summary.

    Never invent tool results.
    """,
    tools=[
        get_research_status,
        search_papers,
    ],
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
                    "First check whether the research system is operational, "
                    "then find papers about Retrieval Augmented Generation."
                )
            )
        ],
    )

    print("\n--- Starting Multi-Tool Agent ---\n")

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.content:
            print(f"\nEVENT FROM: {event.author}")

            for part in event.content.parts:
                if part.function_call:
                    print(
                        f"  → FUNCTION CALL: "
                        f"{part.function_call.name}"
                    )

                if part.function_response:
                    print(
                        f"  → FUNCTION RESPONSE: "
                        f"{part.function_response.name}"
                    )

                if part.text:
                    print(f"  → TEXT: {part.text}")

        if event.is_final_response():
            print("\nFINAL RESPONSE:")
            if event.content and event.content.parts:
                print(event.content.parts[0].text)

    print("\n--- Multi-Tool Agent Finished ---\n")


if __name__ == "__main__":
    asyncio.run(main())
