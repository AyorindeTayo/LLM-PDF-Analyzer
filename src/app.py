from flask import Flask, request, jsonify, render_template
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

app = Flask(__name__)

# Define the relative file path

file_path = os.path.join("data", "Allen B. Downey - Think Python, 2nd Edition_ How to Think Like a Computer Scientist-O'Reilly Media (2015).pdf")
# Load the PDF using PyPDFLoader
loader = PyPDFLoader(file_path)
docs = loader.load()

# Create embeddings for the documents
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create a vector store using FAISS
vector_store = FAISS.from_texts([doc.page_content for doc in docs], embeddings)

# Create a RetrievalQA chain
retriever = vector_store.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm="gpt-3.5-turbo", retriever=retriever, return_source_documents=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_pdf():
    data = request.json
    user_prompt = data.get('prompt', '')
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = qa_chain({"query": user_prompt})
    result = response["result"]
    source_docs = [doc.page_content for doc in response["source_documents"]]
    return jsonify({"result": result, "source_docs": source_docs})

if __name__ == '__main__':
    app.run(debug=True)
