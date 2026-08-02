# Đồ án Tối ưu tuyến tính — Bài toán Vận tải

## 1. Tổng quan
Project này là ứng dụng desktop giải **Bài toán vận tải** (Transportation Problem) bằng Python và Tkinter. Người dùng nhập ma trận chi phí `c_ij`, vector phát `a_i` (supply) và vector thu `b_j` (demand), sau đó chọn phương pháp xây dựng phương án cơ sở ban đầu (**Least Cost** hoặc **Northwest Corner**) để lấy ma trận phân phối `x_ij` ban đầu. Ứng dụng tiếp tục tối ưu hóa bằng thuật toán **MODI** (Modified Distribution Method), cho phép xem từng bước cải tiến (Next Step) hoặc giải tự động (Auto Solve). Hệ thống hỗ trợ cả bài toán cân bằng và không cân bằng (thêm trạm phát/thu ảo). Kết quả hiển thị tổng chi phí `Z`, thế vị `u_i`, `v_j`, hệ số kiểm tra `Δ_ij` và trạng thái ô cơ sở.

## 2. Cây thư mục

```
├── .clinerules            (18 dòng)  Quy tắc kiến trúc và coding convention cho dự án.
├── .gitignore             (223 dòng) Danh sách file/thư mục bị bỏ qua bởi Git.
├── main.py                (23 dòng)  Entry point: khởi tạo Tkinter và TransportationApp.
├── README.md              (43 dòng)  [File cũ] Mô tả tổng quan ban đầu của project.
├── requirements.txt       (2 dòng)   Khai báo dependency: numpy, pandas.
├── vantai.py              (525 dòng) [Legacy] GUI cũ (TransportationApp cũ), không còn được entry point sử dụng.
├── data/
│   ├── example_5.csv      (6 dòng)   Dữ liệu mẫu Ví dụ 5: 4 trạm phát, 6 trạm thu.
│   ├── example_a.csv      (6 dòng)   Dữ liệu mẫu từ ảnh a: 4 trạm phát, 5 trạm thu.
│   └── example_b.csv      (6 dòng)   Dữ liệu mẫu từ ảnh b: 4 trạm phát, 5 trạm thu.
└── src/
    ├── __init__.py        (0 dòng)    Package marker.
    └── gui/
        ├── __init__.py    (0 dòng)    Package marker.
        ├── app.py         (633 dòng) Giao diện Tkinter chính (TransportationApp hiện tại).
        └── canvas.py      (121 dòng) Widget MatrixGrid hiển thị ma trận bài toán và nghiệm.
    └── solver/
        ├── __init__.py    (0 dòng)    Package marker.
        ├── core.py        (488 dòng) Thuật toán giải bài toán vận tải (Least Cost, NW Corner, MODI).
        └── models.py      (161 dòng) Cấu trúc dữ liệu TransportationData và đọc CSV.
```

## 3. Mô tả chi tiết từng module

### 3.1 `main.py`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\main.py`
- **Mục đích:** Entry point duy nhất của ứng dụng.
- **Import:**
  - Chuẩn: `sys`, `os`
  - Bên thứ ba: `tkinter`
  - Nội bộ: `src.gui.app.TransportationApp`
- **Hàm:**
  - `main() -> None`: Tạo cửa sổ `tk.Tk()`, khởi tạo `TransportationApp(root)`, gọi `root.mainloop()` để chạy vòng lặp sự kiện. Không chứa logic nghiệp vụ.

### 3.2 `src/gui/app.py`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\src\gui\app.py`
- **Mục đích:** Xây dựng toàn bộ giao diện Tkinter, nhận input người dùng, hiển thị ma trận kết quả, bảng phân phối và log từng bước.
- **Import:**
  - Chuẩn: (không có)
  - Bên thứ ba: `tkinter`, `tkinter.ttk`, `tkinter.messagebox`, `pathlib.Path`
  - Nội bộ: `src.solver.models.TransportationData`, `src.solver.core.TransportationSolver`
