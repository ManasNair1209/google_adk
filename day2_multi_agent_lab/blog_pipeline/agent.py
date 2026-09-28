from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.workflow import START, Workflow

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

# Equivalent ordered pipeline using Workflow
root_agent = Workflow(
    name="BlogPipelineAgent",
    edges=[
        (START, writer_agent, reviewer_agent, polisher_agent),
    ],
)