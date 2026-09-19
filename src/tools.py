import json
import os
import subprocess

def list_dir(path):
    entries = []
    for entry in os.scandir(path):
        entries.append(entry.name + ("/" if entry.is_dir() else ""))
    return "\n".join(entries) or "Empty Directory"


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as error:
        return f"Error When Reading file {path}: {error}"


def write_file(path, content):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote content to {path}"
    except Exception as error:
        return f"Raise Writing Error: {error}"


def run_command(command):
    command_approval = input(f"Run Command: {command} [Y/n]")
    if command_approval.strip().upper() != "Y":
        return "The user declined to this command"
    try:
        command_result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=120
        )
        command_output = (command_result.stdout + command_result.stderr).strip()

        return command_output or f"No output, exit code: {command_result.returncode}"
    except Exception as error:
        return f"Running Command Error: {error}"


TOOL = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}


def run_tool(tool_call):
    args = json.loads(tool_call.function.arguments)
    name = tool_call.function.name

    print(f"\n🛠️  Running Tool: {name}({args})")
    try:
        return str(TOOL[name](**args))
    except Exception as error:
        return f"Running Tool Error: {error} "