- **Class `TransportationApp`:**
  - `__init__(self, root: tk.Tk) -> None`: Khởi tạo cửa sổ 1200x700, khởi tạo các biến trạng thái (`m`, `n`, `c`, `supply`, `demand`, `x`, `solver`, `current_method`, các nút và log), gọi `setup_ui()`.
  - `setup_ui(self) -> None`: Xây dựng các khung giao diện:
    - Title frame với tên "Chương 5: Bài toán Vận tải".
    - Khung nhập liệu: chọn số trạm phát `m` và thu `n`, nút **"Tạo bảng vận tải"** để tạo ma trận nhập `C`, `a`, `b`.
    - Khung nút chức năng: **"Giải - Cực tiểu cước phí"** (gọi `solve_moc`), **"Giải - Góc Tây Bắc"** (gọi `solve_nw`), **"Bước tiếp"** (gọi `step_once`), **"Tự động"** (gọi `solve_auto`), **"Reset"** (gọi `reset_solver`), các nút ví dụ **"Ví dụ 5"**, **"Ảnh (a)"**, **"Ảnh (b)"**, **"Đọc CSV"**, **"Xóa"**.
    - Khung kết quả: hiển thị tên phương pháp, tổng chi phí `Z`, bảng `Treeview` kết quả, nhãn thông tin và vùng log từng bước (`Text`).
  - `create_table(self) -> None`: Dựa trên `m` và `n`, tạo ma trận `Entry` cho ma trận chi phí `c_ij`, vector `a_i` và `b_j`.
  - `read_input(self) -> TransportationData | None`: Đọc giá trị từ các `Entry`, tạo `TransportationData`, kiểm tra cân bằng, khởi tạo `TransportationSolver`. Trả về `None` nếu có lỗi nhập liệu.
  - `solve_moc(self) -> None`: Gọi `self.solver.find_initial_solution('least_cost')`, lấy trạng thái ban đầu và hiển thị bằng `show_result`. Bật các nút bước tiếp / tự động / reset.
  - `solve_nw(self) -> None`: Gọi `self.solver.find_initial_solution('northwest_corner')`, hiển thị tương tự.
  - `show_result(self, method_name: str, result: dict | None = None) -> None`: Điền dữ liệu ma trận nghiệm vào `Treeview`, tính số ô cơ sở, kiểm tra suy biến, hiển thị tổng chi phí và thông tin.
  - `_fill_table(self, alloc, basic_count: int, need: int, padded: bool) -> None`: Cập nhật ô trong ma trận hiển thị: tô màu xanh cho ô cơ sở, ghi giá trị `x_ij`, ghi `0` cho ô không cơ sở.
  - `step_once(self) -> None`: Gọi `self.solver.optimize_step()` để thực hiện 1 bước MODI. Cập nhật bảng và log. Nếu đã tối ưu thì vô hiệu hóa nút "Bước tiếp".
  - `solve_auto(self) -> None`: Gọi `self.solver.solve(method)` để giải hoàn chỉnh, hiển thị toàn bộ log các bước.
  - `reset_solver(self) -> None`: Gọi `self.solver.reset()`, xóa kết quả, vô hiệu hóa các nút solver.
  - `load_example5(self) -> None`: Điền dữ liệu Ví dụ 5 vào bảng nhập liệu (m=4, n=6, a=[70,60,20,30], b=[10,40,40,50,10,30], ma trận C tương ứng).
  - `load_image_a(self) -> None`: Điền dữ liệu ảnh a (m=4, n=5).
  - `load_image_b(self) -> None`: Điền dữ liệu ảnh b (m=4, n=5).
  - `load_csv(self) -> None`: Mở hộp thoại chọn file CSV, đọc bằng `TransportationData.from_csv`, điền vào bảng.
  - `clear_all(self) -> None`: Xóa toàn bộ widget trong bảng, reset các biến và nhãn kết quả.
  - `fmt(self, value) -> str`: Định dạng số thực thành chuỗi có dấu phân cách.
  - `_clear_step_log(self)`, `_append_log(self, text: str)`, `_enable_solver_controls(self)`: Tiện ích quản lý vùng log và trạng thái nút.
  - `main()`: Hàm chạy độc lập (legacy), tạo `tk.Tk()` và `root.mainloop()`.


## 1. Tổng quan
Project này là ứng dụng desktop giải **Bài toán vận tải** (Transportation Problem) bằng Python và Tkinter. Người dùng nhập ma trận chi phí c_ij, vector phát a_i (supply) và vector thu b_j (demand), sau đó chọn phương pháp xây dựng phương án cơ sở ban đầu (Least Cost hoặc Northwest Corner) để lấy ma trận phân phối x_ij ban đầu. Ứng dụng tiếp tục tối ưu hóa bằng thuật toán MODI (Modified Distribution Method), cho phép xem từng bước cải tiến (Next Step) hoặc giải tự động (Auto Solve). Hệ thống hỗ trợ cả bài toán cân bằng và không cân bằng (thêm trạm phát/thu ảo). Kết quả hiển thị tổng chi phí Z, thế vị u_i, v_j, hệ số kiểm tra Δ_ij và trạng thái ô cơ sở.

## 2. Cây thư mục

`
├── .clinerules            (18 dòng)  Quy tắc kiến trúc và coding convention cho dự án.
├── .gitignore             (223 dòng) Danh sách file/thư mục bị bỏ qua bởi Git.
├── main.py                (23 dòng)  Entry point: khởi tạo Tkinter và TransportationApp.
├── README.md              (43 dòng)  [File cũ] Mô tả tổng quan ban đầu của project.
├── requirements.txt       (2 dòng)   Khai báo dependency: numpy, pandas.
├── vantai.py              (525 dòng) [Legacy] GUI cũ (TransportationApp cũ), không còn được entry point sử dụng.
### 3.3 `src/gui/canvas.py`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\src\gui\canvas.py`
- **Mục đích:** Cung cấp widget `MatrixGrid` để hiển thị ma trận bài toán và nghiệm dưới dạng lưới `Label`.
- **Import:**
  - Chuẩn: `typing.Optional`
  - Bên thứ ba: `tkinter`
  - Nội bộ: (không có)
- **Class `MatrixGrid(tk.Frame)`:**
  - `__init__(self, parent: tk.Widget, **kwargs) -> None`: Khởi tạo khung, `self._cells` lưu danh sách 2 chiều các `Label`/`Entry`.
  - `build_grid(self, rows: int, cols: int) -> None`: Xóa toàn bộ widget cũ, tạo grid `Label` kích thước `rows x cols`.
  - `update_cell(self, row: int, col: int, value: str, color_code: str = "") -> None`: Cập nhật nội dung và màu nền của ô `(row, col)`. Bỏ qua nếu chỉ số nằm ngoài phạm vi.
  - `render_from_data(self, a: list[float], b: list[float], c: list[list[float]], color_header: str = "#1565c0", color_supply: str = "#e8f5e9") -> None`: Vẽ ma trận bài toán đầy đủ gồm header `i\j`, `B_j`, `a_i`, `b_j`.
  - `render_solution(self, x: list[list[float]], basic_color: str = "#e3f2fd", zero_color: str = "#ffffff") -> None`: Tô màu ô có giá trị `x_ij > 1e-9` bằng màu `basic_color`, các ô bằng `0` bằng `zero_color`.

├── data/
│   ├── example_5.csv      (6 dòng)   Dữ liệu mẫu Ví dụ 5: 4 trạm phát, 6 trạm thu.
│   ├── example_a.csv      (6 dòng)   Dữ liệu mẫu từ ảnh a: 4 trạm phát, 5 trạm thu.
│   └── example_b.csv      (6 dòng)   Dữ liệu mẫu từ ảnh b: 4 trạm phát, 5 trạm thu.
└── src/
    ├── __init__.py        (0 dòng)    Package marker.
    └── gui/
