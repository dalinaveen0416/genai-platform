import json
import os ,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from backend.agent_tools import AgentService

agent = AgentService()

def evaluate_agent():

    with open("eval/agent_eval_data.json") as f:
        data = json.load(f)

    correct = 0

    for item in data:
        result = str(agent.run(item["question"]))

        print("Q:", item["question"])
        print("Result:", result)
        print("-" * 50)

        if item["expected"] in result:
            correct += 1

    print(f"\nAgent Accuracy: {correct}/{len(data)}")

if __name__ == "__main__":
    evaluate_agent()
