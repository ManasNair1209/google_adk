from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import preload_memory
from google.genai import types

from logging_callbacks import (
    log_after_tool,
    log_before_model,
    log_before_tool,
    save_session_to_memory,
)

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

async def auto_save_to_memory(callback_context):
    await save_session_to_memory(callback_context, label="auto_memory_agent: STORE")

root_agent = LlmAgent(
    model=Gemini(model="gemini-3.5-flash-lite", retry_options=retry_config),
    name="AutoMemoryAgent",
    instruction="Answer user questions.",
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory,
    before_model_callback=log_before_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)