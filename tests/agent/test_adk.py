from google.adk.agents import Agent
from google.adk.models import Gemini

root_agent = Agent(
    name = "ResearchPilot_test",
    model = Gemini(model="gemini-3.6-flash"),
    instruction="""
    you are a test agent for researchpilot.
    respond clearly and briefly"""
)

print("ADK  agent created successfully")
print(f"Agent name: {root_agent.name}")