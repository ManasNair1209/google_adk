from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini

writer_agent = Agent(
    name="WriterAgent",
    model=Gemini(model="gemini-3.5-flash"),
    instruction="Write a short (150-word) blog post draft on the given topic.",
    output_key="draft",
)

reviewer_agent = Agent(
    name="ReviewerAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""Review this draft for clarity and tone, list 2-3 concrete issues:
{draft}""",
    output_key="review_notes",
)

polisher_agent = Agent(
    name="PolisherAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""Rewrite the draft below, fixing the listed issues. Output only the final post.
Draft: {draft}
Issues: {review_notes}""",
    output_key="final_post",
)

# Ordered pipeline: writer -> reviewer -> polisher.
# Each agent writes its result to session state via output_key, and the next
# agent reads it back through the {placeholders} in its instruction.
root_agent = SequentialAgent(
    name="BlogPipelineAgent",
    sub_agents=[writer_agent, reviewer_agent, polisher_agent],
)