### 3.4 `src/solver/models.py`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\src\solver\models.py`
- **Mục đích:** Định nghĩa cấu trúc dữ liệu bài toán vận tải, kiểm tra tính hợp lệ và cân bằng, đọc dữ liệu từ CSV.
- **Import:**
  - Chuẩn: `pathlib.Path`, `typing.Optional`
  - Bên thứ ba: `numpy`, `pandas`
  - Nội bộ: (không có)
- **Class `TransportationData`:**
  - `__init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> None`: Kiểm tra `a` 1-D, `b` 1-D, `c` 2-D, kích thước khớp nhau, không chứa giá trị âm. Lưu các mảng dưới dạng `float`.
  - `from_csv(cls, path: str | Path) -> "TransportationData"`: Đọc file UTF-8, parse từng dòng:
    - Dòng bắt đầu bằng `c_ij` → thêm vào `c_rows`.
    - Dòng `supply` → lưu `a_vals`.
    - Dòng `demand` → lưu `b_vals`.
    Kiểm tra độ dài các dòng khớp nhau, trả về instance.
  - `a(self) -> np.ndarray`: Trả về bản sao vector phát.
  - `b(self) -> np.ndarray`: Trả về bản sao vector thu.
  - `c(self) -> np.ndarray`: Trả về bản sao ma trận chi phí.
  - `num_supply(self) -> int`: Trả về `m`.
  - `num_demand(self) -> int`: Trả về `n`.
  - `total_supply(self) -> float`: Trả về `Σ a_i`.
  - `total_demand(self) -> float`: Trả về `Σ b_j`.
  - `is_balanced(self) -> bool`: Trả về `True` nếu `|Σa_i - Σb_j| < 1e-9`.
  - `balance_problem(self) -> "TransportationData"`: Nếu mất cân bằng, thêm trạm ảo:
    - Nếu `Σa_i > Σb_j`: thêm cột `diff` vào `c`, mở rộng `b`.
    - Nếu `Σa_i < Σb_j`: thêm hàng `diff` vào `c`, mở rộng `a`.
    Trả về `TransportationData` mới đã cân bằng.
  - `to_dataframe(self) -> pd.DataFrame`: Xuất ma trận `c` dạng `DataFrame` với index `A_1..A_m` và columns `B_1..B_n`.

        ├── __init__.py    (0 dòng)    Package marker.
        ├── app.py         (633 dòng) Giao diện Tkinter chính (TransportationApp hiện tại).
        └── canvas.py      (121 dòng) Widget MatrixGrid hiển thị ma trận bài toán và nghiệm.
    └── solver/
        ├── __init__.py    (0 dòng)    Package marker.
        ├── core.py        (488 dòng) Thuật toán giải bài toán vận tải (Least Cost, NW Corner, MODI).
        └── models.py      (161 dòng) Cấu trúc dữ liệu TransportationData và đọc CSV.
### 3.5 `src/solver/core.py`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\src\solver\core.py`
- **Mục đích:** Chứa toàn bộ thuật toán giải bài toán vận tải: xây dựng phương án cơ sở ban đầu (Least Cost / Northwest Corner), tính thế vị, kiểm tra tối ưu, tìm chu trình cải tiến, điều chỉnh và lặp MODI.
- **Import:**
  - Chuẩn: `typing.Any`
  - Bên thứ ba: `numpy`
  - Nội bộ: `src.solver.models.TransportationData`
