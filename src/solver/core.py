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
        self._forbidden: set[tuple[int, int]] = set(balanced.forbidden)
        self._forbidden_check: dict[str, Any] | None = None
        self._x: np.ndarray | None = None
        self._u: np.ndarray | None = None
        self._v: np.ndarray | None = None
        self._method: str = ""
        self._basic_cells: list[tuple[int, int]] = []
        self._steps: list[dict[str, Any]] = []
        self._is_optimal: bool = False
        self._marks: list[list[str]] = []

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
    # 2b. Phuong phap uu tien kep theo gia cuoc cuc tieu (PP2, slide 24)
    # ------------------------------------------------------------------

    def double_priority(self) -> tuple[np.ndarray, list[tuple[int, int]]]:
        """
        Phuong phap uu tien kep theo gia cuoc cuc tieu (PP2 muc 5.2.3).

        Buoc A - Danh dau (tinh MOT lan tren ma tran cuoc phi da can bang):
          - Voi moi HANG i: tim min c[i,:], moi o dat gia tri min do duoc danh 1 lan.
          - Voi moi COT j: tim min c[:,j], moi o dat gia tri min do duoc danh 1 lan.
          - O duoc danh dau 2 lan (vua min hang vua min cot) => nhan "VV".
          - O duoc danh dau 1 lan => nhan "V".
          - O khong duoc danh dau => nhan "" (khong dau).
          Ket qua luu vao self._marks (list 2 chieu cac chuoi).

        Buoc B - Phan phoi theo 3 dot uu tien: VV -> V -> "".
          Trong moi dot dung dunng quy tac cua phuong phap cuc tieu cuoc phi:
          chon o co cuoc phi nho nhat trong cac hang/cot chua bi gach; neu
          nhieu o cung cuoc phi min thi uu tien o co min(sup,dem) LON HON.
          Xu ly suy bien giong least_cost: khi cung va cau can kiet cung luc,
          chi gach HANG, giu COT lai de vong sau tao o co ban 0.
          Dung khi da du m+n-1 o co ban hoac khong con o nao phan phoi duoc.

        Tra ve (ma tran x, danh sach o co ban).
        """
        m, n = self._m, self._n
        # === Buoc A: danh dau ===
        marks = [[""] * n for _ in range(m)]
        # min moi hang -> danh dau 1 lan (V)
        for i in range(m):
            mn = float(np.min(self._c[i, :]))
            for j in range(n):
                if abs(self._c[i, j] - mn) < 1e-12:
                    marks[i][j] = "V"
        # min moi cot -> cong them (V -> VV)
        for j in range(n):
            mn = float(np.min(self._c[:, j]))
            for i in range(m):
                if abs(self._c[i, j] - mn) < 1e-12:
                    marks[i][j] = "VV" if marks[i][j] == "V" else "V"
        self._marks = marks

        sup = self._a.copy()
        dem = self._b.copy()
        x = np.zeros((m, n), dtype=float)
        row_done = np.zeros(m, dtype=bool)
        col_done = np.zeros(n, dtype=bool)
        basic_cells: list[tuple[int, int]] = []

        # === Buoc B: 3 dot uu tien ===
        for priority in ("VV", "V", ""):
            while len(basic_cells) < m + n - 1:
                candidates = []
                for i in range(m):
                    if row_done[i]:
                        continue
                    for j in range(n):
                        if col_done[j]:
                            continue
                        if marks[i][j] != priority:
                            continue
                        candidates.append({
                            'i': i, 'j': j,
                            'cost': float(self._c[i, j]),
                            'amt': min(sup[i], dem[j]),
                        })
                if not candidates:
                    break
                # Chon cuoc phi nho nhat; neu bang nhau chon amt lon nhat
                candidates.sort(key=lambda item: (item['cost'], -item['amt']))
                best = candidates[0]
                i, j = best['i'], best['j']
                amt = best['amt']
                x[i, j] = amt
                basic_cells.append((i, j))
                sup[i] -= amt
                dem[j] -= amt

                row_exhausted = sup[i] < 1e-12
                col_exhausted = dem[j] < 1e-12
                if row_exhausted and col_exhausted:
                    # === SUY BIEN: chi gach hang, giu cot (dem=0) de tao o 0 ===
                    row_done[i] = True
                elif row_exhausted:
                    row_done[i] = True
                elif col_exhausted:
                    col_done[j] = True

        return x, basic_cells

    # ------------------------------------------------------------------
    # 3. Tinh tong chi phi Z = SumSum c_ij * x_ij
    # ------------------------------------------------------------------

    def total_cost(
        self,
        x: np.ndarray | None = None,
        exclude_forbidden: bool = False,
    ) -> float:
        """
        Tinh tong chi phi Z = SumSum c_ij * x_ij.
        Khi exclude_forbidden=True, khong cong chi phi cua cac o cam vao tong
        (dung de bao cao chi phi thuc te). Mac dinh giu nguyen hanh vi cu.
        """
        if x is None:
            x = self._x
        if x is None:
            return 0.0
        if not exclude_forbidden:
            return float(np.sum(x * self._c))
        mask = np.ones(self._c.shape, dtype=bool)
        for (i, j) in self._forbidden:
            mask[i, j] = False
        return float(np.sum(x[mask] * self._c[mask]))

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
        elif method == "double_priority":
            x, basic_cells = self.double_priority()
            method_name = "Uu tien kep theo gia cuoc cuc tieu"
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
            'is_optimal': self._is_optimal,
            'forbidden': sorted(list(self._forbidden)),
            'forbidden_check': self._forbidden_check,
        }

    def reset(self) -> None:
        """Dua solver ve trang thai ban dau (chua co phuong an)."""
        self._x = None
        self._method = ""
        self._basic_cells = []
        self._steps.clear()
        self._is_optimal = False
        self._forbidden_check = None

    # ------------------------------------------------------------------
    # Phase 4 - Thuat toan the vi MODI
    # ------------------------------------------------------------------

    def _ensure_spanning_basis(self) -> None:
        """
        Dam bao tap o co ban co dung m+n-1 o va KHONG tao vong, dung ky
        thuat hop nhat tap (union-find) tren do thi hai phia (hang - cot):
        moi o co ban noi hang i voi cot (m+j). Neu thieu o co ban (phuong
        an suy bien - xem DN4 muc 5.1.3), bo sung cac "o chon 0" sao cho
        khong tao vong (giu tinh chat cay khung, dieu kien de tinh the vi).

        Day la buoc an toan chay truoc moi lan tinh the vi, bat ke
        phuong phap tim phuong an ban dau (least_cost / northwest_corner)
        co xu ly suy bien dung hay khong.
        """
        m, n = self._m, self._n
        parent = list(range(m + n))

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
            return True

        basic: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()

        # Uu tien giu lai cac o dang duoc coi la o co ban hien tai
        # (bao gom ca o co gia tri 0 dung de chong suy bien tu buoc truoc).
        for (i, j) in self._basic_cells:
            if (i, j) in seen:
                continue
            if union(i, m + j):
                basic.append((i, j))
                seen.add((i, j))

        # Dam bao moi o thuc su > 0 trong x deu duoc tinh la o co ban
        # (phong truong hop basic_cells bi lech so voi x sau dieu chinh).
        for i in range(m):
            for j in range(n):
                if (i, j) in seen:
                    continue
                if self._x[i, j] > 1e-9:
                    if union(i, m + j):
                        basic.append((i, j))
                        seen.add((i, j))
                    else:
                        print(
                            f"[CANH BAO] O ({i},{j}) co x>0 nhung tao chu trinh trong tap o "
                            f"co ban - phuong an hien tai khong phai phuong an cuc bien."
                        )

        # Bo sung o chon 0 neu con thieu de du m+n-1 o khong vong.
        if len(basic) < m + n - 1:
            for i in range(m):
                if len(basic) >= m + n - 1:
                    break
                for j in range(n):
                    if len(basic) >= m + n - 1:
                        break
                    if (i, j) in seen:
                        continue
                    if union(i, m + j):
                        basic.append((i, j))
                        seen.add((i, j))

        self._basic_cells = basic

    def calculate_potentials(self) -> dict[str, Any]:
        """
        Tinh the vi dong u_i va cot v_j theo dung quan he (5.2.2):
            Neu x_ij > 0 (o chon) thi v_j - u_i = c_ij  <=>  v_j = c_ij + u_i
        Quy uoc u_1 = 0 (mot dong bat ky lam moc), roi lan truyen theo
        cac o co ban (giong duyet cay khung vi m+n-1 o co ban khong vong).
        """
        if self._x is None:
            raise RuntimeError("Chua co phuong an ban dau. Goi find_initial_solution() truoc.")

        self._ensure_spanning_basis()
        m, n = self._m, self._n
        u: list[float | None] = [None] * m
        v: list[float | None] = [None] * n
        u[0] = 0.0

        changed = True
        while changed:
            changed = False
            for (i, j) in self._basic_cells:
                if u[i] is not None and v[j] is None:
                    v[j] = self._c[i, j] + u[i]
                    changed = True
                elif v[j] is not None and u[i] is None:
                    u[i] = v[j] - self._c[i, j]
                    changed = True

        if any(val is None for val in u) or any(val is None for val in v):
            raise RuntimeError(
                "Khong tinh du the vi - tap o co ban khong lien thong "
                "(kiem tra lai buoc tim phuong an ban dau / xu ly suy bien)."
            )

        self._u = np.array(u, dtype=float)
        self._v = np.array(v, dtype=float)
        return {
            'u': self._u.tolist(),
            'v': self._v.tolist(),
            'basic_cells': list(self._basic_cells),
        }

    def check_optimality(self) -> dict[str, Any]:
        """
        Tinh he so uoc luong Delta_ij = v_j - u_i - c_ij cho MOI o.
        Dau hieu toi uu (Dinh ly 5.2.2): Delta_ij <= 0 voi moi (i,j)
        (Delta_ij = 0 tai o chon theo (*), Delta_ij < 0 tai o loai theo (**)).
        """
        self.calculate_potentials()
        m, n = self._m, self._n
        delta = np.zeros((m, n), dtype=float)
        for i in range(m):
            for j in range(n):
                delta[i, j] = self._v[j] - self._u[i] - self._c[i, j]

        self._delta = delta
        max_delta = float(delta.max())
        is_optimal = max_delta <= 1e-9

        for (bi, bj) in self._basic_cells:
            assert abs(delta[bi, bj]) < 1e-6, \
                f"BUG: o co so ({bi},{bj}) co delta={delta[bi,bj]:.9f}, phai bang 0"

        entering: tuple[int, int] | None = None
        if not is_optimal:
            ei, ej = np.unravel_index(int(np.argmax(delta)), delta.shape)
            entering = (int(ei), int(ej))

        self._is_optimal = bool(is_optimal)

        return {
            'u': self._u.tolist(),
            'v': self._v.tolist(),
            'delta': delta.tolist(),
            'is_optimal': self._is_optimal,
            'entering_cell': entering,
            'max_delta': max_delta,
        }

    # ------------------------------------------------------------------
    # Phase 5 - Tim chu trinh dieu chinh va lap MODI
    # ------------------------------------------------------------------

    def find_cycle(self, entering: tuple[int, int]) -> dict[str, Any]:
        """
        Tim chu trinh (vong) khep kin xuat phat tu o "entering" (o vao)
        di qua cac o co ban, cac buoc di chuyen bat buoc luan phien:
        dong - cot - dong - cot - ... (dung DN2, muc 5.1.3).
        """
        basic = list(self._basic_cells)
        cells = [entering] + basic

        def search(path: list[tuple[int, int]], last_dir: str) -> list[tuple[int, int]] | None:
            cur = path[-1]
            next_dir = 'col' if last_dir == 'row' else 'row'
            for cell in cells:
                same_row = cell[0] == cur[0] and cell[1] != cur[1]
                same_col = cell[1] == cur[1] and cell[0] != cur[0]
                matches = same_row if next_dir == 'row' else same_col
                if not matches:
                    continue

                if cell == entering:
                    if len(path) >= 3:
                        return list(path)
                    continue
                if cell in path:
                    continue

                path.append(cell)
                result = search(path, next_dir)
                if result:
                    return result
                path.pop()
            return None

        for first_dir in ('row', 'col'):
            path = [entering]
            result = search(path, 'col' if first_dir == 'row' else 'row')
            if result:
                return {'loop': result, 'entering': entering}

        return {
            'loop': None,
            'entering': entering,
            'error': (
                'Khong tim duoc vong dieu chinh - kiem tra lai phuong an co ban '
                '(co the dang suy bien hoac tap o co ban khong hop le).'
            ),
        }

    def optimize_step(self) -> dict[str, Any]:
        """
        Thuc hien MOT buoc lap MODI:
          1. Kiem tra toi uu (check_optimality). Neu da toi uu -> dung.
          2. Neu chua, tim o vao (Delta lon nhat), tim vong dieu chinh.
          3. Tinh theta = min cac o mang dau tru trong vong, cap nhat x.
          4. Cap nhat tap o co ban: loai o roi, them o vao.
        """
        if self._x is None:
            raise RuntimeError("Chua co phuong an ban dau. Goi find_initial_solution() truoc.")

        check = self.check_optimality()
        if check['is_optimal']:
            result = {
                'is_optimal': True,
                'x': self._x.tolist(),
                'cost': self.total_cost(),
                'u': check['u'], 'v': check['v'], 'delta': check['delta'],
                'description': f"Da toi uu (Dinh ly 5.2.2). Z = {self.total_cost():.2f}",
            }
            self._steps.append(result)
            return result

        entering = check['entering_cell']
        cyc = self.find_cycle(entering)
        if cyc['loop'] is None:
            result = {'is_optimal': False, 'entering_cell': entering, 'error': cyc['error']}
            self._steps.append(result)
            return result

        loop = cyc['loop']
        minus_cells = loop[1::2]
        theta = min(self._x[i, j] for (i, j) in minus_cells)
        leaving = min(minus_cells, key=lambda cell: self._x[cell[0], cell[1]])

        for idx, (i, j) in enumerate(loop):
            sign = 1.0 if idx % 2 == 0 else -1.0
            self._x[i, j] = self._x[i, j] + sign * theta

        assert np.allclose(self._x.sum(axis=1), self._a, atol=1e-6), "Vi pham rang buoc cung"
        assert np.allclose(self._x.sum(axis=0), self._b, atol=1e-6), "Vi pham rang buoc cau"
        if theta < 1e-9:
            print(
                f"[CANH BAO] theta = 0 tai o vao {entering} - buoc xoay suy bien, "
                f"Z khong giam"
            )

        self._basic_cells = [cell for cell in self._basic_cells if cell != leaving]
        self._basic_cells.append(entering)

        result = {
            'is_optimal': False,
            'x': self._x.tolist(),
            'entering_cell': entering,
            'leaving_cell': leaving,
            'theta': float(theta),
            'loop': loop,
            'u': check['u'], 'v': check['v'], 'delta': check['delta'],
            'cost': self.total_cost(),
            'description': (
                f"O vao {tuple(x+1 for x in entering)}, "
                f"o roi {tuple(x+1 for x in leaving)}, theta={theta:.2f}. "
                f"Z sau dieu chinh = {self.total_cost():.2f}"
            ),
        }
        self._steps.append(result)
        return result

    def solve(self, method: str = "least_cost", max_iter: int = 100) -> dict[str, Any]:
        """
        Dieu phoi toan bo quy trinh: tim phuong an ban dau roi lap MODI
        cho den khi toi uu (hoac het max_iter). Tra ve trang thai cuoi
        cung + lich su tung buoc (dung cho nut Next Step / Reset o UI).
        """
        self.reset()
        self.find_initial_solution(method)

        for _ in range(max_iter):
            step = self.optimize_step()
            if step.get('is_optimal') or step.get('error'):
                break

        self._forbidden_check = self.check_forbidden_cells()
        return self.get_state()

    def compare_initial_methods(self) -> dict[str, Any]:
        """
        Chay ca 3 phuong phap tim phuong an ban dau (PP1/PP2/PP3) tren cung
        mot bai toan, moi phuong phap giai MODI den toi uu, roi tra ve bang
        so sanh: ten phuong phap, Z ban dau, so o co ban, Z toi uu, so vong
        lap MODI (dung cho Vi du 3 muc 5.2.3: "so sanh hai phuong phap do").
        """
        methods = [
            ("least_cost", "Cuc tieu cuoc phi (Least Cost)"),
            ("double_priority", "Uu tien kep theo gia cuoc cuc tieu"),
            ("northwest_corner", "Goc tren-trai (Northwest Corner)"),
        ]
        rows: list[dict[str, Any]] = []
        for key, name in methods:
            self.reset()
            init = self.find_initial_solution(key)
            iterations = 0
            while True:
                step = self.optimize_step()
                if step.get('is_optimal') or step.get('error'):
                    break
                iterations += 1
            rows.append({
                'method': name,
                'initial_cost': init['cost'],
                'basic_count': init['basic_count'],
                'optimal_cost': self.total_cost(),
                'modi_iterations': iterations,
            })
        return {'methods': rows}

    def check_forbidden_cells(self) -> dict[str, Any]:
        """
        Kiem tra phuong an hien tai co van chuyen vao o cam nao khong.
        Tra ve {'valid': bool, 'violations': [(i, j, x_ij), ...], 'message': str}.
        Neu ton tai o cam co x_ij > 1e-9 thi valid=False (Menh de 4, muc 5.4).
        """
        violations: list[tuple[int, int, float]] = []
        if self._x is None:
            return {
                'valid': True,
                'violations': [],
                'message': "Chua co phuong an.",
            }
        for (i, j) in sorted(self._forbidden):
            if self._x[i, j] > 1e-9:
                violations.append((i, j, float(self._x[i, j])))
        if violations:
            return {
                'valid': False,
                'violations': violations,
                'message': (
                    "Bai toan o cam khong co phuong an toi uu "
                    "(Menh de 4, muc 5.4)"
                ),
            }
        return {
            'valid': True,
            'violations': [],
            'message': "Khong co o cam nao bi van chuyen.",
        }

