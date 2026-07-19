"""
canvas.py — Widget lưới ma trận tùy chỉnh cho ứng dụng vận tải.

MatrixGrid kế thừa tk.Frame, dùng để hiển thị ma trận cước phí / phương án
với các Label/Entry sắp xếp theo hàng và cột. Hỗ trợ tô màu ô theo mã màu.
"""

from typing import Optional

import tkinter as tk


class MatrixGrid(tk.Frame):
    """
    Lưới hiển thị ma trận dạng bảng (Label / Entry).
    Dùng để vẽ ma trận cước phí, phương án, delta...
    """

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        """
        Khởi tạo khung lưới.
        Args:
            parent: Widget cha (thường là tk.Frame hoặc tk.Tk).
        """
        super().__init__(parent, **kwargs)
        self._cells: list[list[tk.Label | tk.Entry]] = []

    def build_grid(self, rows: int, cols: int) -> None:
        """
        Xây dựng lưới ô kích thước rows × cols.
        Xóa toàn bộ ô cũ nếu có, tạo lại từ đầu.
        """
        # Xoá các widget cũ
        for widget in self.winfo_children():
            widget.destroy()
        self._cells = []

        for i in range(rows):
            row_cells: list[tk.Label | tk.Entry] = []
            for j in range(cols):
                cell = tk.Label(
                    self,
                    text="",
                    width=8,
                    height=2,
                    relief="solid",
                    borderwidth=1,
                    font=("Consolas", 10),
                )
                cell.grid(row=i, column=j, padx=1, pady=1)
                row_cells.append(cell)
            self._cells.append(row_cells)

    def update_cell(self, row: int, col: int, value: str, color_code: str = "") -> None:
        """
        Cập nhật nội dung và màu nền cho ô (row, col).

        Args:
            row: Chỉ số hàng (0-based).
            col: Chỉ số cột (0-based).
            value: Giá trị hiển thị (str hoặc số).
            color_code: Mã màu nền (hex, ví dụ "#FFDDDD").
        """
        if row < 0 or row >= len(self._cells):
            return
        if col < 0 or col >= len(self._cells[row]):
            return

        cell = self._cells[row][col]
        cell.config(text=str(value))
        if color_code:
            cell.config(bg=color_code)
        else:
            cell.config(bg="SystemButtonFace")  # màu mặc định
