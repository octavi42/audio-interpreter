from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
import json
import os
import requests


load_dotenv()

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-4-1106-preview"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ['OPENAI_API_KEY'],
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    

def get_interpretation_from_prompt(prompt):
    messages = [
        {"role": "system", "content": "you are an advanced prompt interpreter that decodes what someone wants to say"},
        {"role": "user", "content": f'taken this command "{prompt}" take out the action, from date to date, and priority'},
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "interprete_prompt",
                "description": "interpret the prompt, the prompt should be an action for a database",
                "parameters": {
                    "type": "object",
                    "properties": {
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
                        "result": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "description": "give me the action that the user wants to perform, inclidign what the action targets, the result should be given from the prompt, if it is not relevant return null",
                                    "enum": ["create", "read", "update", "delete"]
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
                            "required": ["action"],
                        }
                    },
                "required": ["relevance", "result"],
                },
            },
        }
    ]

    chat_response = chat_completion_request(
        messages, tools=tools, tool_choice={"type": "function", "function": {"name": "interprete_prompt"}},
    )

    output = chat_response.json()["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]

    return json.loads(output)