import asyncio, os
from google.adk.sessions import DatabaseSessionService
from agent import root_agent

async def main():
    db_file = "recipe_sessions.db"
    db_service = DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{db_file}")
    session = await db_service.create_session(
        app_name="RecipeApp", user_id="user_alex", session_id="db_001",
        state={"diet_type": "Keto", "allergies": ["Dairy"]}
    )
    assert os.path.exists(db_file)
    print("[SUCCESS] DatabaseSessionService True/False assertion passed!")

if __name__ == "__main__":
    asyncio.run(main())

