import os
import sys
from mcp import StdioServerParameters
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams

MCP_SERVER_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mcp_server.py"))

server_params = StdioServerParameters(
    command=sys.executable,
    args=[MCP_SERVER_SCRIPT],
    env=dict(os.environ),
)

mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=server_params,
        timeout=10
    ),
)

root_agent = Agent(
    name="MCPAgent",
    model="gemini-3.5-flash-lite",
    instruction="""You are an Enterprise Assistant powered by Model Context Protocol (MCP).
Use your MCP tools to assist the user accurately.""",
    tools=[mcp_toolset],
)



