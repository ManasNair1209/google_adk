from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini

# Three specialists analyse the SAME input text concurrently. Because they run
# in parallel they must each write to a DIFFERENT output_key to avoid clashing.

sentiment_agent = Agent(
    name="SentimentAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="Classify the overall sentiment of the user's text as Positive, Negative, or Mixed, with one sentence of justification.",
    output_key="sentiment",
)

keyword_agent = Agent(
    name="KeywordAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="Extract 3-5 key topics or keywords from the user's text as a comma-separated list.",
    output_key="keywords",
)

summary_agent = Agent(
    name="SummaryAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="Summarise the user's text in a single concise sentence.",
    output_key="summary",
)

# Fan-out: all three analysts run at the same time on the same input.
analysis_fanout = ParallelAgent(
    name="ParallelAnalysis",
    sub_agents=[sentiment_agent, keyword_agent, summary_agent],
)

# Fan-in: compose the three state values into one structured report.
report_agent = Agent(
    name="ReportAgent",
    model=Gemini(model="gemini-3.5-flash-lite"),
    instruction="""Produce a short analysis report using the fields below:

Sentiment: {sentiment}
Keywords: {keywords}
Summary: {summary}""",
    output_key="report",
)

# Run the parallel analysis first, then build the combined report.
root_agent = SequentialAgent(
    name="ParallelAnalysisAgent",
    sub_agents=[analysis_fanout, report_agent],
)