- **Class `TransportationSolver`:**
  - `__init__(self, data: TransportationData) -> None`: Lưu `data` gốc, gọi `data.balance_problem()` để có bài toán cân bằng, khởi tạo các biến trạng thái: `_x` (ma trận nghiệm), `_u`, `_v` (thế vị), `_method`, `_basic_cells` (tập ô cơ sở dạng list `[(i,j)]`), `_steps` (lịch sử các bước).
  - `least_cost(self) -> tuple[np.ndarray, list[tuple[int, int]]]`: Xây dựng phương án cơ sở ban đầu bằng **phương pháp chi phí nhỏ nhất**:
    - Trong khi số ô cơ sở < `m + n - 1`, tìm ô có `c_ij` nhỏ nhất trong các hàng/cột chưa bị gạch.
    - Phân phối `amt = min(sup[i], dem[j])`, cập nhật `sup`, `dem`.
    - Đánh dấu hàng/cột đã hết. Nếu cả hàng và cột cùng hết (suy biến), chỉ gạch **hàng**, giữ **cột** để lần sau tạo ô cơ sở có giá trị `0`.
    - Trả về ma trận `x` và danh sách `basic_cells`.
  - `northwest_corner(self) -> tuple[np.ndarray, list[tuple[int, int]]]`: Xây dựng phương án cơ sở ban đầu bằng **phương pháp góc Tây Bắc**:
    - Bắt đầu từ ô `(0,0)`, phân phối `amt = min(sup[i], dem[j])`, dịch chỉ số.
    - Nếu hàng hết → xuống hàng tiếp theo. Nếu cột hết → sang cột tiếp theo.
    - Nếu cả hai cùng hết, chỉ **xuống hàng**, giữ nguyên cột (để tạo ô 0 phục vụ suy biến).
    - Trả về `x` và `basic_cells`.
  - `total_cost(self, x: np.ndarray | None = None) -> float`: Tính `Z = ΣΣ c_ij * x_ij`. Nếu `x` là `None` dùng `self._x`.
  - `find_initial_solution(self, method: str = "least_cost") -> None`: Gọi `least_cost()` hoặc `northwest_corner()` theo `method`, lưu `_x`, `_basic_cells`, tính tổng chi phí ban đầu, lưu bước đầu vào `_steps`.
  - `get_state(self) -> dict[str, Any]`: Trả về dict chứa trạng thái hiện tại: `x`, `c`, `a`, `b`, `m`, `n`, `cost`, `method`, `basic_cells`, `steps`, `balanced_flag`, `u`, `v`, `delta`, `is_optimal` (nếu đã kiểm tra).
  - `reset(self) -> None`: Đặt lại solver về trạng thái chưa giải: `_x = None`, `_basic_cells = []`, `_steps = []`, `_method = ""`.
  - `_ensure_spanning_basis(self) -> None`: Dùng **Union-Find (Disjoint Set)** để kiểm tra tính liên thông của tập ô cơ sở. Nếu số ô < `m + n - 1` hoặc tập không liên thông, bổ sung các ô có `x_ij ≈ 0` (chọn 0) để đảm bảo đủ số ô và liên thông. Đây là cơ chế chống suy biến.
  - `calculate_potentials(self) -> tuple[np.ndarray, np.ndarray]`: Tính thế vị `u_i`, `v_j`. Đặt `u[0] = 0`, lan truyền qua các ô cơ sở `(i,j)` với `x_ij > 0`: `v_j = c_ij - u_i` và `u_i = c_ij - v_j`.
  - `check_optimality(self) -> dict[str, Any]`: Gọi `_ensure_spanning_basis()`, tính `u`, `v`, rồi tính `delta_ij = v_j - u_i - c_ij` cho tất cả các ô. Tìm ô vào có `delta_max = max(delta)` lớn nhất. Nếu `delta_max > 1e-9` thì chưa tối ưu. Nếu `delta_max <= 1e-9` thì đã tối ưu (`is_optimal = True`).
  - `find_cycle(self, entering: tuple[int, int]) -> dict[str, Any]`: Tìm **chu trình điều chỉnh** bắt đầu từ ô vào `entering` bằng **DFS**:
    - Bắt đầu từ ô vào, luân phiên duyệt theo dòng (`row`) rồi cột (`col`) (hoặc ngược lại), chỉ đi qua các ô cơ sở hiện tại.
    - Trả về danh sách các ô trong chu trình kín.
    - Nếu không tìm được, trả về lỗi.
  - `optimize_step(self) -> dict[str, Any]`: Thực hiện **1 bước lặp MODI**:
    1. Gọi `check_optimality()`. Nếu đã tối ưu, trả về kết quả cuối.
    2. Lấy ô vào có `delta` lớn nhất, gọi `find_cycle()` để lấy chu trình.
    3. Tính `theta = min(x_ij)` tại các ô có dấu trừ (`-`) trong chu trình (`minus_cells = loop[1::2]`).
    4. Cập nhật ma trận `x`: ô chẵn `+theta`, ô lẻ `-theta` theo thứ tự trong chu trình.
    5. Cập nhật `_basic_cells`: loại bỏ ô rời (`leaving` = ô có `x_ij = theta` trong `minus_cells`), thêm ô vào `entering`.
    6. Trả về dict mô tả bước (ô vào, ô rời, theta, vòng, chi phí mới).
  - `solve(self, method: str = "least_cost", max_iter: int = 100) -> dict[str, Any]`: Điều phối toàn bộ quy trình:
    1. Gọi `reset()`.
    2. Gọi `find_initial_solution(method)`.
    3. Lặp tối đa `max_iter` lần: gọi `optimize_step()`. Nếu đã tối ưu hoặc có lỗi thì dừng.
    4. Trả về `get_state()` (kèm lịch sử `steps`).

`


### 3.6 `vantai.py`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\vantai.py`
- **Mục đích:** File GUI cũ (legacy), chứa class `TransportationApp` phiên bản trước khi refactor theo kiến trúc tách biệt UI/Solver. Không được `main.py` sử dụng làm entry point, nhưng vẫn tồn tại trong project.
- **Import:**
  - Bên thứ ba: `tkinter`, `tkinter.ttk`, `tkinter.messagebox`
  - Nội bộ: (không có)
- **Class `TransportationApp` (legacy):**
  - `__init__(self, root)`: Tương tự `app.py` nhưng không có thuộc tính `solver`, `current_method`, `step_log`. Chỉ dùng `m`, `n`, `c`, `supply`, `demand`, `x`.
  - `setup_ui(self)`: Xây dựng UI với các nút: **"Tạo bảng"**, **"Giải - Cực tiểu cước phí"** (`solve_moc`), **"Giải - Góc Tây Bắc"** (`solve_nw`), **"Bước tiếp"** (`step_once`), **"Tự động"** (`solve_auto`), **"Reset"** (`reset_solver`), các nút ví dụ, **"Xóa"**.
  - `create_table(self)`: Tạo ma trận nhập liệu.
  - `read_input(self)`: Đọc dữ liệu từ Entry, kiểm tra hợp lệ, gán `self.c`, `self.supply`, `self.demand`.
  - `least_cost(self) -> np.ndarray`: Xây dựng phương án ban đầu (phiên bản nội bộ, không dùng `numpy`).
  - `northwest_corner(self) -> np.ndarray`: Xây dựng phương án ban đầu (phiên bản nội bộ).
  - `total_cost(self, x) -> float`: Tính `Z`.
  - `solve_moc(self) -> None`: Gọi `least_cost()`, hiển thị kết quả.
  - `solve_nw(self) -> None`: Gọi `northwest_corner()`, hiển thị kết quả.
  - `show_result(self, result=None)`: Điền kết quả vào `Treeview`.
  - `step_once(self) -> None`: [CHƯA RÓ: Hàm này có trong `app.py` nhưng trong `vantai.py` tôi chưa đọc được chính xác. Có thể là wrapper gọi thuật toán đơn giản vì `vantai.py` không có MODI.]
  - `solve_auto(self) -> None`: [CHƯA RÓ: Tương tự, cần đọc chính xác.]
  - `reset_solver(self) -> None`: [CHƯA RÓ.]
  - `load_example5(self)`, `load_image_a(self)`, `load_image_b(self)`: Điền dữ liệu mẫu cứng vào bảng.
  - `clear_all(self)`: Xóa bảng và kết quả.
  - `main()`: Tạo `tk.Tk()` và chạy `mainloop()`.

