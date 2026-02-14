import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

VECTOR_PATH = "vectorstore/faiss_index"

rag_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""You are a helpful assistant that answers questions based on retrieved document chunks.

Use the following retrieved information to answer the question.
If you don't know the answer, say you don't know.
if the retrieved information is not relevant, ignore it and say you don't know.
if the questionis asking specifit one like collage name cgpa link etc then answer in the shortest way possible and do not include any extra information.


Question: {question}
Retrieved Information:
{context}
"""
)

class RAGService:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.2
        )

        self.qa_chain = None

    def ingest(self, file_path):

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        docs = [doc for doc in docs if doc.page_content.strip()]


        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local(VECTOR_PATH)

        return "Document indexed successfully."

    def load_chain(self):

        vectorstore = FAISS.load_local(
            VECTOR_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
        , chain_type_kwargs={"prompt": rag_prompt}
        )

    def query(self, question):

        if not self.qa_chain:
            self.load_chain()

        response = self.qa_chain.invoke({"query": question})
        return response["result"]
