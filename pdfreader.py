

import os
from dotenv import load_dotenv
import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Set the API key for OpenAI
openai.api_key = openai_api_key

# Define the relative file path
file_path = os.path.join("data", "Allen B. Downey - Think Python, 2nd Edition_ How to Think Like a Computer Scientist-O'Reilly Media (2015).pdf")

# Load the PDF using PyPDFLoader
loader = PyPDFLoader(file_path)
docs = loader.load()

# Print the number of documents loaded
print(f"Number of documents loaded: {len(docs)}")

# Convert documents to text
pdf_text = "\n".join([doc.page_content for doc in docs])

# Create embeddings for the documents
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create a vector store using FAISS
vector_store = FAISS.from_texts([doc.page_content for doc in docs], embeddings)

# Create a RetrievalQA chain
retriever = vector_store.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm="gpt-3.5-turbo", retriever=retriever, return_source_documents=True)

def query_pdf(prompt):
    response = qa_chain({"query": prompt})
    return response["result"], response["source_documents"]

# Example query
user_prompt = "What is the main topic discussed in the PDF?"
result, source_docs = query_pdf(user_prompt)
print(f"Query result: {result}")

# Print source documents
for i, doc in enumerate(source_docs):
    print(f"Source document {i+1}: {doc.page_content[:500]}...")

# You can make additional queries as needed
another_prompt = "List the key points mentioned in the PDF."
another_result, source_docs = query_pdf(another_prompt)
print(f"Another query result: {another_result}")
