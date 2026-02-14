from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


class AgentService:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an AI agent.

If the user question is a math problem, solve it.
If not, answer normally.

Question: {question}
"""
        )

    def calculate(self, expression: str):
        try:
            return str(eval(expression))
        except:
            return None

    def run(self, query: str):

        # Try to detect math
        if any(op in query for op in ["+", "-", "*", "/", "%"]):
            result = self.calculate(query)
            if result:
                return result

        # Otherwise use LLM
        chain = self.prompt | self.llm
        response = chain.invoke({"question": query})

        return response.content
