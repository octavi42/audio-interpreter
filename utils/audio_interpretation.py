from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
import json
import os
import requests
from datetime import datetime

load_dotenv()

# Retry decorator with exponential backoff to handle transient failures
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=os.environ['GPT_MODEL']):
    # Define headers for the API request including authorization with OpenAI API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ['OPENAI_API_KEY'],
    }

    # Construct JSON data for the API request
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})

    try:
        # Send a POST request to OpenAI API for chat completions
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        # Handle exceptions related to API requests
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    

def get_interpretation_from_prompt(prompt):

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Define a set of messages for the chat, including system and user roles
    messages = [
        {"role": "system", "content": "you are an advanced prompt interpreter that decodes what someone wants to say"},
        {"role": "user", "content": f'taken this prompt "{prompt}" take out the title, description, action, from date to date, and priority, keep in mind this is the current date {current_date}'},
    ]

    # Define a set of tools for interpretation using the Chat API
    tools = [
        {
            "type": "function",
            "function": {
                "name": "interprete_prompt",
                "description": f"interpret the prompt, the prompt is about a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        # Define parameters for relevance and result
                        "relevance": {
                            "type": "object",
                            "description": "how relevant is the prompt to this function",
                            "properties": {
                                "is_relevant": {
                                    "type": "boolean",
                                    "description": "is the prompt relevant to this function",
                                },
                                "reason": {
                                    "type": "string",
                                    "description": "the reason why you find this prompt relevant or not"
                                },
                                "value": {
                                    "type": "number",
                                    "description": "rate the relevance of the prompt to this function from 0 to 100"
                                },
                            },
                            "required": ["is_relevant"],
                        },
                        # Define result properties including action, action_target, dates, and priority
                        "result": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": f"add a simple title to the task, it should be the action of the prompt",
                                },
                                "description": {
                                    "type": "string",
                                    "description": f"give me the description of the task, summarize from the prompt, include only the essential information",
                                },
                                "action": {
                                    "type": "string",
                                    "description": "give me the action that the user wants to perform, inclidign what the action targets, the result should be given from the prompt, if it is not relevant return null",
                                    "enum": ["create", "read", "update", "delete"]
                                },
                                "action_target": {
                                    "type": "string",
                                    "description": "give me the target of the action, from the prompt, what specific things does the actions target, if it is not relevant return null"
                                },
                                "from_date": {
                                    "type": "string",
                                    "description": "give me the date from which the user wants to perform the action in the format YYYY-MM-DD HH:mm"
                                },
                                "to_date": {
                                    "type": "string",
                                    "description": "give me the date to which the user wants to perform the action in the format YYYY-MM-DD HH:mm"
                                },
                                "priority": {
                                    "type": "string",
                                    "description": "the priority of the action if it is specified, if not specified return null",
                                    "enum": ["low", "medium", "high"]
                                },
                            },
                            "required": ["action", "title", "description"],
                        }
                    },
                    "required": ["relevance", "result"],
                },
            },
        }
    ]

    # Make a chat completion request using the defined messages and tools
    chat_response = chat_completion_request(
        messages, tools=tools, tool_choice={"type": "function", "function": {"name": "interprete_prompt"}},
    )

    # Parse the output from the Chat API response
    output = chat_response.json()["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]

    return json.loads(output)