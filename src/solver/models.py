"""
models.py - Dinh nghia cau truc du lieu dau vao cho bai toan van tai.

Lop TransportationData luu tru:
  - Mang phat a = (a_1, a_2, ..., a_m)
  - Mang thu b = (b_1, b_2, ..., b_n)
  - Ma tran cuoc phi c = (c_ij) kich thuoc m x n

Cung cap phuong thuc nap tu CSV, kiem tra can bang va can bang hoa bai toan.
"""

from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd


# Hang so M dai dien cho cuoc phi cua o cam (muc 5.4).
# Bao dam BE KA lon hon moi tong chi phi kha di: lay cuoc phi huu han lon nhat
# nhan voi tong cung roi *10, cong them 1000. Dinh nghia tai thoi diem import
# de from_csv co the dung ngay (tinh lai theo tung bai toan trong from_csv).
BIG_M: float = 1e6


class TransportationData:
    """Luu tru du lieu bai toan van tai va cac tien ich kiem tra can bang."""

    def __init__(
        self,
        a: np.ndarray,
        b: np.ndarray,
        c: np.ndarray,
        forbidden: set[tuple[int, int]] | None = None,
    ) -> None:
        if a.ndim != 1:
            raise ValueError(f"a phai la mang 1-D, nhan duoc {a.ndim}-D")
        if b.ndim != 1:
            raise ValueError(f"b phai la mang 1-D, nhan duoc {b.ndim}-D")
        if c.ndim != 2:
            raise ValueError(f"c phai la mang 2-D, nhan duoc {c.ndim}-D")
        if c.shape[0] != a.shape[0] or c.shape[1] != b.shape[0]:
            raise ValueError(
                f"Kich thuoc khong khop: c {c.shape}, a {a.shape}, b {b.shape}"
            )
        if np.any(a < 0):
            raise ValueError("Mang phat a chua gia tri am")
        if np.any(b < 0):
            raise ValueError("Mang thu b chua gia tri am")
        if np.any(c < 0):
            raise ValueError("Ma tran cuoc phi c chua gia tri am")

        self._a = a.astype(float)
        self._b = b.astype(float)
        self._c = c.astype(float)
        self._forbidden: set[tuple[int, int]] = set(forbidden or [])

    @classmethod
    def from_csv(cls, path: str | Path) -> "TransportationData":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Khong tim thay file: {path}")

        # utf-8-sig de loai bo BOM (Excel xuat CSV kem BOM se crash neu dung utf-8)
        lines = path.read_text(encoding="utf-8-sig").strip().splitlines()

        c_rows: list[list[float]] = []
        a_vals: Optional[list[float]] = None
        b_vals: Optional[list[float]] = None

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            keyword = parts[0].strip().lower()
            values = [v.strip() for v in parts[1:]]

            if keyword == "c_ij":
                c_rows.append([np.nan if v in ("M", "m") else float(v) for v in values])
            elif keyword == "supply":
                a_vals = [float(v) for v in values]
            elif keyword == "demand":
                b_vals = [float(v) for v in values]
            else:
                raise ValueError(f"Dong khong hop le trong CSV: {line}")

        if a_vals is None or b_vals is None or len(c_rows) == 0:
            raise ValueError(
                "File CSV phai chua it nhat mot dong c_ij, mot dong supply va mot dong demand"
            )

        m = len(c_rows)
        n = len(c_rows[0]) if c_rows else 0
        if any(len(row) != n for row in c_rows):
            raise ValueError("Cac dong c_ij trong CSV phai co cung so cot")
        if len(a_vals) != m:
            raise ValueError(
                f"So luong supply ({len(a_vals)}) khong khop voi so hang c ({m})"
            )
        if len(b_vals) != n:
            raise ValueError(
                f"So luong demand ({len(b_vals)}) khong khop voi so cot c ({n})"
            )

        # Xac dinh o cam (nhan M/m) va gan cuoc phi = BIG_M.
        # BIG_M duoc tinh dong du lon so voi moi tong chi phi kha di.
        c_full = np.array(c_rows, dtype=float)
        finite = c_full[np.isfinite(c_full)]
        local_big_m = (
            float(np.max(finite)) * float(np.sum(a_vals)) * 10.0 + 1000.0
            if finite.size > 0
            else BIG_M
        )
        c_final = c_full.copy()
        forbidden: set[tuple[int, int]] = set()
        for i in range(m):
            for j in range(n):
                if not np.isfinite(c_full[i, j]):
                    forbidden.add((i, j))
                    c_final[i, j] = local_big_m

        return cls(
            a=np.array(a_vals),
            b=np.array(b_vals),
            c=c_final,
            forbidden=forbidden,
        )

    @property
    def a(self) -> np.ndarray:
        """Mang phat a_i."""
        return self._a.copy()

    @property
    def b(self) -> np.ndarray:
        """Mang thu b_j."""
        return self._b.copy()

    @property
    def c(self) -> np.ndarray:
        """Ma tran cuoc phi c_ij."""
        return self._c.copy()

    @property
    def forbidden(self) -> set[tuple[int, int]]:
        """Tap cac o cam (i, j) khong duoc phep van chuyen."""
        return set(self._forbidden)

    @property
    def num_supply(self) -> int:
        """So tram phat (m)."""
        return self._a.shape[0]

    @property
    def num_demand(self) -> int:
        """So tram thu (n)."""
        return self._b.shape[0]

    @property
    def total_supply(self) -> float:
        """Tong luong phat Tong a_i."""
        return float(np.sum(self._a))

    @property
    def total_demand(self) -> float:
        """Tong luong thu Tong b_j."""
        return float(np.sum(self._b))

    def is_balanced(self) -> bool:
        """
        Kiem tra bai toan co can bang thu/phat hay khong.
        Tra ve True neu Tong a_i == Tong b_j (trong sai so floating-point 1e-9).
        """
        return abs(self.total_supply - self.total_demand) < 1e-9

    def balance_problem(self) -> "TransportationData":
        """
        Neu chua can bang, them tram phat ao (dummy supply) hoac
        tram thu ao (dummy demand) voi cuoc phi 0 de dua ve can bang.
        Giu nguyen tap o cam self._forbidden; cac o hang/cot gia mac dinh
        (cuoc phi 0) KHONG phai la o cam.
        """
        if self.is_balanced():
            return TransportationData(
                self._a.copy(),
                self._b.copy(),
                self._c.copy(),
                forbidden=set(self._forbidden),
            )

        diff = self.total_supply - self.total_demand

        if diff > 0:
            new_b = np.append(self._b, diff)
            new_c = np.column_stack([self._c, np.zeros(self.num_supply)])
            return TransportationData(
                self._a.copy(),
                new_b,
                new_c,
                forbidden=set(self._forbidden),
            )
        else:
            new_a = np.append(self._a, -diff)
            new_c = np.vstack([self._c, np.zeros(self.num_demand)])
            return TransportationData(
                new_a,
                self._b.copy(),
                new_c,
                forbidden=set(self._forbidden),
            )

    def to_dataframe(self) -> pd.DataFrame:
        """Xuat ma tran cuoc phi dang DataFrame de debug."""
        idx = [f"A_{i+1}" for i in range(self.num_supply)]
        cols = [f"B_{j+1}" for j in range(self.num_demand)]
        return pd.DataFrame(self._c, index=idx, columns=cols)