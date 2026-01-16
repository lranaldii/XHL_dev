import os
import sys
import json

# allows to import modules from the project
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from agent.agent import run_agent
from XLH_utilities.find_subtasks import find_subtasks

def get_canonical_testbed(task_dir: str, is_officebench: bool):
    """
    For XLH: XLH_translated/it/1-2 -> XLH_tasks/en/1-2/testbed
    For OB: OB_tasks/... -> OB_tasks/.../testbed (if exists)
    """
    parts = task_dir.replace("\\", "/").split("/")

    if is_officebench:
        # OB testbed path
        testbed_path = os.path.join(task_dir, "testbed")
        if os.path.exists(testbed_path):
            return testbed_path
        else:
            return None
    else:
        # XLH testbed path
        if "XLH_translated" in parts:
            idx = parts.index("XLH_translated")
            task_id = parts[idx + 2]
            return os.path.join("XLH_tasks", "en", task_id, "testbed")
        else:
            return None

def evaluate_directory(tasks_dir: str):
    print(f"\n📂 Evaluate directory: {tasks_dir}")

    tasks_dir_norm = tasks_dir.replace("\\", "/").lower()

    is_officebench = "OB" in tasks_dir_norm

    if not os.path.isdir(tasks_dir):
        print("❌ Directory does not exist")
        return

    subtasks = find_subtasks(tasks_dir)
    print(f"🔎 Subtasks found: {len(subtasks)}")

    if not subtasks:
        print("⚠️ No subtasks found")
        return

    for task_root, subtask_path in subtasks:
        rel_path = os.path.relpath(subtask_path, tasks_dir)
        task_id = os.path.basename(task_root)
        subtask_id = os.path.splitext(os.path.basename(subtask_path))[0]

        print(f"\n▶ Task {task_id} | Subtask {subtask_id}")
        print(f"   File: {rel_path}")

        try:
            with open(subtask_path, "r", encoding="utf-8") as f:
                task_json = json.load(f)

            canonical_testbed = get_canonical_testbed(task_root, is_officebench)

            # Run agent
            run_agent(
                task_json=task_json,
                task_root=task_root,
                subtask_id=subtask_id,
                testbed_path=canonical_testbed
            )

        except Exception as e:
            print(f"❌ Errore in {rel_path}")
            print(f"   {type(e).__name__}: {e}")


# =========================
# CLI
# =========================
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Correct usage:")
        print("   python evaluator/run_groq_evaluator.py <directory_tasks>")
        sys.exit(1)

    tasks_directory = sys.argv[1]
    evaluate_directory(tasks_directory)
