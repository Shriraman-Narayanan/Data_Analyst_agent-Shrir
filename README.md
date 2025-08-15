Data Analyst Agent 
This is a robust, AI-powered data analyst agent designed for reliability and speed. It uses a powerful one-shot script generation model to analyze data and produce results, ensuring it passes complex evaluations.

This version is an overhaul of a previous ReAct-style agent, built to be simpler, faster, and more dependable.

🚀 Features
Reliable Script Generation: Instead of a complex, multi-step reasoning process, the agent generates a single, complete Python script to solve the entire user request in one go. This massively reduces the points of failure.

High Speed: The single-call architecture is significantly faster than conversational agents, with most requests completing in 15-30 seconds.

One-Shot Prompting: The agent is guided by a highly-detailed system prompt that instructs it to act as a senior data scientist, ensuring it follows all requirements for data analysis, plotting, and output formatting.

Secure & Isolated Execution: Each generated script is run in a secure subprocess within a dedicated workspace for the request.

Deployment Ready: Comes pre-configured with a Dockerfile and render.yaml for easy, one-click deployment to Render.

⚙️ Project Structure
/data-analyst-agent-v2/
|
├── agent/
│   ├── __init__.py
│   ├── generator.py        # Brain: Generates the Python script.
│   ├── executor.py         # Hands: Executes the script.
│   └── prompts.py          # Soul: Contains the core instructions for the AI.
|
├── workspaces/             # Auto-created for temporary request files.
|
├── app.py                  # The main Flask web server and API endpoint.
├── requirements.txt        # List of all Python libraries needed.
├── Dockerfile              # Blueprint for building the deployment container.
├── render.yaml             # Specific instructions for deploying on Render.
└── .gitignore              # Tells Git which files to ignore.

🛠️ Local Setup
Prerequisites
Python 3.9+

Pip & Git

Installation
Clone the repository:

git clone <your-repo-url>
cd data-analyst-agent-v2

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Set up environment variables:
Create a file named .env in the project root and add your Google API key:

GENAI_API_KEY="your_google_ai_studio_api_key"

Run the application:

gunicorn app:app

The server will be running at http://127.0.0.1:8000.

☁️ Deployment to Render
Push your project to a new public GitHub repository.

Go to the Render Dashboard and create a New Web Service.

Connect your GitHub repository.

Render will automatically detect the render.yaml file. Give your service a name.

Go to the Environment tab and add a new Environment Variable:

Key: GENAI_API_KEY

Value: Paste your Google API key.

Click Create Web Service. Render will build and deploy your agent.

🧪 API Usage
Send a POST request to the /api/ endpoint with multipart/form-data.

Required file: questions.txt (contains the prompt)

Optional files: Any data files needed for the analysis (e.g., sample-sales.csv).

cURL Example:
curl -X POST https://your-render-app-url/api/ \
     -F "questions.txt=@path/to/questions.txt" \
     -F "sample-sales.csv=@path/to/sample-sales.csv"
