import asyncio
from google.adk.sessions import InMemorySessionService
from agent import root_agent

async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="RecipeApp", user_id="user_alex", session_id="inmemory_001",
        state={"diet_type": "Vegan", "allergies": ["Peanuts"]}
    )
    retrieved = await session_service.get_session("RecipeApp", "user_alex", "inmemory_001")
    assert retrieved.state["diet_type"] == "Vegan"
    print("[SUCCESS] InMemorySessionService True/False assertion passed!")

if __name__ == "__main__":
    asyncio.run(main())

