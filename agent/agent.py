import os
import json
import requests

from groq import Groq

from agent.testbed_loader import load_testbed
from agent.tools_schema import TOOLS


# Config

API_URL = "http://localhost:8002"
MODEL_NAME = "llama-3.1-8b-instant"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Tool Execution

def call_tool(name: str, args: dict):
    """
    Calls one of the available tools.
    Creates folders if necessary.
    """
    print(f"🔧 Tool: {name} | Args: {args}")

    # normalize path for writing
    if "file_path" in args:
        dir_path = os.path.dirname(args["file_path"])
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

    if name == "read_file":
        return requests.post(f"{API_URL}/file/read", json=args).json()

    if name == "write_file":
        return requests.post(f"{API_URL}/file/write", json=args).json()

    if name == "extract_text_from_pdf":
        return requests.post(f"{API_URL}/pdf/extract", json=args).json()

    if name == "extract_text_from_csv":
        return requests.post(f"{API_URL}/csv/extract", json=args).json()

    if name == "read_excel":
        return requests.post(f"{API_URL}/excel/read", json=args).json()

    if name == "generate_chart":
        return requests.post(f"{API_URL}/chart/generate", json=args).json()

    if name == "add_calendar_event":
        return requests.post(f"{API_URL}/calendar/add", json=args).json()

    if name == "send_email":
        return requests.post(f"{API_URL}/email/send", json=args).json()

    if name == "add_todo":
        return requests.post(f"{API_URL}/todo/add", json=args).json()

    return {"error": "Unknown tool"}

def safe_call_tool(name: str, args: dict):
    try:
        result = call_tool(name, args)
        if isinstance(result, dict) and "error" in result:
            return {"success": False, "error": result["error"], "tool": name}
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e), "tool": name}


# Agent Loop

def run_agent(task_json: dict, task_root: str, subtask_id: str, testbed_path: str):
    """
    Execute one XLH/OB task.
    All generated files are saved in the outputs/subtask_id directory.
    """

    task_text = task_json["task"]

    # Load testbed
    testbed_data, real_testbed_path = load_testbed(task_root)
    testbed_files = sorted(testbed_data.keys())
    print(f"📂 Testbed path: {real_testbed_path}")
    print(f"All available testbed files for group {task_root[-7:]}: {testbed_files}")

    # Output directory
    safe_output_dir = os.path.join(task_root, "outputs")
    os.makedirs(safe_output_dir, exist_ok=True)
    print(f"🔒 Output Sandbox: {safe_output_dir}")

    # System prompt
    system_prompt = (
        "You are a STRICT assistant.\n\n"
        "Follow the instructions given below to carefully complete the task using ONLY the allowed tools.\n\n"
        "You MUST complete the task in the minimum number of steps possible.\n"
        "If the task requires you to create a new file, save it in the outputs directory.\n"
        "Writing in the testbed directory is NOT allowed.\n"
        "If required by the task, you can access the testbed files if available."
        "If the task is not in english, you MUST create outputs in the same language as the task."

        "You MUST follow these rules EXACTLY:\n"
        "- You may call ONLY ONE tool per message (MANDATORY).\n"
        "- If you need multiple tool calls, do them in SEPARATE messages.\n"
        "- NEVER output multiple tool calls at once.\n"
        "- NEVER write tool calls as text.\n"
        "- Tool calls MUST be valid JSON only.\n"
        "- After a tool call, WAIT for the tool response before continuing.\n\n"
        "- Never invent tools or file paths.\n"
        "- serialize CSV or ICS content as text before writing.\n"
        "- Do not embed tool calls inside text.\n"

        "ALLOWED TOOLS:\n"
        "1. read_file(file_path: str) → read text files (.txt, .md, .json)\n"
        "2. extract_text_from_csv(file_path: str) → read CSV files (.csv) IMPORTANT!\n"
        "3. read_excel(file_path: str) → read Excel files (.xlsx, .xls)\n"
        "4. extract_text_from_pdf(file_path: str) → read PDF files (.pdf)\n"
        "5. write_file(file_path: str, content: str) → write either text, CSV, or ICS. File_path must match requested path.\n"
        "6. send_email(to: str, subject: str, body: str) -> sends an email. Use ONLY when explicitly asked.\n"
        "7. add_todo(task: str) -> Add a task to the todo list. Use ONLY when explicitly asked.\n"

        "All available files in testbed: \n"
        + "\n".join(testbed_files)
        + "\n\nImportant! From the available files, choose only the ones inherent to the task."
        "You are FORBIDDEN from translating, renaming, or inventing file names.\n"
        "- Even if the task is translated, you MUST use the exact filenames listed below.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task_text}
    ]

    task_lower = task_root.lower()
    MAX_STEPS = 3 if "ob_tasks" in task_lower or "ob_translated" in task_lower else 15

    step = 0
    while step < MAX_STEPS:
        tool_result = None

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if name in ["write_file", "generate_chart"]:
                if "file_path" in args:
                    raw_path = args["file_path"]
                    filename = os.path.basename(raw_path)
                    safe_path = os.path.join(safe_output_dir, filename)
                    print(f"🛡️ Sandbox Rewrite: {raw_path} -> {safe_path}")
                    args["file_path"] = safe_path

            elif name in ["read_file", "extract_text_from_csv", "read_excel", "extract_text_from_pdf"]:
                if "file_path" in args:
                    raw_path = args["file_path"]
                    filename = os.path.basename(raw_path)  # clean relative path

                    # Candidate paths
                    path_in_outputs = os.path.join(safe_output_dir, filename)
                    path_in_testbed = os.path.join(real_testbed_path, filename)

                    # Priority Logic:
                    # 1. If the path was created by the agent (is in outputs), read it.
                    if os.path.exists(path_in_outputs):
                        final_path = path_in_outputs
                        print(f"📖 Reading form OUTPUTS: {filename}")
                    # 2. Otherwise, assume it's an input file (testbed).
                    else:
                        final_path = path_in_testbed
                        print(f"📖 Reading from TESTBED: {filename}")

                    args["file_path"] = final_path

            tool_result = safe_call_tool(name, args)
            step += 1

            # Append tool result to messages for next turn
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

        else:
            # no tool calls → task may be complete
            messages.append(msg)
            break

    # Final status
    if step >= MAX_STEPS:
        print(f"⚠️ Subtask {subtask_id} ended — max steps reached ({step})")
    else:
        print(f"ℹ️ Subtask {subtask_id} ended (steps executed: {step})")