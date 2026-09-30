import os, sys, asyncio
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams

class DummyContext:
    pass

async def run_verification():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[os.path.abspath("mcp_server.py")],
        env=dict(os.environ),
    )
    toolset = McpToolset(connection_params=StdioConnectionParams(server_params=server_params, timeout=10))
    tools = await toolset.get_tools()
    print(f"[OK] Discovered {len(tools)} MCP Tools")
    
    weather_tool = next((t for t in tools if t.name == "get_weather"), None)
    if weather_tool:
        res = await weather_tool.run_async(args={"city": "London"}, tool_context=DummyContext())
        print("Weather Result:", res)

if __name__ == "__main__":
    asyncio.run(run_verification())
