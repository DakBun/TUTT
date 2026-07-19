# Đồ án Tối ưu tuyến tính — Trực quan hóa thuật toán giải Bài toán vận tải

## Mục tiêu
Xây dựng ứng dụng desktop bằng Python & Tkinter để **giải và trực quan hóa từng bước** bài toán vận tải:
- **Bài toán cân bằng thu/phát** (∑a_i = ∑b_j).
- **Bài toán không cân bằng thu/phát** (thêm trạm phát ảo hoặc trạm thu ảo để đưa về cân bằng).

Ứng dụng hiển thị ma trận cước phí, phương án vận tải, thế vị, hệ số kiểm tra delta, và cho phép người dùng tương tác từng bước (Next Step, Reset).

## Kiến trúc
- **Tách biệt hoàn toàn UI và Solver** — không import 	kinter trong module solver/.
- src/gui/: giao diện Tkinter (MatrixGrid, TransportationApp).
- src/solver/: logic thuật toán thuần Python + NumPy (TransportationData, TransportationSolver).
- data/: chứa file dữ liệu mẫu (nếu có).

## Cấu trúc thư mục

```
├── .clinerules              
├── .gitignore
├── README.md
├── requirements.txt          
├── main.py                   
├── data/                  
├── src/
│   ├── __init__.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py            
│   │   └── canvas.py         
│   └── solver/
│       ├── __init__.py
│       ├── models.py         
│       └── core.py          
```

## Hướng dẫn cài đặt & chạy

### Yêu cầu
- Python ≥ 3.11
- pip
- numpy
- pandas
