from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini


class Recipe(BaseModel):
    """Schema the model must return. Field descriptions guide the generation."""

    title: str = Field(description="A short, appetising name for the dish.")
    prep_minutes: int = Field(description="Total preparation time in minutes.")
    ingredients: list[str] = Field(
        description="Ingredients, each with its quantity, e.g. '2 cups flour'."
    )
    steps: list[str] = Field(description="Ordered preparation steps.")


# Setting output_schema forces the model to emit JSON that validates against
# Recipe; the parsed object is written to session state under output_key.
# Constraint: an agent with output_schema cannot use tools or transfer control.
root_agent = LlmAgent(
    name="StructuredRecipeAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""The user names a dish or lists some ingredients. Reply with ONE
recipe that conforms to the required schema. Output only the JSON object, with no
surrounding prose or markdown fencing.""",
    output_schema=Recipe,
    output_key="recipe",
)
