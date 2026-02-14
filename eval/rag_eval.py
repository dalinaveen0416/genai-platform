import os ,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import json
from backend.rag_pipeline import RAGService

rag = RAGService()


def evaluate_rag():

    with open("eval/rag_eval_data.json") as f:
        data = json.load(f)

    correct = 0

    print("\n====== RAG Evaluation Results ======\n")

    for idx, item in enumerate(data, 1):

        question = item["question"]
        expected_keywords = item["expected_keywords"]

        answer = rag.query(question)

        print(f"Q{idx}: {question}")
        print(f"Answer: {answer}")

        # Count how many expected keywords appear
        matches = sum(
            1 for keyword in expected_keywords
            if keyword.lower() in answer.lower()
        )

        if len(expected_keywords) == 0:
            # Hallucination check
            if "no" in answer.lower() or "not" in answer.lower():
                print("Result: ✅ Correct (No hallucination)")
                correct += 1
            else:
                print("Result: ❌ Wrong (Hallucinated)")
        else:
            if matches == len(expected_keywords):
                print("Result: ✅ Correct")
                correct += 1
            elif matches > 0:
                print("Result: ⚠️ Partial Match")
            else:
                print("Result: ❌ Wrong")

        print("-" * 60)

    total = len(data)
    accuracy = (correct / total) * 100

    print(f"\nFinal Accuracy: {correct}/{total}")
    print(f"Accuracy Percentage: {accuracy:.2f}%")
    print("\n====================================\n")


if __name__ == "__main__":
    evaluate_rag()
