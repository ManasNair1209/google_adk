"""Shared, verbose logging callbacks for the Day 6 memory lab.

Three of the four agents import from here so the terminal narrates every
store and every retrieve while you chat with them in adk web.
"""

def _preview(text: str | None, n: int = 100) -> str:
    if not text:
        return "(no text -- e.g. a function call/response part)"
    text = text.replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 3] + "..."

async def log_before_tool(tool, args, tool_context):
    """Fires right before ANY tool call (load_memory, save_to_memory, ...)."""
    print(f"\n[TOOL CALL] {tool.name}({args})")
    return None

async def log_after_tool(tool, args, tool_context, tool_response):
    """Fires right after a tool returns -- shows what came back."""
    print(f"[TOOL RESULT] {tool.name} -> {_preview(str(tool_response), 220)}")
    return None

async def log_before_model(callback_context, llm_request):
    """Fires right before the request goes to Gemini.

    preload_memory injects a <PAST_CONVERSATIONS> block into the prompt BEFORE
    this callback runs. The block is placed just before the latest user turn,
    NOT appended at the very end -- so every content is checked, not just the
    last one.
    """
    for content in llm_request.contents:
        if not content.parts:
            continue
        text = content.parts[0].text
        if text and "<PAST_CONVERSATIONS>" in text:
            print("\n[MEMORY PRELOADED] preload_memory silently added this to the prompt:")
            print("  " + _preview(text, 250))
    return None

async def save_session_to_memory(callback_context, label: str):
    """The actual store: copies the current session into long-term memory."""
    invocation_context = callback_context._invocation_context
    session = invocation_context.session
    print(f"\n[{label}] Saving session '{session.id}' to memory ({len(session.events)} event(s) total):")
    for event in session.events[-2:]:
        text = event.content.parts[0].text if event.content and event.content.parts else "(empty)"
        print(f"  {event.content.role}: {_preview(text)}")
    await invocation_context.memory_service.add_session_to_memory(session)
    print(f"[{label}] -> stored. This is now retrievable from ANY future session for this user.")