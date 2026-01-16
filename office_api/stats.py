import matplotlib
matplotlib.use("Agg")  # backend headless (perfect for FastAPI)

import matplotlib.pyplot as plt
from .state import tool_metrics
import os

def generate_success_rate_plot():
    tools = []
    rates = []

    for tool, stats in tool_metrics.items():
        total = stats["total"]
        success = stats["success"]
        rate = success / total if total > 0 else 0

        tools.append(tool)
        rates.append(rate * 100)  # percentuale

    plt.figure(figsize=(10, 5))
    plt.bar(tools, rates)
    plt.ylim(0, 100)
    plt.ylabel("Success Rate (%)")
    plt.xlabel("API Tool")
    plt.title("API Tool Success Rate")
    plt.xticks(rotation=30)

  # Save figure
    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "api_tool_success_rate.png")
    plt.savefig(output_path)
    plt.close()

    return output_path