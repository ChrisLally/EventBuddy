# from typing import Dict, List, Union

# from google.cloud import aiplatform
# from google.protobuf import json_format
# from google.protobuf.struct_pb2 import Value

import os, vertexai
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="google-service-account-key.json"

from vertexai.language_models import ChatModel, InputOutputTextPair, ChatSession, ChatMessage

def generate_prediction(
    prompt: str,
    message_history: list,
    project_id: str,
    location: str,
) -> str:
    """Streaming Chat Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    chat_model = ChatModel.from_pretrained("chat-bison-32k") #text-bison

    parameters = {
        "temperature": 0.8,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 400,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 1,  # A top_k of 1 means the selected token is the most probable among all tokens.

        }
    messages = []
    print("got HISTORY LEN",len(message_history),message_history)
    for message in message_history:
        if message["is_user"]:
            messages.append(
                ChatMessage(author="user", content=message["message"])
            )
        else:
            messages.append(
                ChatMessage(author="model", content=message["message"])
            )
    print("got all MESSAGES LEN",len(messages))

    chat = chat_model.start_chat(
        context="""You are EventBuddy!""",
        message_history=messages,
        examples=[
            InputOutputTextPair(
                input_text="My name is Chris",
                output_text="""Response""",
            ),
        ],
    )

    print('sending prompt',prompt)
    response = chat.send_message(
        message=prompt, **parameters
    )
    print(response.text)
    return response.text



def generateResponse(prompt,message_history):
    response=generate_prediction(
    prompt=prompt,
    message_history=message_history,
    project_id="000",
    location="us-central1",
    )
    return response

#generateResponse("For sure! Can you help me?")