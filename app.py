"""Legacy entry point - redirects to app.main.

This file is kept for backward compatibility.
Use 'streamlit run app/main.py' or 'python run.py' instead.
"""

import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])