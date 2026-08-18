import sys
from pathlib import Path

# Allow running this file directly (python app.py) while keeping package-relative imports.
# When executed as a script, set up the parent directory on sys.path and set __package__
# so relative imports (`from . import ...`) continue to work.
if __name__ == "__main__" and __package__ is None:
    parent = Path(__file__).resolve().parent
    sys.path.insert(0, str(parent.parent))
    __package__ = parent.name

import tkinter as tk
from . import database
from . import login


def main():
    # Create database and tables (only if they do not already exist)
    database.create_tables()

    # Start application
    root = tk.Tk()
    login.launch_login(root)
    root.mainloop()


if __name__ == "__main__":
    main()