### 3.7 `data/example_5.csv`, `data/example_a.csv`, `data/example_b.csv`
- **Đường dẫn:** `C:\Users\user\OneDrive\Tài liệu\project\TUTT\data\`
- **Mục đích:** Dữ liệu mẫu để test nhanh.
- **Format:**
  - Các dòng bắt đầu bằng `c_ij` → giá trị ma trận chi phí theo hàng.
  - Dòng `supply` → vector `a_i`.
  - Dòng `demand` → vector `b_j`.
- **Ví dụ `example_5.csv`:**
  ```csv
  c_ij,2,3,6,8,1,4
  c_ij,1,7,2,6,5,2
  c_ij,3,6,1,2,4,5
  c_ij,7,4,3,5,2,1
  supply,70,60,20,30
  demand,10,40,40,50,10,30
  ```

## 4. Luồng thực thi

1. **Entry point:** `main.py` chạy đầu tiên. Hàm `main()` tạo `tk.Tk()`, khởi tạo `TransportationApp(root)` từ `src.gui.app`, gọi `root.mainloop()`.
2. **Khởi tạo UI:** `TransportationApp.__init__` gọi `setup_ui()` để vẽ cửa sổ chính, các khung nhập liệu, nút chức năng và vùng kết quả.
3. **Nhập liệu:** Người dùng chọn `m`, `n`, bấm **"Tạo bảng vận tải"** → gọi `create_table()` tạo ma trận `Entry`. Người dùng điền `C`, `a`, `b` hoặc bấm nút ví dụ / đọc CSV để tự động điền.
4. **Giải phương án cơ sở ban đầu:** Người dùng bấm **"Giải - Cực tiểu cước phí"** hoặc **"Giải - Góc Tây Bắc"**:
   - Gọi `read_input()` → tạo `TransportationData` từ ma trận nhập, gọi `TransportationData.balance_problem()` nếu cần.
   - Tạo `TransportationSolver(data)`.
   - Gọi `solver.find_initial_solution(method)` → thuật toán Least Cost / NW Corner trả về `x` ban đầu và danh sách ô cơ sở.
   - Gọi `show_result()` để hiển thị `x`, chi phí, số ô cơ sở, kiểm tra suy biến.
5. **Tối ưu từng bước (MODI):** Sau khi có phương án cơ sở, người dùng bấm **"Bước tiếp"**:
   - Gọi `solver.optimize_step()`:
     - `check_optimality()`: tính `u_i`, `v_j`, `Δ_ij`. Nếu tối ưu → dừng.
     - Nếu chưa tối ưu: `find_cycle()` tìm chu trình, tính `theta`, điều chỉnh `x`, cập nhật `_basic_cells`.
   - UI cập nhật ma trận kết quả và log bước.
6. **Tối ưu tự động:** Bấm **"Tự động"** → gọi `solver.solve(method)` lặp `optimize_step()` đến khi tối ưu, hiển thị toàn bộ log.
7. **Reset:** Bấm **"Reset"** → gọi `solver.reset()`, xóa kết quả, vô hiệu hóa các nút solver.

## 5. Cấu trúc dữ liệu

| Biến / Cấu trúc | Kiểu dữ liệu | Ý nghĩa | Ví dụ giá trị |
|-----------------|--------------|---------|---------------|
| `a_i` (trong `TransportationData`) | `np.ndarray` (1-D, float) | Lượng phát của trạm phát `i` | `[70, 60, 20, 30]` |
| `b_j` (trong `TransportationData`) | `np.ndarray` (1-D, float) | Lượng thu của trạm thu `j` | `[10, 40, 40, 50, 10, 30]` |
| `c_ij` (trong `TransportationData`) | `np.ndarray` (2-D, float, shape `m x n`) | Ma trận chi phí vận chuyển từ `i` đến `j` | `[[2,3,6,8,1,4], ...]` |
| `x_ij` (trong `TransportationSolver`) | `np.ndarray` (2-D, float, shape `m x n`) | Ma trận phân phối (lượng hàng vận chuyển) | `[[10,0,0,...], ...]` |
| `u_i` | `np.ndarray` (1-D, float) | Thế vị dòng `i` | `[0, -2, 3, ...]` |
| `v_j` | `np.ndarray` (1-D, float) | Thế vị cột `j` | `[2, 5, 1, ...]` |
| `delta_ij` | `np.ndarray` (2-D, float) | Hệ số kiểm tra `Δ_ij = v_j - u_i - c_ij` | `[[-1, 3, 0, ...], ...]` |
| `basic_cells` | `list[tuple[int, int]]` | Tập ô cơ sở hiện tại (các ô `(i,j)` có `x_ij > 0` hoặc được chọn 0) | `[(0,0), (0,5), (1,0), ...]` |
| `steps` | `list[dict[str, Any]]` | Lịch sử từng bước lặp MODI (dùng cho log UI) | `[{'x': ..., 'cost': ..., 'description': ...}, ...]` |
| `balanced_flag` | `bool` | Đánh dấu bài toán gốc có mất cân bằng hay không | `True` nếu đã thêm trạm ảo` |

## 6. Thuật toán cốt lõi

### 6.1 Xây dựng phương án cơ sở ban đầu — Phương pháp chi phí nhỏ nhất (`least_cost`)
```python
def least_cost(self) -> tuple[np.ndarray, list[tuple[int, int]]]:
    sup = self._a.copy()
    dem = self._b.copy()
    m, n = self._m, self._n
    x = np.zeros((m, n), dtype=float)
    row_done = np.zeros(m, dtype=bool)
    col_done = np.zeros(n, dtype=bool)
    basic_cells: list[tuple[int, int]] = []

    while len(basic_cells) < m + n - 1:
        candidates = []
        for i in range(m):
            if row_done[i]:
                continue
            for j in range(n):
                if col_done[j]:
                    continue
                candidates.append({'i': i, 'j': j, 'cost': self._c[i, j]})
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
        elif row_exhausted:
            row_done[i] = True
        elif col_exhausted:
            col_done[j] = True
```
**Giải thích:** Thuật toán duyệt vòng lặp đến khi số ô cơ sở đạt đủ `m + n - 1`. Ở mỗi vòng, tìm ô có chi phí nhỏ nhất trong các hàng/cột chưa bị gạch, phân phối `min(sup[i], dem[j])`. Khi cả hàng và cột cùng hết (suy biến), chỉ gạch hàng, giữ cột để lần sau tạo ô cơ sở `0`.
## 6. Thuật toán cốt lõi

