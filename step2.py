import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

context_mem = []
while True:
    user_input = input("\n👨 User: ")

    # Check for quit the chat
    if user_input.strip().lower() in ("exit", "quit"):
        break

    # Update the context window
    context_mem.append({"role": "user", "content": user_input})

    # Generate a response from the model
    response = client.chat.completions.create(
        model="Qwen/Qwen3.8-27B:ovhcloud",
        messages=context_mem,
    )
    # Get the assistant's reply and update the context
    reply = response.choices[0].message
    context_mem.append({"role": "assistant", "content": str(reply)})

    print(f"\n🤖 Assistant: {str(reply.content).strip()}")
