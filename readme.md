# Investor CRM

A full-stack Investor CRM built with React (Vite), FastAPI (Python), SQLite, and local AI (Ollama).

## Prerequisites
- Node.js & npm
- Python 3
- [Ollama](https://ollama.com/) (running locally)

## Running the Project

You will need to open **two separate terminal windows** to run the frontend and backend simultaneously.

### 1. Start the Backend API (Terminal 1)
The backend uses FastAPI and handles the SQLite database and AI service routing. Because your Python environment (`venv`) is in the root project folder, you must activate it before going into the backend!

```bash
cd /Users/vanshagarwal/investor-crm         # Make sure you are in the main project folder
source venv/bin/activate                    # Activate the python environment
cd backend                                  # Go into the backend folder
uvicorn app.main:app --reload               # Start the server
```
*The backend will run on `http://127.0.0.1:8000`*

### 2. Start the Frontend Application (Terminal 2)
The frontend uses Vite and React.

```bash
cd /Users/vanshagarwal/investor-crm/frontend
npm install   # Only needed the first time
npm run dev
```
*The frontend will run on `http://localhost:5174`*

### 3. Ensure Local AI is Running
For the AI Assistant (Email Generation, Summaries, Next Commands) to work, make sure Ollama is active on your machine.

If you haven't pulled the configured model yet, run:
```bash
ollama pull phi3
```
*(Note: As long as the Ollama app is open/running in the background on your Mac, the API at `localhost:11434` will actively respond to the CRM's requests).*