### 6.1 Xây dựng phương án cơ sở ban đầu — Phương pháp chi phí nhỏ nhất (`least_cost`)
```python
def least_cost(self) -> tuple[np.ndarray, list[tuple[int, int]]]:
    sup = self._a.copy()
    dem = self._b.copy()
    m, n = self._m, self._n
    x = np.zeros((m, n), dtype=float)
    row_done = np.zeros(m, dtype=bool)
    col_done = np.zeros(n, dtype=bool)
    basic_cells: list[tuple[int, int]] = []

    while len(basic_cells) < m + n - 1:
        candidates = []
        for i in range(m):
            if row_done[i]:
                continue
            for j in range(n):
                if col_done[j]:
                    continue
                candidates.append({'i': i, 'j': j, 'cost': self._c[i, j]})
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
### 6.2 Xây dựng phương án cơ sở ban đầu — Phương pháp góc Tây Bắc (`northwest_corner`)
```python
def northwest_corner(self) -> tuple[np.ndarray, list[tuple[int, int]]]:
    sup = self._a.copy()
    dem = self._b.copy()
    m, n = self._m, self._n
    x = np.zeros((m, n), dtype=float)
    basic_cells: list[tuple[int, int]] = []
    i, j = 0, 0

    while i < m and j < n:
        amt = min(sup[i], dem[j])
        x[i, j] = amt
        basic_cells.append((i, j))
        sup[i] -= amt
        dem[j] -= amt

        if sup[i] < 1e-12 and dem[j] < 1e-12:
            # SUY BIEN: chi xuong hang, giu nguyen cot de tao o 0
            i += 1
        elif sup[i] < 1e-12:
            i += 1
        elif dem[j] < 1e-12:
            j += 1

    return x, basic_cells
```
**Giải thích:** Bắt đầu từ ô góc trên-trái `(0,0)`, phân phối `min(sup, dem)`. Khi hàng hết thì xuống hàng, khi cột hết thì sang cột. Nếu cả hai cùng hết, chỉ **xuống hàng** (giữ cột) để tạo ô cơ sở `0` phục vụ suy biến.


        row_exhausted = sup[i] < 1e-12
        col_exhausted = dem[j] < 1e-12

        if row_exhausted and col_exhausted:
### 6.3 Kiểm tra tối ưu (`check_optimality`)
```python
def check_optimality(self) -> dict[str, Any]:
    self._ensure_spanning_basis()
    u = np.full(self._m, np.nan)
    v = np.full(self._n, np.nan)
    u[0] = 0.0
    changed = True
    while changed:
        changed = False
        for (i, j) in self._basic_cells:
            if self._x[i, j] > 1e-9:
                if np.isnan(v[j]) and not np.isnan(u[i]):
                    v[j] = self._c[i, j] - u[i]
                    changed = True
                elif np.isnan(u[i]) and not np.isnan(v[j]):
                    u[i] = self._c[i, j] - v[j]
                    changed = True

    delta = np.zeros((self._m, self._n))
    for i in range(self._m):
        for j in range(self._n):
            delta[i, j] = v[j] - u[i] - self._c[i, j]

    max_delta = float(np.max(delta))
    entering = None
    if max_delta > 1e-9:
        entering = tuple(int(x) for x in np.unravel_index(np.argmax(delta), delta.shape))

    return {
        'is_optimal': max_delta <= 1e-9,
        'u': u.tolist(),
        'v': v.tolist(),
        'delta': delta.tolist(),
        'entering_cell': entering,
    }
```
**Giải thích:**
- Đảm bảo tập ô cơ sở liên thông và đủ `m+n-1` bằng Union-Find.
- Đặt `u_0 = 0`, lan truyền qua các ô cơ sở có `x_ij > 0` để tính `v_j = c_ij - u_i` và `u_i = c_ij - v_j`.
- Tính `Δ_ij = v_j - u_i - c_ij` cho mọi ô.
- Nếu `max(Δ) > 1e-9` → chưa tối ưu, chọn ô vào có `Δ` lớn nhất.

            # === SUY BIEN: chi gach hang, giu cot (dem=0) de tao o 0 ===
            row_done[i] = True
        elif row_exhausted:
            row_done[i] = True
        elif col_exhausted:
            col_done[j] = True
```
**Giải thích:** Thuật toán duyệt vòng lặp đến khi số ô cơ sở đạt đủ `m + n - 1`. Ở mỗi vòng, tìm ô có chi phí nhỏ nhất trong các hàng/cột chưa bị gạch, phân phối `min(sup[i], dem[j])`. Khi cả hàng và cột cùng hết (suy biến), chỉ gạch hàng, giữ cột để lần sau tạo ô cơ sở `0`.

### 6.4 Tìm chu trình cải tiến (`find_cycle`) — DFS
```python
def find_cycle(self, entering: tuple[int, int]) -> dict[str, Any]:
    def search(path: list[tuple[int, int]], direction: str) -> list[tuple[int, int]] | None:
        last_i, last_j = path[-1]
        if direction == 'row':
            for (i, j) in self._basic_cells:
                if i == last_i and (i, j) not in path:
                    result = search(path + [(i, j)], 'col')
                    if result:
                        return result
        else:
            for (i, j) in self._basic_cells:
                if j == last_j and (i, j) not in path:
                    result = search(path + [(i, j)], 'row')
                    if result:
                        return result
        if direction == 'col' and last_j == entering[1] and len(path) >= 3:
            return path
        if direction == 'row' and last_i == entering[0] and len(path) >= 3:
            return path
        return None

    path = [entering]
    for first_dir in ('row', 'col'):
        result = search(path, 'col' if first_dir == 'row' else 'row')
        if result:
            return {'loop': result, 'entering': entering}
    return {'loop': None, 'entering': entering, 'error': '...'}
```
**Giải thích:** DFS bắt đầu từ ô vào `entering`, luân phiên duyệt theo hàng (`row`) và cột (`col`). Chỉ đi qua các ô thuộc `_basic_cells`. Khi quay lại đúng hàng hoặc cột của ô vào và độ dài chu trình ≥ 3, trả về chu trình kín.

