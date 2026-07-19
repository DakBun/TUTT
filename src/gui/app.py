"""
app.py — Cửa sổ chính của ứng dụng trực quan hóa bài toán vận tải.

TransportationApp tạo cửa sổ Tkinter với:
  - Frame trái: chứa MatrixGrid để hiển thị ma trận.
  - Frame phải: chứa các nút điều khiển (Next Step, Reset).
"""

import tkinter as tk
from tkinter import ttk

from src.gui.canvas import MatrixGrid


class TransportationApp:
    """
    Ứng dụng desktop trực quan hóa giải bài toán vận tải.
    """

    def __init__(self) -> None:
        """Khởi tạo cửa sổ chính và các thành phần giao diện."""
        self.root = tk.Tk()
        self.root.title("Bài toán vận tải — Transportation Problem")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # ----- Frame bên trái: ma trận -----
        self.left_frame = ttk.Frame(self.root, padding=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.matrix_grid = MatrixGrid(self.left_frame)
        self.matrix_grid.pack(fill=tk.BOTH, expand=True)

        # ----- Frame bên phải: điều khiển -----
        self.right_frame = ttk.Frame(self.root, padding=10, width=200)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)

        btn_next = ttk.Button(
            self.right_frame,
            text="Next Step",
            command=self._on_next_step,
        )
        btn_next.pack(pady=10, fill=tk.X)

        btn_reset = ttk.Button(
            self.right_frame,
            text="Reset",
            command=self._on_reset,
        )
        btn_reset.pack(pady=10, fill=tk.X)

        btn_exit = ttk.Button(
            self.right_frame,
            text="Thoát",
            command=self.root.quit,
        )
        btn_exit.pack(pady=10, fill=tk.X)

        # ----- Thanh trạng thái -----
        self.status_var = tk.StringVar(value="Sẵn sàng. Nhấn 'Next Step' để bắt đầu.")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Khởi tạo lưới mẫu 3×4 để demo — sẽ thay bằng dữ liệu thật sau
        self.matrix_grid.build_grid(3, 4)
        for i in range(3):
            for j in range(4):
                self.matrix_grid.update_cell(i, j, f"({i},{j})")

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _on_next_step(self) -> None:
        """Xử lý sự kiện nhấn nút 'Next Step'."""
        # TODO: gọi solver.optimize_step() và cập nhật giao diện
        self.status_var.set("TODO: gọi solver.optimize_step() ở Phase 4+")

    def _on_reset(self) -> None:
        """Xử lý sự kiện nhấn nút 'Reset'."""
        # TODO: gọi solver.reset() và vẽ lại trạng thái ban đầu
        self.status_var.set("TODO: gọi solver.reset() ở Phase 4+")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Chạy vòng lặp chính của Tkinter."""
        self.root.mainloop()
