"""
main.py — Entry point của ứng dụng.

Khởi tạo TransportationApp và chạy vòng lặp giao diện.
"""

import sys
import os

# Thêm thư mục gốc vào sys.path để import src được
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.app import TransportationApp


def main() -> None:
    """Điểm vào chính của chương trình."""
    app = TransportationApp()
    app.run()


if __name__ == "__main__":
    main()
