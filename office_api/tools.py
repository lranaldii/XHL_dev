import csv
import matplotlib.pyplot as plt
import os


def extract_text_from_pdf(file_path: str) -> str:
    return f"[PDF text extracted from {file_path}]"


def read_excel(file_path: str):
    return f"[Excel content from {file_path}]"


def read_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return f"[File not found: {file_path}]"

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()



def write_file(file_path: str, content: str):
    # Ensure directory exists
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    # Write content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"[File written to {file_path}]"


def read_csv(file_path: str) -> str:
    """
    Reads a CSV file and returns it as a normalized text table.
    """
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return ""

    # Render as pipe-separated text (LLM-friendly)
    output = []
    for row in rows:
        output.append(" | ".join(cell.strip() for cell in row))

    return "\n".join(output)


def generate_chart(args):
    x = args["x"]
    y = args["y"]
    file_path = args["file_path"]

    title = args.get("title", "Output chart")
    x_label = args.get("x_label", "")
    y_label = args.get("y_label", "")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    plt.figure()
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return {
        "success": True,
        "file": file_path
    }


# Calendar (simulated)

def add_calendar_event(args: dict):
    """
    Simulates adding a calendar event.
    Only uses allowed keys: title, date, time.
    Strips invalid time ranges.
    """
    allowed_keys = ["title", "date", "time"]
    safe_args = {k: args[k] for k in allowed_keys if k in args}

    # Keep only the first time if a range is provided
    if "time" in safe_args and "-" in safe_args["time"]:
        safe_args["time"] = safe_args["time"].split("-")[0]

    print(f"📅 Added event: {safe_args.get('title','')} at {safe_args.get('date','')} {safe_args.get('time','')}")
    return {"success": True, "event": safe_args}
