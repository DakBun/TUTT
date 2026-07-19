"""
core.py - Thua toan giai bai toan van tai.

Lop TransportationSolver nhan vao mot TransportationData da can bang
va thuc hien cac buoc:
  1. Tim phuong an cuc bien ban dau (phuong phap chi phi nho nhat / goc Tay Bac).
  2. Tinh tong chi phi.
  3. Ho tro hien thi trang thai tung buoc cho UI.

Quy tac chong suy bien (anti-degeneracy):
  Khi luong Cung va Cau can kiet cung mot luc, chi duoc gach bo
  HANG i HOAC COT j, tuyet doi khong gach ca hai.
  Chieu khong bi gach giu lai gia tri 0 de vong lap sau tao o co ban 0.
"""

from typing import Any

import numpy as np

from src.solver.models import TransportationData


class TransportationSolver:
    """
    Giai bai toan van tai bang phuong phap chi phi nho nhat hoac goc Tay Bac.
    Luu tru danh sach o co ban (basic_cells) phuc vu cho thuat toan the vi MODI.
    """

    def __init__(self, data: TransportationData) -> None:
        self._original_data = data
        balanced = data.balance_problem()
        self._a = balanced.a
        self._b = balanced.b
        self._c = balanced.c
        self._m = balanced.num_supply
        self._n = balanced.num_demand
        self._balanced_flag = not data.is_balanced()
        self._x: np.ndarray | None = None
        self._method: str = ""
        self._basic_cells: list[tuple[int, int]] = []
        self._steps: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 1. Phuong phap chi phi nho nhat (Matrix Minimum / Least Cost)
    # ------------------------------------------------------------------

    def least_cost(self) -> tuple[np.ndarray, list[tuple[int, int]]]:
        """
        Phuong phap chi phi nho nhat.
        Tra ve (ma tran x, danh sach o co ban).
        """
        sup = self._a.copy()
        dem = self._b.copy()
        m, n = self._m, self._n
        x = np.zeros((m, n), dtype=float)
        row_done = np.zeros(m, dtype=bool)
        col_done = np.zeros(n, dtype=bool)
        basic_cells: list[tuple[int, int]] = []

        while len(basic_cells) < m + n - 1:
            # Tim o co cuoc phi nho nhat trong cac hang/cot chua bi gach
            candidates = []
            for i in range(m):
                if row_done[i]:
                    continue
                for j in range(n):
                    if col_done[j]:
                        continue
                    candidates.append({
                        'i': i, 'j': j,
                        'cost': self._c[i, j],
                    })
            if not candidates:
                break

            candidates.sort(key=lambda item: item['cost'])
            best = candidates[0]
            i, j = best['i'], best['j']
            amt = min(sup[i], dem[j])
            x[i, j] = amt
            basic_cells.append((i, j))
            sup[i] -= amt
            dem[j] -= amt

            row_exhausted = sup[i] < 1e-12
            col_exhausted = dem[j] < 1e-12

            if row_exhausted and col_exhausted:
                # === SUY BIEN: chi gach hang, giu cot (dem=0) de tao o 0 ===
                row_done[i] = True
                # Cot giu nguyen -> lan sau chon o cot nay se co amt = 0
            elif row_exhausted:
                row_done[i] = True
            elif col_exhausted:
                col_done[j] = True
            # Neu ca hai deu chua can, vong lap tiep tuc chon o khac

        return x, basic_cells

    # ------------------------------------------------------------------
    # 2. Phuong phap goc Tay Bac (Northwest Corner)
    # ------------------------------------------------------------------

    def northwest_corner(self) -> tuple[np.ndarray, list[tuple[int, int]]]:
        """
        Phuong phap goc Tay Bac.
        Tra ve (ma tran x, danh sach o co ban).
        """
        sup = self._a.copy()
        dem = self._b.copy()
        m, n = self._m, self._n
        x = np.zeros((m, n), dtype=float)
        basic_cells: list[tuple[int, int]] = []
        i, j = 0, 0

        while len(basic_cells) < m + n - 1 and i < m and j < n:
            amt = min(sup[i], dem[j])
            x[i, j] = amt
            basic_cells.append((i, j))
            sup[i] -= amt
            dem[j] -= amt

            if sup[i] < 1e-12 and dem[j] < 1e-12:
                # === SUY BIEN: chi xuo'ng hang, giu nguyen cot ===
                i += 1
                # j giu nguyen -> o (i+1, j) se co amt = 0
            elif sup[i] < 1e-12:
                i += 1
            else:
                j += 1

        return x, basic_cells

    # ------------------------------------------------------------------
    # 3. Tinh tong chi phi Z = SumSum c_ij * x_ij
    # ------------------------------------------------------------------

    def total_cost(self, x: np.ndarray | None = None) -> float:
        """Tinh tong chi phi Z = SumSum c_ij * x_ij."""
        if x is None:
            x = self._x
        if x is None:
            return 0.0
        return float(np.sum(x * self._c))

    # ------------------------------------------------------------------
    # 4. Tim phuong an ban dau (public API)
    # ------------------------------------------------------------------

    def find_initial_solution(self, method: str = "least_cost") -> dict[str, Any]:
        """
        Tim phuong an cuc bien ban dau.
        KHONG dung padding sai bang 2 vong for long nhau.
        So o co ban lay truc tiep tu len(basic_cells).
        """
        if method == "northwest_corner":
            x, basic_cells = self.northwest_corner()
            method_name = "Goc tren-trai (Northwest Corner)"
        else:
            x, basic_cells = self.least_cost()
            method_name = "Cuc tieu cuoc phi (Least Cost)"

        self._x = x
        self._basic_cells = basic_cells
        self._method = method_name
        cost = self.total_cost()
        basic_count = len(basic_cells)
        need = self._m + self._n - 1

        result = {
            'x': x.tolist(),
            'method': method_name,
            'cost': cost,
            'basic_count': basic_count,
            'need': need,
            'padded': basic_count < need,
            'basic_cells': [(int(r), int(c)) for r, c in basic_cells],
            'description': (
                f"Tim phuong an ban dau bang {method_name}. "
                f"So o co ban: {basic_count}/{need}. "
                f"Tong chi phi Z = {cost:.2f}"
            ),
        }
        self._steps.append(result)
        return result

    # ------------------------------------------------------------------
    # 5. Lay trang thai hien tai
    # ------------------------------------------------------------------

    def get_state(self) -> dict[str, Any]:
        """Tra ve toan bo trang thai hien tai de UI ve lai."""
        return {
            'a': self._a.tolist(),
            'b': self._b.tolist(),
            'c': self._c.tolist(),
            'x': self._x.tolist() if self._x is not None else None,
            'basic_cells': [(int(r), int(c)) for r, c in self._basic_cells]
                           if self._basic_cells else [],
            'm': self._m,
            'n': self._n,
            'method': self._method,
            'cost': self.total_cost(),
            'balanced_flag': self._balanced_flag,
            'steps': self._steps,
        }

    def reset(self) -> None:
        """Dua solver ve trang thai ban dau (chua co phuong an)."""
        self._x = None
        self._method = ""
        self._basic_cells = []
        self._steps.clear()

    # ------------------------------------------------------------------
    # TODO: Phase 4+ - Thue at toan the vi MODI
    # ------------------------------------------------------------------

    def calculate_potentials(self) -> dict[str, Any]:
        """Tinh the vi u_i, v_j (se implement o Phase 4)."""
        raise NotImplementedError("TODO: Phase 4 - MODI method")

    def check_optimality(self) -> dict[str, Any]:
        """Kiem tra toi uu bang delta_ij (se implement o Phase 4)."""
        raise NotImplementedError("TODO: Phase 4 - MODI method")

    def find_cycle(self, entering: tuple[int, int]) -> dict[str, Any]:
        """Tim chu trinh dieu chinh (se implement o Phase 5)."""
        raise NotImplementedError("TODO: Phase 5 - Cycle detection")

    def optimize_step(self) -> dict[str, Any]:
        """Thuc hien mot buoc lap MODI (se implement o Phase 5)."""
        raise NotImplementedError("TODO: Phase 5 - MODI iteration")