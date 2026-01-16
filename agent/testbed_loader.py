import os
import csv
import json

def load_testbed(task_dir: str):
    """
    Load testbed for a task.
    If the task is translated, fallback to the English version in XLH_tasks/en/<task_id>
    """

    task_dir = os.path.abspath(task_dir).replace("\\", "/")
    parts = task_dir.split("/")

    # Default testbed path in the current task folder
    testbed_path = os.path.join(task_dir, "testbed")

    # Fallback for translated tasks
    if "XLH_translated" in parts:
            try:
                # Find the index to correctly navigate up
                idx = parts.index("XLH_translated")
                project_root = "/".join(parts[:idx])
                task_id = parts[-1] 
                testbed_path = os.path.join(project_root, "XLH_tasks", "en", task_id, "testbed")
            except ValueError:
                pass

    if "OB_translated" in parts:
            try:
                idx = parts.index("OB_translated")
                project_root = "/".join(parts[:idx])
                task_id = parts[-1]
                testbed_path = os.path.join(project_root, "OB_tasks", "en", task_id, "testbed")
            except ValueError:
                pass

    if not os.path.isdir(testbed_path):
            print(f"❌ No testbed folder found at {testbed_path}")
            return {}, testbed_path  # Return path even if empty
        
    data = {}

    for root, dirs, files in os.walk(testbed_path):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, testbed_path)

            if file.endswith(".csv"):
                with open(path, encoding="utf-8", errors="replace") as f:
                    data[rel_path] = list(csv.DictReader(f))

            elif file.endswith(".json"):
                with open(path, encoding="utf-8", errors="replace") as f:
                    data[rel_path] = json.load(f)

            elif file.endswith(".txt") or file.endswith(".eml"):
                with open(path, encoding="utf-8", errors="replace") as f:
                    data[rel_path] = f.read().strip()

            elif file.endswith(".xlsx"):
                data[rel_path] = f"[Excel file: {rel_path}]"

            elif file.endswith(".pdf"):
                data[rel_path] = f"[PDF file: {rel_path}]"

            elif file.endswith(".ics"):
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    data[rel_path] = f.read()

            else:
                data[rel_path] = f"[Unknown file type: {rel_path}]"

    return data, testbed_path