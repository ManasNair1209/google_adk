# Google ADK — Hands-On Agent Labs

A progressive, day-by-day tour of the **[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)**,
built with `google-adk` **1.20.0**. Each folder is a self-contained, runnable
lab that isolates one concept — from a single-prompt agent to multi-agent
orchestration, tool use, the Model Context Protocol (MCP), sessions, long-term
memory, and advanced workflow patterns.

Every agent folder is an importable package exposing a `root_agent`, so you can
explore any of them interactively with `adk web`.

---

## What's inside

| Day | Folder | Focus | Key ADK surface |
| --- | ------ | ----- | --------------- |
| 1 | `day1_setup` | Minimal single agent | `Agent` |
| 2 | `day2_multi_agent_lab/research_coordinator` | Agents-as-tools coordinator | `AgentTool`, `HttpRetryOptions` |
| 2 | `day2_multi_agent_lab/blog_pipeline` | Sequential writer → reviewer → polisher | `SequentialAgent`, `output_key` |
| 2 | `day2_multi_agent_lab/parallel_research` | Parallel fan-out + synthesis | `ParallelAgent` + `SequentialAgent`, `google_search` |
| 3 | `day3_tools_lab/api_caller_agent` | Custom function tools over a REST API | function tools, FastAPI demo server |
| 3 | `day3_tools_lab/builtin_tools_agent` | Built-in web tools | `google_search`, `url_context` |
| 3 | `day3_tools_lab/db_query_agent` | SQLite-backed tools | function tools, `setup_db.py` |
| 3 | `day3_tools_lab/human_in_loop_agent` | Human approval gate | `LongRunningFunctionTool` |
| 3 | `day3_tools_lab/parallel_analysis_agent` | Parallel text analysis + report | `ParallelAgent` + `SequentialAgent` |
| 4 | `day4_mcpsetup/mcpagent` | MCP server + ADK client | `FastMCP`, `McpToolset` |
| 5 | `day5_session_management/receipee` | Session state & lifecycle callbacks | `InMemorySessionService`, `DatabaseSessionService`, model callbacks |
| 6 | `day6_memory` | Long-term memory | `InMemoryMemoryService`, `preload_memory`, `load_memory` |
| 7 | `day7_advanced_patterns/loop_refiner` | Iterative refinement loop | `LoopAgent`, `exit_loop` |
| 7 | `day7_advanced_patterns/structured_output` | Typed JSON output | `output_schema` (Pydantic) |

## Concepts covered

- **Agents:** `Agent` / `LlmAgent`, instructions, per-agent model selection
- **Orchestration:** the three workflow agents — `SequentialAgent`, `ParallelAgent`, `LoopAgent`
- **Agents as tools:** the `AgentTool` coordinator pattern
- **Shared state:** wiring agents together with `output_key` and `{state}` templating
- **Tools:** custom Python function tools, built-in `google_search` / `url_context`, database tools, human-in-the-loop `LongRunningFunctionTool`, and `exit_loop`
- **MCP:** exposing tools from a `FastMCP` server and consuming them via `McpToolset`
- **Sessions:** `InMemorySessionService` vs `DatabaseSessionService`, plus before/after model callbacks
- **Memory:** ingesting and searching long-term memory; automatic `preload_memory` vs on-demand `load_memory`
- **Structured output:** constraining responses with a Pydantic `output_schema`
- **Resilience:** retry/backoff with `HttpRetryOptions`

---

## Setup

Requires **Python 3.10+** (MCP support needs 3.10 or newer).

```powershell
# 1. Create and activate a virtual environment
python -m venv adk_env
adk_env\Scripts\Activate.ps1      # Windows (PowerShell)
# source adk_env/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
copy .env.example .env            # then edit .env with your API key
```

The `adk_env/` virtual environment, `.env`, and generated `*.db` files are all
gitignored and should never be committed.

## Running the labs

Launch the ADK web UI from the repo root and pick any agent folder:

```powershell
adk web
```

Some labs include standalone scripts or prerequisites:

```powershell
# Day 3 — create the demo database before using db_query_agent
python day3_tools_lab/db_query_agent/setup_db.py

# Day 3 — start the demo REST API (port 8005) for api_caller_agent
python day3_tools_lab/api_caller_agent/dummy_api_server.py

# Day 6 — run a memory walkthrough script directly
python day6_memory/memory_liteagent/agent.py
```

> Day 4's MCP agent launches its `mcp_server.py` automatically over stdio, and
> reuses the Day 3 `company.db`, so run the Day 3 `setup_db.py` first.

---

## Repository layout

```
day1_setup/                     Minimal single agent
day2_multi_agent_lab/           Coordinator, sequential & parallel pipelines
day3_tools_lab/                 Function, built-in, DB, human-in-loop & parallel tools
day4_mcpsetup/                  MCP server and ADK client
day5_session_management/        Session services and callbacks
day6_memory/                    Long-term memory patterns
day7_advanced_patterns/         LoopAgent and structured output
requirements.txt                Pinned dependencies
.env.example                    Credential template
```
