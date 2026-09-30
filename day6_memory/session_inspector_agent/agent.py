import asyncio
import os
import sys
from dotenv import load_dotenv

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from google.adk.agents import LlmAgent
from google.adk.memory import InMemoryMemoryService
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Plain agent, no memory tools -- this session only fills short-term storage.
root_agent = LlmAgent(
    model=Gemini(model="gemini-3.5-flash", retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words.",
)

async def main():
    print("=== STEP 1: INITIALIZE ===")
    memory_service = InMemoryMemoryService()
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("=== STEP 2: HAVE A CONVERSATION (fills the SESSION only) ===")
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
    )
    query = "My favorite color is blue-green. Can you write a Haiku about it?"
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session.id, new_message=query_content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Model: > {event.content.parts[0].text}")

    print("=== STEP 3: INSPECT THE SESSION ===")
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
    )
    for event in session.events:
        text = event.content.parts[0].text[:60] if event.content and event.content.parts else "(empty)"
        print(f"  {event.content.role}: {text}...")

    print("=== STEP 4: INGEST -- copy the session into long-term MEMORY ===")
    await memory_service.add_session_to_memory(session)

    print("=== STEP 5: VERIFY -- search memory directly (no agent involved) ===")
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="favorite color"
    )
    print(f"Found {len(search_response.memories)} matching entrie(s).")

if __name__ == "__main__":
    asyncio.run(main())