import os
import logging
import google.generativeai as genai
from .prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

try:
    if "GENAI_API_KEY" not in os.environ:
        raise ValueError("GENAI_API_KEY environment variable not set.")
    genai.configure(api_key=os.environ["GENAI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    logger.error(f"Failed to configure Generative AI model: {e}")
    model = None

def generate_script(prompt: str, workspace_dir: str) -> str:
    if model is None:
        raise ConnectionError("Generative AI model is not configured. Check API key and configuration.")

    try:
        files_in_workspace = os.listdir(workspace_dir)
    except FileNotFoundError:
        files_in_workspace = []
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Request:\n---\n{prompt}\n---\n\nAvailable Files: {files_in_workspace}"

    for attempt in range(3):
        try:
            response = model.generate_content(full_prompt)
            script = response.text.strip()
            if script.startswith("```python"):
                script = script[9:]
            if script.endswith("```"):
                script = script[:-3]
            return script.strip()
        except Exception as e:
            logger.warning(f"LLM generation failed (attempt {attempt+1}/{3}): {e}")
            if attempt == 2:
                raise ConnectionError("LLM failed to respond after multiple attempts.") from e
    
    raise ConnectionError("LLM failed to generate a script.")
