"""
core.py - Thua toan giai bai toan van tai.

Lop TransportationSolver nhan vao mot TransportationData da can bang
va thuc hien cac buoc:
  1. Tim phuong an cuc bien ban dau (phuong phap chi phi nho nhat / goc Tay Bac).
  2. Tinh tong chi phi.
  3. Ho tro hien thi trang thai tung buoc cho UI.
"""

from typing import Any

import numpy as np

from src.solver.models import TransportationData


class TransportationSolver:
    """
    Giai bai toan van tai bang phuong phap chi phi nho nhat hoac goc Tay Bac.
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
        self._steps: list[dict[str, Any]] = []

    def least_cost(self) -> np.ndarray:
        """Phuong phap chi phi nho nhat (Minimum Cost / Matrix Minimum)."""
        sup = self._a.copy()
        dem = self._b.copy()
        m, n = self._m, self._n
        x = np.zeros((m, n), dtype=float)
        used = np.zeros((m, n), dtype=bool)

        remaining = m * n
        while remaining > 0:
            candidates = []
            for i in range(m):
                if sup[i] <= 1e-12:
                    continue
                for j in range(n):
                    if dem[j] <= 1e-12 or used[i, j]:
                        continue
                    candidates.append({
                        'i': i, 'j': j,
                        'cost': self._c[i, j],
                        'amt': min(sup[i], dem[j]),
                    })
            if not candidates:
                break
            candidates.sort(key=lambda item: (item['cost'], -item['amt']))
            best = candidates[0]
            i, j = best['i'], best['j']
            amt = min(sup[i], dem[j])
            x[i, j] = amt
            sup[i] -= amt
            dem[j] -= amt
            used[i, j] = True
            if sup[i] <= 1e-12:
                used[i, :] = True
            if dem[j] <= 1e-12:
                used[:, j] = True
            remaining -= 1
        return x

    def northwest_corner(self) -> np.ndarray:
        """Phuong phap goc Tay Bac (Northwest Corner)."""
        sup = self._a.copy()
        dem = self._b.copy()
        m, n = self._m, self._n
        x = np.zeros((m, n), dtype=float)
        i, j = 0, 0
        while i < m and j < n:
            amt = min(sup[i], dem[j])
            x[i, j] = amt
            sup[i] -= amt
            dem[j] -= amt
            if sup[i] < 1e-12:
                i += 1
            else:
                j += 1
        return x

    def total_cost(self, x: np.ndarray | None = None) -> float:
        if x is None:
            x = self._x
        if x is None:
            return 0.0
        return float(np.sum(x * self._c))

    def find_initial_solution(self, method: str = "least_cost") -> dict[str, Any]:
        if method == "northwest_corner":
            self._x = self.northwest_corner()
            method_name = "Goc tren-trai (Northwest Corner)"
        else:
            self._x = self.least_cost()
            method_name = "Cuc tieu cuoc phi (Least Cost)"

        self._method = method_name
        cost = self.total_cost()
        basic_count = int(np.sum(self._x > 1e-12))
        need = self._m + self._n - 1
        padded = basic_count < need

        if padded:
            alloc = self._x.copy()
            for i in range(self._m):
                for j in range(self._n):
                    if alloc[i, j] < 1e-12 and basic_count < need:
                        alloc[i, j] = 0.0
                        basic_count += 1
            self._x = alloc

        result = {
            'x': self._x.tolist(),
            'method': method_name,
            'cost': cost,
            'basic_count': basic_count,
            'need': need,
            'padded': padded,
            'description': (
                f"Tim phuong an ban dau bang {method_name}. "
                f"So o co ban: {basic_count}/{need}. "
                f"Tong chi phi Z = {cost:.2f}"
            ),
        }
        self._steps.append(result)
        return result

    def get_state(self) -> dict[str, Any]:
        return {
            'a': self._a.tolist(),
            'b': self._b.tolist(),
            'c': self._c.tolist(),
            'x': self._x.tolist() if self._x is not None else None,
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
        self._steps.clear()

    def calculate_potentials(self) -> dict[str, Any]:
        raise NotImplementedError("TODO: Phase 4 - MODI method")

    def check_optimality(self) -> dict[str, Any]:
        raise NotImplementedError("TODO: Phase 4 - MODI method")

    def find_cycle(self, entering: tuple[int, int]) -> dict[str, Any]:
        raise NotImplementedError("TODO: Phase 5 - Cycle detection")

    def optimize_step(self) -> dict[str, Any]:
        raise NotImplementedError("TODO: Phase 5 - MODI iteration")