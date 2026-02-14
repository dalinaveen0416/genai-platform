from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from backend.create_db import create_sample_database
import os


class SQLChat:

    def __init__(self):
        # Ensure database exists before connecting
        db_path = create_sample_database()
        
        # Connect to SQLite database with absolute path
        abs_path = os.path.abspath(db_path)
        self.db = SQLDatabase.from_uri(f"sqlite:///{abs_path}")

        # Groq LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

        # SQL generation prompt
        self.prompt = PromptTemplate(
            input_variables=["question"],
            template="""You are an expert SQLite assistant. Given the following question about a database, generate ONLY a valid SQL query. Do not include any explanation or comments.

Question: {question}

SQL Query:"""
        )

    def ask(self, question):
        try:
            # Generate SQL query using LLM
            chain = self.prompt | self.llm
            response = chain.invoke({"question": question})
            
            # Extract SQL query
            sql_query = response.content.strip()
            
            # Execute the query
            result = self.db.run(sql_query)
            
            if result:
                return result
            return "Query executed successfully."
        except Exception as e:
            return f"Error: {str(e)}"
