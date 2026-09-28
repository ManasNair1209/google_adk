from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.adk.workflow import JoinNode, START, Workflow

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

join_results = JoinNode(name="JoinResearchResults")

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

# Equivalent pipeline using Workflow (non-deprecated):
# START -> (pros, cons, cost) in parallel -> join -> merger
root_agent = Workflow(
    name="ParallelThenMergeAgent",
    edges=[
        (START, (pros_agent, cons_agent, cost_agent), join_results, merger_agent),
    ],
)