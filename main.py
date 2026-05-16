"""Legacy CLI entry point - redirects to src.cli.

This file is kept for backward compatibility.
Use 'python -m src.cli.main --interactive' instead.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    from src.cli.main import main
    sys.argv.append("--interactive")
    main()