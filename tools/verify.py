import os
import sys

import numpy as np

TUTT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TUTT not in sys.path:
    sys.path.insert(0, TUTT)

from src.solver.models import TransportationData
from src.solver.core import TransportationSolver

DATA_DIR = os.path.join(TUTT, 'data')

METHODS = ('least_cost', 'double_priority', 'northwest_corner')

# Header dung the dung y: hai cot dau co khoang trong de can le
header = '   Bai              Z0_PP1   Z0_PP2   Z0_PP3   o_co_ban_PP2   Z*_PP1  Z*_PP2  Z*_PP3'
print(header)
print('-' * len(header))

for name in sorted(os.listdir(DATA_DIR)):
    if not name.endswith('.csv'):
        continue
    path = os.path.join(DATA_DIR, name)
    data = TransportationData.from_csv(path)

    # Z0 moi phuong phap
    z0 = {}
    for method in METHODS:
        solver = TransportationSolver(data)
        res = solver.find_initial_solution(method)
        z0[method] = res['cost']

    # So o co ban thuc te cua PP2 (sau can bang) - lay len(basic) de bao gom o chon 0
    solver = TransportationSolver(data)
    x, basic = solver.double_priority()
    real_basic = len(basic)
    need = solver._m + solver._n - 1
    obs_str = f'{real_basic}/{need}'

    # Z toi uu moi phuong phap
    zstar = {}
    for method in METHODS:
        solver = TransportationSolver(data)
        st = solver.solve(method)
        zstar[method] = st['cost']

    print(
        f'{name:<20}'
        f'{z0["least_cost"]:>7.0f} '
        f'{z0["double_priority"]:>7.0f} '
        f'{z0["northwest_corner"]:>8.0f}  '
        f'{obs_str:>12}  '
        f'{zstar["least_cost"]:>8.0f} '
        f'{zstar["double_priority"]:>8.0f} '
        f'{zstar["northwest_corner"]:>8.0f}'
    )

    if name == 'vd7.csv':
        solver = TransportationSolver(data)
        st = solver.solve('least_cost')
        print(f"   x tai o cam (0,4) = {st['x'][0][4]:.4f}   (forbidden_check valid = {st['forbidden_check']['valid']})")
