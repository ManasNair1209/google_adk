from google.adk.agents import LlmAgent
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from typing import Optional
from google.genai import types

# --- Define the after_model_callback function ---
def append_disclaimer_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print(f"[Callback] Running after model call for agent: {callback_context.agent_name}")

    # The text we want to append
    disclaimer = "\n\n[Disclaimer: This response was processed by an AI agent.]"

    # Check if the response contains text content we can modify
    if llm_response.content and llm_response.content.parts:
        # Get the original text from the last part of the response
        original_text = llm_response.content.parts[-1].text or ""
        
        # Append our disclaimer
        llm_response.content.parts[-1].text = original_text + disclaimer
        print("[Callback] Successfully appended disclaimer.")
        
        # Return the modified LlmResponse to override the original one
        return llm_response

    # If there was no text to modify, return None to allow the default response to proceed
    return None

# --- Register it during Agent creation ---
my_agent = LlmAgent(
    name="SafeResponseAgent",
    model="gemini-3.5-flash", 
    instruction="You are a helpful assistant.",
    after_model_callback=append_disclaimer_callback # Assign the callback here
)

