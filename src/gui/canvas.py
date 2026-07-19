"""
canvas.py - Widget luoi ma tran tuy chinh cho ung dung van tai.

MatrixGrid ke thua tk.Frame, dung de hien thi ma tran cuoc phi / phuong an
voi cac Label/Entry sap xep theo hang va cot. Ho tro to mau o theo ma mau.
"""

from typing import Optional

import tkinter as tk


class MatrixGrid(tk.Frame):
    """Luoi hien thi ma tran dang bang (Label / Entry)."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        """
        Khoi tao khung luoi.
        Args:
            parent: Widget cha (thuong la tk.Frame hoac tk.Tk).
        """
        super().__init__(parent, **kwargs)
        self._cells: list[list[tk.Label | tk.Entry]] = []

    def build_grid(self, rows: int, cols: int) -> None:
        """
        Xay dung luoi o kich thuoc rows x cols.
        Xoa toan bo o cu neu co, tao lai tu dau.
        """
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
        Cap nhat noi dung va mau nen cho o (row, col).
        Args:
            row: Chi so hang (0-based).
            col: Chi so cot (0-based).
            value: Gia tri hien thi (str hoac so).
            color_code: Ma mau nen (hex, vi du "#FFDDDD").
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
            cell.config(bg="SystemButtonFace")

    # ------------------------------------------------------------------
    # Phuong thuc tien ich - hien thi du lieu bai toan
    # ------------------------------------------------------------------

    def render_from_data(self, a: list[float], b: list[float],
                         c: list[list[float]],
                         color_header: str = "#1565c0",
                         color_supply: str = "#e8f5e9") -> None:
        """
        Xay dung luoi hien thi bai toan van tai hoan chinh.
        """
        m = len(a)
        n = len(b)
        rows = m + 2
        cols = n + 2

        self.build_grid(rows, cols)

        # Header row
        self.update_cell(0, 0, "i\\j", color_header)
        for j in range(n):
            self.update_cell(0, j + 1, f"B_{j+1}", color_header)
        self.update_cell(0, n + 1, "a_i", color_header)

        # Data rows
        for i in range(m):
            self.update_cell(i + 1, 0, f"A_{i+1}", color_header)
            for j in range(n):
                self.update_cell(i + 1, j + 1, str(c[i][j]))
            self.update_cell(i + 1, n + 1, str(a[i]), color_supply)

        # Demand row
        self.update_cell(m + 1, 0, "b_j", color_header)
        for j in range(n):
            self.update_cell(m + 1, j + 1, str(b[j]), color_supply)
        self.update_cell(m + 1, n + 1, "Sum=Sum", color_supply)

    def render_solution(self, x: list[list[float]],
                        basic_color: str = "#e3f2fd",
                        zero_color: str = "#ffffff") -> None:
        """
        To mau ma tran phuong an.
        """
        m = len(x)
        n = len(x[0]) if x else 0
        for i in range(m):
            for j in range(n):
                if x[i][j] > 1e-9:
                    self.update_cell(i + 1, j + 1, f"{x[i][j]:.2f}", basic_color)
                else:
                    self.update_cell(i + 1, j + 1, "0", zero_color)