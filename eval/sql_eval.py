import os ,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
from backend.sql_chat import SQLChat

sql = SQLChat()

def evaluate_sql():

    with open("eval/sql_eval_data.json") as f:
        data = json.load(f)

    correct = 0

    for item in data:
        result = str(sql.ask(item["question"]))

        print("Q:", item["question"])
        print("Result:", result)
        print("-" * 50)

        if item["expected"].lower() in result.lower():
            correct += 1

    print(f"\nSQL Accuracy: {correct}/{len(data)}")

if __name__ == "__main__":
    evaluate_sql()
