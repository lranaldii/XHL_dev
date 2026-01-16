import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .state import xlh_tool_metrics
import os

def generate_xlh_tool_plot():
    tools = []
    rates = []

    for tool, stats in xlh_tool_metrics.items():
        total = stats["total"]
        success = stats["success"]
        rate = success / total if total > 0 else 0
        tools.append(tool)
        rates.append(rate * 100)  # percentuale

    plt.figure(figsize=(10, 5))
    plt.bar(tools, rates, color="blue")
    plt.ylim(0, 100)
    plt.ylabel("Success Rate (%)")
    plt.xlabel("XLH Tool")
    plt.title("XLH Tool Success Rate")
    plt.xticks(rotation=30)
    plt.tight_layout()

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "xlh_tool_success_rate.png")
    plt.savefig(output_path)
    plt.close()

    return output_path
