"""
models.py — Định nghĩa cấu trúc dữ liệu đầu vào cho bài toán vận tải.

Lớp TransportationData lưu trữ:
  - Mảng phát a = (a_1, a_2, ..., a_m)
  - Mảng thu  b = (b_1, b_2, ..., b_n)
  - Ma trận cước phí c = (c_ij) kích thước m × n

Cung cấp phương thức kiểm tra cân bằng và cân bằng hóa bài toán.
"""

from typing import Optional

import numpy as np
import pandas as pd


class TransportationData:
    """
    Lưu trữ dữ liệu bài toán vận tải và cung cấp các tiện ích kiểm tra cân bằng.
    """

    def __init__(
        self,
        a: np.ndarray,        # Mảng phát (m,) — a_i >= 0
        b: np.ndarray,        # Mảng thu  (n,) — b_j >= 0
        c: np.ndarray,        # Ma trận cước phí (m, n) — c_ij >= 0
    ) -> None:
        """Khởi tạo bài toán với mảng phát , mảng thu , ma trận cước c."""
        raise NotImplementedError("TODO: Phase 2")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def num_supply(self) -> int:
        """Số trạm phát (m)."""
        raise NotImplementedError("TODO: Phase 2")

    @property
    def num_demand(self) -> int:
        """Số trạm thu (n)."""
        raise NotImplementedError("TODO: Phase 2")

    @property
    def total_supply(self) -> float:
        """Tổng lượng phát ∑a_i."""
        raise NotImplementedError("TODO: Phase 2")

    @property
    def total_demand(self) -> float:
        """Tổng lượng thu ∑b_j."""
        raise NotImplementedError("TODO: Phase 2")

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def is_balanced(self) -> bool:
        """
        Kiểm tra bài toán có cân bằng thu/phát hay không.
        Trả về True nếu ∑a_i == ∑b_j (trong sai số floating-point).
        """
        raise NotImplementedError("TODO: Phase 2")

    def balance_problem(self) -> "TransportationData":
        """
        Nếu chưa cân bằng, thêm trạm phát ảo (dummy supply) hoặc
        trạm thu ảo (dummy demand) với cước phí 0 để đưa về cân bằng.
        Trả về bản sao đã cân bằng.
        """
        raise NotImplementedError("TODO: Phase 2")

    def to_dataframe(self) -> pd.DataFrame:
        """Xuất ma trận cước phí dạng DataFrame để dễ xem / debug."""
        raise NotImplementedError("TODO: Phase 2")
