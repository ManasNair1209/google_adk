from google.adk.agents import Agent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import exit_loop

# LoopAgent is the third workflow-agent type (alongside SequentialAgent and
# ParallelAgent). It re-runs its sub-agents in order until a sub-agent escalates
# (here, by calling exit_loop) or max_iterations is hit.
#
# Pattern: a Writer and a Critic take turns. The `?` in {draft?}/{critique?}
# marks the state key optional, so the first iteration (when nothing is stored
# yet) renders an empty string instead of raising a KeyError.

writer_agent = Agent(
    name="WriterAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""Write or improve a short (~60 word) marketing paragraph for the user's topic.

If a critique is present, revise the previous draft to address every point in it.
Previous draft: {draft?}
Critique to address: {critique?}

Output only the improved paragraph, nothing else.""",
    output_key="draft",
)

critic_agent = Agent(
    name="CriticAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""You are a strict editor reviewing this draft:
{draft}

If it is punchy, specific, and free of clichés, call the exit_loop tool to stop.
Otherwise, reply with 1-2 concrete, actionable fixes (no praise, no rewrite).""",
    tools=[exit_loop],
    output_key="critique",
)

# Writer -> Critic, repeated up to 3 times or until the critic calls exit_loop.
root_agent = LoopAgent(
    name="IterativeRefiner",
    sub_agents=[writer_agent, critic_agent],
    max_iterations=3,
)
