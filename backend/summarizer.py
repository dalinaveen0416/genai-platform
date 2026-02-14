from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


class Summarizer:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            "Summarize the following text clearly:\n\n{text}"
        )

    def summarize(self, text):

        chain = self.prompt | self.llm

        response = chain.invoke({"text": text})

        return response.content

print("Summarizer file loaded")