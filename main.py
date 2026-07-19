"""
main.py - Entry point cua ung dung.

Khoi tao cua so Tkinter, tao TransportationApp va chay vong lap giao dien.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from src.gui.app import TransportationApp


def main() -> None:
    root = tk.Tk()
    app = TransportationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()