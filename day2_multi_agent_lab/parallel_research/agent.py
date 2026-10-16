from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

pros_agent = Agent(
    name="ProsAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="Use google_search to find 2-3 advantages of the given topic. Cite sources.",
    tools=[google_search],
    output_key="pros",
)

cons_agent = Agent(
    name="ConsAgent",
    model=Gemini(model="gemini-3.5-flash"),
    instruction="Use google_search to find 2-3 disadvantages of the given topic. Cite sources.",
    tools=[google_search],
    output_key="cons",
)

cost_agent = Agent(
    name="CostAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="Use google_search to find typical cost/pricing info on the given topic. Cite sources.",
    tools=[google_search],
    output_key="costs",
)

# Synthesis agent
merger_agent = Agent(
    name="MergerAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""Combine these three research angles into one balanced briefing with headed sections:
Pros: {pros}
Cons: {cons}
Costs: {costs}""",
    output_key="briefing",
)

# Fan-out: run the three researchers concurrently; each writes its own output_key.
research_fanout = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[pros_agent, cons_agent, cost_agent],
)

# Fan-in: run the parallel block first, then the merger reads pros/cons/costs
# from shared session state and synthesises the final briefing.
root_agent = SequentialAgent(
    name="ParallelThenMergeAgent",
    sub_agents=[research_fanout, merger_agent],
)