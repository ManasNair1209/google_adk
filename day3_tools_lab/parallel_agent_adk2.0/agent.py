from typing import Any
from google.adk import Event
from google.adk import Workflow
from google.adk.workflow import JoinNode




def make_uppercase(node_input: str):
  return node_input.upper()




def count_characters(node_input: str):
  return len(node_input)




def reverse_string(node_input: str):
  return node_input[::-1]




join_node = JoinNode(name="join_for_results")




async def aggregate(node_input: dict[str, Any]):
  yield Event(
      message=(
          f"Uppercase: {node_input['make_uppercase']}\n\n"
          f"Character Count: {node_input['count_characters']}\n\n"
          f"Reversed: {node_input['reverse_string']}\n\n"
      ),
  )




root_agent = Workflow(
    name="root_agent",
    edges=[(
        "START",
        (make_uppercase, count_characters, reverse_string),
        join_node,
        aggregate,
    )],
)
