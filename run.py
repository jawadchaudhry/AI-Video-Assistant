"""Streamlit application entry point."""

import os
import sys

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

# Add to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Set PYTHONPATH for subprocess
env = os.environ.copy()
env["PYTHONPATH"] = PROJECT_ROOT

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    import subprocess
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app/main.py"],
        env=env,
        cwd=PROJECT_ROOT,
    )