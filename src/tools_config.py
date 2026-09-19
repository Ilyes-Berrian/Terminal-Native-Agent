TOOL_SCHEMAS = [
    # List Directory Tool
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List the files in a directory; folders should end with /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to list, e.g '.'"}
                },
                "required": ["path"],
            },
        },
    },
    # Read File Tool
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File to read, e.g './file.txt'"}
                },
                "required": ["path"],
            },
        },
    },
    # Write File Tool
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or append content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File to write to, e.g './file.txt'"},
                    "content": {"type": "string", "description": "Full content to write or append to the file."},
                },
                "required": ["path", "content"],
            },
        },
    },
    # Run Command Tool
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Shell command to run and return its output; user approval is required first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command you should run after user approval"}
                },
                "required": ["command"],
            },
        },
    },
]