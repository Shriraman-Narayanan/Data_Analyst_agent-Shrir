import os
import uuid
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from agent.generator import generate_script
from agent.executor import execute_script

load_dotenv()

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

WORKSPACE_DIR = os.path.join(os.getcwd(), "workspaces")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

@app.route("/")
def index():
    """A simple route to confirm the server is running."""
    return "Data Analyst Agent V2 is running."

@app.route("/api/", methods=['POST'])
def api():
    """Main API endpoint to handle data analysis requests."""
    request_id = str(uuid.uuid4())
    request_workspace = os.path.join(WORKSPACE_DIR, request_id)
    os.makedirs(request_workspace, exist_ok=True)
    logger.info(f"Created workspace: {request_workspace}")

    try:
        if 'questions.txt' not in request.files:
            logger.error("Bad Request: 'questions.txt' is missing.")
            return jsonify({"error": "questions.txt is a required file."}), 400

        file_paths = []
        for filename, file_storage in request.files.items():
            file_path = os.path.join(request_workspace, filename)
            file_storage.save(file_path)
            file_paths.append(file_path)
            logger.info(f"Saved file '{filename}' to '{file_path}'")

        with open(os.path.join(request_workspace, 'questions.txt'), 'r') as f:
            prompt = f.read()


        logger.info("Generating analysis script...")
        script_to_execute = generate_script(prompt, request_workspace)
        
        script_path = os.path.join(request_workspace, "analysis_script.py")
        with open(script_path, "w") as f:
            f.write(script_to_execute)
        logger.info("Analysis script generated successfully.")

        logger.info("Executing analysis script...")
        execution_result = execute_script(script_path)
        
        if not execution_result["success"]:
             logger.error(f"Script execution failed: {execution_result['stderr']}")
             return jsonify({"error": "Script execution failed", "details": execution_result['stderr']}), 500
        
        logger.info("Script executed successfully.")

        result_path = os.path.join(request_workspace, "result.json")
        if not os.path.exists(result_path):
            logger.error("Execution succeeded but result.json was not created.")
            return jsonify({"error": "Agent failed to produce result file.", "script_output": execution_result['stdout']}), 500

        with open(result_path, 'r') as f:
            final_result = f.read()
        
        return app.response_class(response=final_result, status=200, mimetype='application/json')

    except Exception as e:
        logger.exception(f"An unexpected error occurred for request {request_id}: {e}")
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
