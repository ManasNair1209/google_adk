from google.adk import Agent, Workflow, Event

draft_agent = Agent(
    name="DraftWriterAgent",
    model="gemini-3.5-flash-lite",
    instruction="Write short, professional 3-sentence email drafts. Output ONLY the subject and body.",
)

def human_review(node_input: str) -> Event:
    """Pauses workflow for terminal human approval."""
    print("\n" + "=" * 50)
    print("PROPOSED AI DRAFT FOR REVIEW:")
    print("=" * 50)
    print(node_input)
    print("=" * 50)

    decision = input("\nApprove draft? (yes / no): ").strip().lower()
    if decision in ("yes", "y"):
        return Event(route=["APPROVED"])
    reason = input("Reason for rejection: ").strip()
    return Event(route=["REJECTED"], message=reason or "Draft rejected.")

def send_email(node_input: str) -> Event:
    print("\n[SUCCESS] Email approved and sent successfully!\n")
    return Event(message="Email successfully approved and dispatched.")

def request_revision(node_input: str) -> Event:
    print("\n[REJECTED] Draft returned for revision.\n")
    return Event(message="Draft rejected. Please re-submit with revised context.")

root_agent = Workflow(
    name="HumanInLoopWorkflow",
    edges=[
        ("START", draft_agent, human_review),
        (human_review, {
            "APPROVED": send_email,
            "REJECTED": request_revision,
        }),
    ],
)