### 6.5 Điều chỉnh lượng hàng (`optimize_step`)
```python
def optimize_step(self) -> dict[str, Any]:
    if self._x is None:
        raise RuntimeError("Chua co phuong an ban dau...")

    check = self.check_optimality()
    if check['is_optimal']:
        return {'is_optimal': True, 'x': self._x.tolist(), 'cost': self.total_cost(), ...}

    entering = check['entering_cell']
    cyc = self.find_cycle(entering)
    if cyc['loop'] is None:
        return {'is_optimal': False, 'entering_cell': entering, 'error': cyc['error']}

    loop = cyc['loop']
    minus_cells = loop[1::2]
    theta = min(self._x[i, j] for (i, j) in minus_cells)
    leaving = min(minus_cells, key=lambda cell: self._x[cell[0], cell[1]])

    for idx, (i, j) in enumerate(loop):
        sign = 1.0 if idx % 2 == 0 else -1.0
        self._x[i, j] = self._x[i, j] + sign * theta

    self._basic_cells = [cell for cell in self._basic_cells if cell != leaving]
    self._basic_cells.append(entering)

    return {'is_optimal': False, 'x': self._x.tolist(), 'entering_cell': entering,
            'leaving_cell': leaving, 'theta': float(theta), 'loop': loop, ...}
```
**Giải thích:**
- Tập ô vào `entering` (ô có `Δ` max).
- Tìm chu trình `loop`.
- Các ô ở vị trí lẻ (`1, 3, 5, ...`) là ô trừ (`minus_cells`).
- `theta = min(x_ij)` tại các ô trừ. `leaving` là ô có `x_ij = theta`.
- Cập nhật `x`: ô chẵn `+theta`, ô lẻ `-theta`.
- Cập nhật tập ô cơ sở: xóa `leaving`, thêm `entering`.

### 6.6 Điều kiện dừng
```python
for _ in range(max_iter):
    step = self.optimize_step()
    if step.get('is_optimal') or step.get('error'):
        break
```
**Giải thích:** Vòng lặp dừng khi:
- `optimize_step()` trả về `is_optimal = True` (tất cả `Δ_ij <= 1e-9`).
- Hoặc có lỗi (ví dụ không tìm được chu trình).
- Hoặc hết số lần lặp tối đa `max_iter` (mặc định 100).

### 6.7 Xử lý bài toán không cân bằng
```python
def balance_problem(self) -> "TransportationData":
    if self.is_balanced():
        return TransportationData(self._a.copy(), self._b.copy(), self._c.copy())
    diff = self.total_supply - self.total_demand
    if diff > 0:
        new_b = np.append(self._b, diff)
        new_c = np.column_stack([self._c, np.zeros(self.num_supply)])
        return TransportationData(self._a.copy(), new_b, new_c)
    else:
        new_a = np.append(self._a, -diff)
        new_c = np.row_stack([self._c, np.zeros(self.num_demand)])
        return TransportationData(new_a, self._b.copy(), new_c)
```
**Giải thích:** Nếu `Σa_i != Σb_j`, thêm trạm ảo với chi phí `0` vào ma trận `c` để cân bằng. Trạm ảo nằm ở cột cuối (nếu thừa phát) hoặc hàng cuối (nếu thiếu phát).

### 6.8 Xử lý suy biến
- Trong `least_cost` và `northwest_corner`: Khi cả hàng và cột cùng hết, chỉ gạch một chiều (hàng) để đảm bảo số ô cơ sở vẫn đạt `m + n - 1` thông qua việc tạo ô có giá trị `0`.
- Trong `_ensure_spanning_basis()`: Dùng Union-Find đảm bảo tập ô cơ sở liên thông và đủ số ô. Nếu thiếu, bổ sung các ô có `x_ij ≈ 0` (ô 0).
- [CHƯA RÓ: Cần đọc chính xác `_ensure_spanning_basis` để mô tả chi tiết thuật toán Union-Find.]

## 7. Cách chạy

### Yêu cầu
- Python >= 3.11
- pip
- Các package: `numpy==2.5.1`, `pandas==3.0.3` (xem `requirements.txt`).

### Cài đặt
```bash
pip install -r requirements.txt
```

### Chạy ứng dụng
```bash
python main.py
```
Hoặc nếu chạy trực tiếp module:
```bash
python -m src.gui.app
```

### Định dạng dữ liệu đầu vào (CSV)
File CSV phải có cấu trúc:
```csv
c_ij,<cot_1>,<cot_2>,...,<cot_n>
c_ij,<cot_1>,<cot_2>,...,<cot_n>
...
supply,<a_1>,<a_2>,...,<a_m>
demand,<b_1>,<b_2>,...,<b_n>
```
- Mỗi dòng `c_ij` tương ứng 1 hàng của ma trận chi phí.
- Số cột trong mỗi dòng `c_ij` phải bằng nhau.
- Độ dài vector `supply` phải bằng số dòng `c_ij`.
- Độ dài vector `demand` phải bằng số cột của `c_ij`.

**Ví dụ input từ `data/example_5.csv`:**
```csv
c_ij,2,3,6,8,1,4
c_ij,1,7,2,6,5,2
c_ij,3,6,1,2,4,5
c_ij,7,4,3,5,2,1
supply,70,60,20,30
demand,10,40,40,50,10,30
```

## 8. Ví dụ kết quả đầu ra

Kết quả được hiển thị trên giao diện dạng bảng (`Treeview`) và vùng log. Các thông tin chính in ra bao gồm:

