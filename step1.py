import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)


response = client.chat.completions.create(
    model="Qwen/Qwen3.8-27B:ovhcloud",
    messages=[
        {"role": "user", "content": "Explain what an AI agent is in one sentence."},
    ],
)

reply = response.choices[0].message.content or ""
print(f"\n🤖 Assistant: {reply.strip()}")
