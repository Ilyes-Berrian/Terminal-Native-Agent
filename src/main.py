import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import run_tool
from tools_config import TOOL_SCHEMAS

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

SYSTEM_PROMPT = """You are a coding agent running in the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from."""


def run_agent(context_win):
    while True:
        response = client.chat.completions.create(
            model=os.environ["MODEL"],
            messages=context_win,
            tools=TOOL_SCHEMAS,
        )
        message = response.choices[0].message
        context_win.append(message)

        if not message.tool_calls:
            return message

        for tool_call in message.tool_calls:
            output = run_tool(tool_call)
            context_win.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": output,
                }
            )


def main():
    context_win = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("=" * 15 + "Omega-0.1.0" + "=" * 15)
    while True:
        user_input = input("\n👨 User: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages = {
            "role": "user",
            "content": user_input,
        }
        context_win.append(messages)

        reply = run_agent(context_win)
        messages = {
            "role": "assistant",
            "content": str(reply),
        }
        context_win.append(messages)

        print(f"\n 🤖 Agent: {str(reply.content).strip()}")


if __name__ == "__main__":
    main()
