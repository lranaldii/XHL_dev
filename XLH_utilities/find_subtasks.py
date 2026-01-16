import os

def find_subtasks(root_dir: str):
    """
    Trova tutte le subtasks XLH valide.

    Ritorna una lista di tuple:
    (task_root, subtask_json_path)
    """
    subtasks = []

    for root, dirs, files in os.walk(root_dir):
        if os.path.basename(root) == "subtasks":
            task_root = os.path.dirname(root)

            for file in files:
                if file.endswith(".json"):
                    subtasks.append(
                        (task_root, os.path.join(root, file))
                    )

    return sorted(subtasks)
