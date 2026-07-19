"""
core.py — Thuật toán giải bài toán vận tải.

Lớp TransportationSolver nhận vào một TransportationData đã cân bằng
và thực hiện các bước:
  1. Tìm phương án cực biên ban đầu (phương pháp chi phí nhỏ nhất / Vogel).
  2. Tính thế vị (u_i, v_j).
  3. Kiểm tra tối ưu (delta_ij).
  4. Nếu chưa tối ưu, tìm chu trình điều chỉnh và cải thiện phương án.
"""

from typing import Any, Optional

import numpy as np

from src.solver.models import TransportationData


class TransportationSolver:
    """
    Giải bài toán vận tải theo phương pháp thế vị (MODI method).
    Mỗi bước trả về trạng thái hiện tại để UI render.
    """

    def __init__(self, data: TransportationData) -> None:
        """
        Khởi tạo solver với dữ liệu bài toán.
        Tự động cân bằng nếu cần.
        """
        raise NotImplementedError("TODO: Phase 3")

    # ------------------------------------------------------------------
    # Public API — gọi từ UI
    # ------------------------------------------------------------------

    def find_initial_solution(self) -> dict[str, Any]:
        """
        Tìm phương án cực biên ban đầu bằng phương pháp chi phí nhỏ nhất.
        Trả về dict chứa:
          - 'x': ma trận phương án
          - 'description': mô tả bước (str)
        """
        raise NotImplementedError("TODO: Phase 3")

    def calculate_potentials(self) -> dict[str, Any]:
        """
        Tính thế vị u_i, v_j dựa trên ô cơ sở (x_ij > 0).
        Trả về dict chứa:
          - 'u': mảng thế vị dòng
          - 'v': mảng thế vị cột
          - 'description': mô tả bước
        """
        raise NotImplementedError("TODO: Phase 4")

    def check_optimality(self) -> dict[str, Any]:
        """
        Tính delta_ij cho tất cả ô phi cơ sở.
        Nếu tất cả delta_ij >= 0 → phương án tối ưu.
        Trả về dict chứa:
          - 'delta': ma trận delta_ij
          - 'is_optimal': bool
          - 'entering': (i, j) ô vào nếu chưa tối ưu
          - 'description': mô tả bước
        """
        raise NotImplementedError("TODO: Phase 4")

    def find_cycle(self, entering: tuple[int, int]) -> dict[str, Any]:
        """
        Tìm chu trình điều chỉnh bắt đầu từ ô (i, j) nhập.
        Trả về dict chứa:
          - 'cycle': list các tọa độ (i, j) trên chu trình
          - 'description': mô tả bước
        """
        raise NotImplementedError("TODO: Phase 5")

    def optimize_step(self) -> dict[str, Any]:
        """
        Thực hiện một bước lặp hoàn chỉnh:
         1. Tính thế vị
         2. Kiểm tra tối ưu
         3. Nếu chưa tối ưu → tìm chu trình → cập nhật phương án
        Trả về dict tổng hợp trạng thái mới.
        """
        raise NotImplementedError("TODO: Phase 5")

    def get_state(self) -> dict[str, Any]:
        """Trả về toàn bộ trạng thái hiện tại để UI vẽ lại."""
        raise NotImplementedError("TODO: Phase 3")

    def reset(self) -> None:
        """Đưa solver về trạng thái ban đầu (chưa có phương án)."""
        raise NotImplementedError("TODO: Phase 3")
