import subprocess
import os

def execute_script(script_path: str) -> dict:
    """
    Executes a Python script in a subprocess and captures its output.

    Args:
        script_path (str): The absolute path to the Python script to execute.

    Returns:
        dict: A dictionary containing success status, stdout, and stderr.
    """
    if not os.path.exists(script_path):
        return {"success": False, "stdout": "", "stderr": "Script file not found."}

    # The working directory should be the directory containing the script
    working_dir = os.path.dirname(script_path)

    try:
        process = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=150  # 2.5 minute timeout
        )

        if process.returncode == 0:
            return {"success": True, "stdout": process.stdout, "stderr": process.stderr}
        else:
            return {"success": False, "stdout": process.stdout, "stderr": process.stderr}

    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Error: Script execution timed out."}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": f"An unexpected error occurred during execution: {e}"}
