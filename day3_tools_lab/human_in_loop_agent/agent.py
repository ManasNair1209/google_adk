from google.adk.agents import Agent
from google.adk.tools import LongRunningFunctionTool, ToolContext

# Human-in-the-loop in ADK is modelled with a LONG-RUNNING tool. Instead of
# blocking on input(), the tool returns a "pending" ticket immediately; the
# surrounding application (or a human) later sends the decision back to the
# agent as a function response. This is the pattern that works inside `adk web`.

def request_email_approval(
    recipient: str, subject: str, body: str, tool_context: ToolContext
) -> dict:
    """Submits a drafted email for human approval before it is sent.

    Args:
        recipient: Who the email is addressed to.
        subject: The email subject line.
        body: The drafted email body.
    """
    return {
        "status": "pending",
        "ticket_id": "email-approval-001",
        "recipient": recipient,
        "subject": subject,
        "message": "Draft submitted for human review. Awaiting approval.",
    }

approval_tool = LongRunningFunctionTool(func=request_email_approval)

root_agent = Agent(
    name="HumanInLoopAgent",
    model="gemini-3.5-flash-lite",
    instruction="""You are an assistant that drafts and sends emails, but a human
must approve every email before it goes out.

1. When the user asks you to send an email, write a short, professional draft.
2. Call request_email_approval with the recipient, subject, and body.
3. The tool returns status 'pending' -- tell the user the email is awaiting
   human approval and share the ticket id. Do NOT claim it has been sent.
4. If a later message says the ticket was APPROVED, confirm the email was sent.
   If it was REJECTED, apologise and offer to revise the draft.""",
    tools=[approval_tool],
)



