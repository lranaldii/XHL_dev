import os
import sys

# permette di importare agent/agent.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.testbed_loader import load_testbed

def check_testbed(subtask_path: str):
    # Construct testbed path inside the subtask block
    testbed_path = os.path.join(subtask_path, "testbed")

    if not os.path.exists(testbed_path):
        print(f"❌ No testbed folder found at {testbed_path}")
        return []

    testbed_data = load_testbed(testbed_path)
    testbed_files = sorted(testbed_data.keys())

    if testbed_files:
        print("Files loaded from testbed:")
        for f in testbed_files:
            print(f" - {f}")
    else:
        print("❌ Testbed is empty or no supported files found.")

    return testbed_files

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 evaluator/check_testbed.py <subtask_block_path>")
        sys.exit(1)

    subtask_block = sys.argv[1]
    check_testbed(subtask_block)
