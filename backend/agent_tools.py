from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

class AgentService:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an AI agent.

If the user question is a math problem, solve it.
if the question is about simple intrest rate is alsways desimal if it 2 rupees means rate =2 if it 3 rate =3 dont converrt to decimal
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
