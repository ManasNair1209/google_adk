from google.adk.agents import Agent
from google.adk.tools import google_search, url_context

root_agent = Agent(
    name="BuiltinToolsAgent",
    model="gemini-3.5-flash",
    instruction="""You are a research assistant equipped with web tools:

1. google_search: Use when answering queries requiring live web data or current events.
2. url_context: Use when given a direct URL to read and summarize.

You can chain both tools: first search for a topic, then read a target URL deeply. Always cite your sources.""",
    tools=[google_search, url_context],
)
