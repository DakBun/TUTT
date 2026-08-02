import os
import numpy as np
import pytest
from src.solver.models import TransportationData
from src.solver.core import TransportationSolver


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def solve_csv(path):
    data = TransportationData.from_csv(path)
    solver = TransportationSolver(data)
    state = solver.solve('least_cost')
    return data, solver, state


def test_suy_bien_2x2():
    a = np.array([10.0, 10.0])
    b = np.array([10.0, 10.0])
    c = np.array([[1.0, 2.0], [3.0, 4.0]])
    data = TransportationData(a, b, c)
    solver = TransportationSolver(data)
    state = solver.solve('least_cost')
    assert state['is_optimal'] is True
    assert state['cost'] == pytest.approx(50.0, rel=1e-6)


def test_rang_buoc():
    for name in ('vd5.csv', 'vd3.csv', 'khong_can_bang.csv'):
        path = os.path.join(DATA_DIR, name)
        data, solver, state = solve_csv(path)
        balanced = data.balance_problem()
        x = np.array(state['x'])
        assert np.allclose(x.sum(axis=1), balanced.a, atol=1e-6)
        assert np.allclose(x.sum(axis=0), balanced.b, atol=1e-6)


def test_khong_can_bang():
    # TH1: cung > cau
    a = np.array([50.0, 100.0])
    b = np.array([80.0, 40.0])
    c = np.array([[1.0, 2.0], [3.0, 4.0]])
    data = TransportationData(a, b, c)
    assert not data.is_balanced()
    balanced = data.balance_problem()
    assert balanced.is_balanced()
    solver = TransportationSolver(data)
    state = solver.solve('least_cost')
    assert state['is_optimal'] is True
    x = np.array(state['x'])
    assert np.allclose(x.sum(axis=1), balanced.a, atol=1e-6)
    assert np.allclose(x.sum(axis=0), balanced.b, atol=1e-6)

    # TH2: cau > cung
    a = np.array([50.0, 80.0])
    b = np.array([100.0, 60.0])
    c = np.array([[1.0, 2.0], [3.0, 4.0]])
    data = TransportationData(a, b, c)
    assert not data.is_balanced()
    balanced = data.balance_problem()
    assert balanced.is_balanced()
    solver = TransportationSolver(data)
    state = solver.solve('least_cost')
    assert state['is_optimal'] is True
    x = np.array(state['x'])
    assert np.allclose(x.sum(axis=1), balanced.a, atol=1e-6)
    assert np.allclose(x.sum(axis=0), balanced.b, atol=1e-6)


def _solve_linprog(a_bal, b_bal, c_bal):
    from scipy.optimize import linprog
    m, n = c_bal.shape
    c_flat = c_bal.reshape(-1)
    A_eq = np.zeros((m + n, m * n))
    for i in range(m):
        A_eq[i, i * n : (i + 1) * n] = 1.0
    for j in range(n):
        A_eq[m + j, j::n] = 1.0
    b_eq = np.concatenate([a_bal, b_bal])
    bounds = [(0, None)] * (m * n)
    res = linprog(c_flat, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    if res.status != 0:
        raise AssertionError(
            "linprog failed (status={}): {}\n"
            "             cung={}, cau={}".format(
                res.status, res.message, a_bal.tolist(), b_bal.tolist()
            )
        )
    return float(res.fun)


def test_doi_chieu_linprog():
    # Kiem tra tren 3 file CSV (luon dung du lieu da can bang)
    for name in ('vd5.csv', 'vd3.csv', 'khong_can_bang.csv'):
        path = os.path.join(DATA_DIR, name)
        data = TransportationData.from_csv(path)
        balanced = data.balance_problem()
        solver = TransportationSolver(data)
        state = solver.solve('least_cost')
        z_modi = state['cost']
        z_linprog = _solve_linprog(balanced.a, balanced.b, balanced.c)
        assert abs(z_modi - z_linprog) < 1e-6

    # 30 bai toan ngau nhien
    rng = np.random.default_rng(42)
    for _ in range(30):
        m = int(rng.integers(2, 7))
        n = int(rng.integers(2, 7))
        c = rng.integers(1, 21, size=(m, n)).astype(float)
        a = rng.integers(5, 51, size=m).astype(float)
        b = rng.integers(5, 51, size=n).astype(float)
        data = TransportationData(a, b, c)
        balanced = data.balance_problem()
        solver = TransportationSolver(data)
        state = solver.solve('least_cost')
        z_modi = state['cost']
        z_linprog = _solve_linprog(balanced.a, balanced.b, balanced.c)
        assert abs(z_modi - z_linprog) < 1e-6


# ---------------------------------------------------------------------------
# Giai doan 3 - Doi chieu voi DAP AN da biet (giao trinh Chuong 5)
# ---------------------------------------------------------------------------

DAP_AN = [
    ("vd1.csv", 37.0, 33.0),
    ("vd2.csv", 885.0, 800.0),
    ("vd3.csv", 7670.0, 6560.0),
    ("vd5.csv", 570.0, 500.0),
    ("vd6.csv", 490.0, 490.0),
    ("vd7.csv", None, 1605.0),
    ("khong_can_bang.csv", None, 3000.0),
]


def test_z_ban_dau_pp1():
    for name, z0_pp1, z_opt in DAP_AN:
        if z0_pp1 is None:
            continue
        p = os.path.join(DATA_DIR, name)
        solver = TransportationSolver(TransportationData.from_csv(p))
        result = solver.find_initial_solution("least_cost")
        assert result["cost"] == pytest.approx(z0_pp1, rel=1e-6), f"{name} Z0_PP1={result['cost']}"


def test_z_toi_uu():
    for name, z0_pp1, z_opt in DAP_AN:
        p = os.path.join(DATA_DIR, name)
        solver = TransportationSolver(TransportationData.from_csv(p))
        state = solver.solve("least_cost")
        assert state["cost"] == pytest.approx(z_opt, rel=1e-6), f"{name} Z*={state['cost']}"


def test_vd7_o_cam():
    p = os.path.join(DATA_DIR, "vd7.csv")
    data = TransportationData.from_csv(p)
    assert (0, 4) in data.forbidden
    solver = TransportationSolver(data)
    state = solver.solve("least_cost")
    assert state["x"][0][4] == pytest.approx(0.0, abs=1e-9)
    assert state["forbidden_check"]["valid"] is True


def test_ba_phuong_phap_cung_Z():
    all_files = [d[0] for d in DAP_AN]
    for name in all_files:
        p = os.path.join(DATA_DIR, name)
        solver0 = TransportationSolver(TransportationData.from_csv(p))
        z0 = solver0.solve("least_cost")["cost"]
        for method in ("double_priority", "northwest_corner"):
            solver = TransportationSolver(TransportationData.from_csv(p))
            z = solver.solve(method)["cost"]
            assert abs(z0 - z) < 1e-6, f"{name}: Z* PP1={z0}, {method}={z}"


def test_pp2_hop_le():
    from pathlib import Path
    for path in sorted(Path('data').glob('*.csv')):
        data = TransportationData.from_csv(path)
        solver = TransportationSolver(data)
        r = solver.find_initial_solution('double_priority')
        m, n = solver._m, solver._n
        assert r['basic_count'] == m + n - 1, \
            f"{path.name}: PP2 co {r['basic_count']} o co ban, phai co {m+n-1}"
        x = np.array(r['x'])
        assert np.allclose(x.sum(axis=1), solver._a, atol=1e-6), f"{path.name}: sai cung"
        assert np.allclose(x.sum(axis=0), solver._b, atol=1e-6), f"{path.name}: sai cau"
