# LLM-PDF-Analyzer
Analysing Pdf documents with RAG fine-tuned LLM 

# Prerequisites
- Ensure you have the following installed on your system:

- Python 3.8+
- Node.js
- pip
- virtualenv

# Set Up the Python Environment

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

#  Install Python Dependencies
```
pip install -r requirements.txt
```
# Set Up Environment Variables
- Create a .env file in the project root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key
```

#  Install Node.js Dependencies
- Install the required Node.js packages:
```
npm install
```
# Run the Flask API 

to create run-flask.bat in the folder structure, in windows, run code below in the command window
```
@echo off
call venv\Scripts\activate
set FLASK_APP=src\app.py
set FLASK_ENV=development
flask run
```
- Run the Flask API using the provided shell script:
```
run-flask.bat
```
- Build and Run the Docker Container
```
docker-compose up
```

