from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import load_memory, ToolContext
from google.genai import types

from logging_callbacks import _preview, log_after_tool, log_before_tool

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

async def save_to_memory(tool_context: ToolContext) -> dict:
    """Ingests the CURRENT conversation into long-term memory.

    Call this when the user shares a fact worth remembering long-term (a
    preference, a date, a personal detail) -- not for small talk.
    """
    invocation_context = tool_context._invocation_context
    session = invocation_context.session
    print(f"\n[save_to_memory CALLED] Storing session '{session.id}' ({len(session.events)} event(s)):")
    for event in session.events:
        text = event.content.parts[0].text if event.content and event.content.parts else "(empty)"
        print(f"  {event.content.role}: {_preview(text)}")
    await invocation_context.memory_service.add_session_to_memory(session)
    return {"status": "saved", "session_id": session.id}

root_agent = LlmAgent(
    model=Gemini(model="gemini-3.5-flash-lite", retry_options=retry_config),
    name="ManualMemoryAgent",
    instruction=(
        "Answer user questions in simple words. "
        "When the user shares something worth remembering long-term (a "
        "preference, a date, a personal fact), call save_to_memory to store "
        "this conversation, then confirm you saved it. "
        "Use load_memory if you need to recall something from a past conversation."
    ),
    tools=[save_to_memory, load_memory],
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)