- **Tên phương pháp:** `Phương pháp: Least Cost` hoặc `Phương pháp: Northwest Corner`.
- **Tổng chi phí:** `Tổng chi phí Z = <giá trị>`.
- **Bảng nghiệm:** Các cột `A_1 .. A_m`, `B_1 .. B_n`, `a_i`, `b_j`, `x_ij`.
- **Thông tin suy biến:** Nếu số ô cơ sở < `m + n - 1`, hiển thị thông báo suy biến.
- **Log từng bước MODI (nếu chọn Next Step / Auto Solve):** Ví dụ:
  ```
  Ô vào (3, 5), ô rời (1, 5), theta=20.00. Z sau điều chỉnh = 820.00
  Đã tối ưu (Định lý 5.2.2). Z = 720.00
  ```

[CHƯA RÓ: Không có lệnh `print` trực tiếp ra terminal trong code, kết quả được hiển thị hoàn toàn trên GUI.]

## 9. Đánh giá hiện trạng

### 9.1 Phần đã hoàn thiện
- Kiến trúc tách biệt UI (`src/gui/`) và Solver (`src/solver/`), không import `tkinter` trong solver.
- Đọc dữ liệu từ CSV (`TransportationData.from_csv`), kiểm tra cân bằng, cân bằng hóa bài toán.
- Xây dựng phương án cơ sở ban đầu bằng **Least Cost** và **Northwest Corner**, có xử lý suy biến cơ bản.
- Thuật toán **MODI** hoàn chỉnh: tính thế vị `u_i`, `v_j`, hệ số kiểm tra `Δ_ij`, tìm chu trình cải tiến bằng DFS, tính `theta`, điều chỉnh `x_ij`.
- Giao diện Tkinter cho phép nhập liệu, chọn phương pháp, xem từng bước, tự động giải, reset.
- Hỗ trợ load ví dụ mẫu và đọc file CSV.

### 9.2 Phần còn thiếu / code chết / chưa dùng
- File `vantai.py` (~525 dòng) là **legacy**, không được `main.py` sử dụng, có thể xem là code chết / dư thừa.
- Các hàm trong `vantai.py` (`solve_moc`, `solve_nw`, `step_once`, `solve_auto`, `reset_solver`) có bản sao tương tự trong `src/gui/app.py` nhưng phiên bản cũ không có tích hợp MODI từ `src/solver/core`.
- [CHƯA RÓ: Chưa xác định rõ hàm nào trong `vantai.py` thực sự còn được gọi từ nơi khác.]
- Union-Find trong `_ensure_spanning_basis()` chưa được đọc chính xác toàn bộ, cần kiểm tra lại logic.
- Chưa có test đơn vị (unit test) cho `TransportationSolver` và `TransportationData`.
- Chưa có cơ chế xuất kết quả ra file (chỉ hiển thị trên GUI).

### 9.3 Lỗi tiềm ẩn
- **`vantai.py` dòng ~90:** `northwest_corner()` cũ (phiên bản không dùng `numpy`) có thể có lỗi logic suy biến nếu `m` hoặc `n` lớn, nhưng file này không còn được sử dụng nên chỉ là rủi ro kế thừa.
- **`src/solver/core.py` dòng ~446:** `optimize_step()` tính `theta = min(self._x[i, j] for (i, j) in minus_cells)`. Nếu `minus_cells` rỗng (chu trình không hợp lệ) sẽ ném `ValueError: min() arg is an empty sequence`. Tuy nhiên `find_cycle()` đã kiểm tra và trả lỗi nếu `loop is None`, nhưng nếu `loop` có độ dài lẻ hoặc không có ô trừ thì có thể lỗi.
- **`src/gui/app.py`:** Chưa xử lý ngoại lệ khi người dùng nhập giá trị không phải số vào `Entry`, dẫn đến `ValueError` khi `float()` trong `read_input()`.
- **`src/solver/models.py` dòng ~49:** Đọc CSV bằng `path.read_text(encoding="utf-8")` — nếu file có BOM hoặc encoding khác sẽ lỗi.
- **`src/solver/core.py` dòng ~162:** `northwest_corner()` trong khi số ô cơ sở < `m + n - 1` nhưng `i >= m` hoặc `j >= n` có thể dừng sớm, dẫn đến thiếu ô cơ sở. Tuy nhiên logic hiện tại có vẻ đủ cho trường hợp cân bằng.

## 10. Ánh xạ sang báo cáo

| Module / Hàm | Mục báo cáo tương ứng |
|--------------|----------------------|
| `main.py` | Mục 3 (Cấu trúc phần mềm) — Entry point |
| `src/gui/app.py` (class `TransportationApp`) | Mục 3 (Giao diện người dùng) |
| `src/gui/canvas.py` (class `MatrixGrid`) | Mục 3 (Widget hiển thị ma trận) |
| `src/solver/models.py` (class `TransportationData`) | Mục 4.1 (Mô hình bài toán), Mục 4.2 (Dữ liệu đầu vào) |
| `src/solver/core.py`: `least_cost()` | Mục 5.2.1 (Phương pháp cực tiểu cước phí) |
| `src/solver/core.py`: `northwest_corner()` | Mục 5.2.2 (Phương pháp góc Tây Bắc) |
| `src/solver/core.py`: `find_initial_solution()` | Mục 5.2 (Xây dựng phương án cơ sở) |
| `src/solver/core.py`: `_ensure_spanning_basis()` | Mục 5.2.3 (Xử lý suy biến) |
| `src/solver/core.py`: `calculate_potentials()` | Mục 5.3.1 (Tính thế vị u_i, v_j) |
| `src/solver/core.py`: `check_optimality()` | Mục 5.3.2 (Kiểm tra điều kiện tối ưu — Định lý 5.2.2) |
| `src/solver/core.py`: `find_cycle()` | Mục 5.4.1 (Tìm chu trình điều chỉnh) |
| `src/solver/core.py`: `optimize_step()` | Mục 5.4.2 (Điều chỉnh lượng hàng — theta) |
| `src/solver/core.py`: `solve()` | Mục 5.5 (Quy trình giải tổng quát) |
| `src/solver/models.py`: `balance_problem()` | Mục 5.1.2 (Xử lý bài toán không cân bằng) |
