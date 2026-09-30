from typing import List
from google.adk.agents import Agent
from google.adk.tools import ToolContext

def set_dietary_profile(user_name: str, diet_type: str, allergies: List[str], tool_context: ToolContext) -> str:
    state = tool_context.session.state
    state["user_name"] = user_name
    state["diet_type"] = diet_type
    state["allergies"] = allergies
    return f"Profile saved for {user_name}! Diet: {diet_type}"

def save_favorite_recipe(recipe_name: str, prep_time_mins: int, tool_context: ToolContext) -> str:
    state = tool_context.session.state
    favs = state.get("favorite_recipes", [])
    favs.append({"name": recipe_name, "prep_time": prep_time_mins})
    state["favorite_recipes"] = favs
    return f"Saved '{recipe_name}' to favorites."

def inspect_recipe_attachment(tool_context: ToolContext) -> str:
    atts = getattr(tool_context, "attachments", None) or tool_context.session.state.get("latest_attachment")
    if not atts: return "No attachment found."
    return f"Processed attachment: {atts}"

root_agent = Agent(
    name="recipe_helper",
    model="gemini-2.5-flash",
    instruction="Stateful Recipe Assistant for managing profile state and attachments.",
    tools=[set_dietary_profile, save_favorite_recipe, inspect_recipe_attachment]
)


