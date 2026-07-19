import tkinter as tk
from tkinter import ttk, messagebox

class TransportationApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Chương 5 - Bài toán Vận tải - Nhóm 6')
        self.root.geometry('1200x700')

        self.m = 4
        self.n = 6
        self.c = []
        self.supply = []
        self.demand = []
        self.x = []

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(title_frame, text='Chương 5: Bài toán Vận tải',
                 font=('Segoe UI', 16, 'bold'), fg='#0d47a1').pack()
        tk.Label(title_frame, text='Trình bày: Nhóm 6',
                 font=('Segoe UI', 10), fg='#555').pack()

        # Theory summary
        theory_frame = tk.LabelFrame(self.root, text=' Tóm tắt lý thuyết nhanh ',
                                     font=('Segoe UI', 10, 'bold'), fg='#1565c0')
        theory_frame.pack(fill=tk.X, padx=10, pady=5)

        theory_left = tk.Frame(theory_frame)
        theory_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(theory_left, text='Mô hình: Z = min ΣΣ c_ij * x_ij',
                 font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W)
        tk.Label(theory_left, text='• Dự trữ: Σ x_ij = a_i  (với mỗi i)',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=10)
        tk.Label(theory_left, text='• Nhu cầu: Σ x_ij = b_j  (với mỗi j)',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=10)
        tk.Label(theory_left, text='• Cân bằng: Σ a_i = Σ b_j',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=10)
        tk.Label(theory_left, text='Lưu ý: Phần mềm lập phương án cơ bản ban đầu, sau đó kiểm tra số ô cơ bản có đủ m + n − 1.',
                 font=('Segoe UI', 8), fg='#666').pack(anchor=tk.W, pady=2)

        theory_right = tk.Frame(theory_frame, bg='#eef2f7', padx=10, pady=5)
        theory_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(theory_right, text='Ví dụ mẫu – Ví dụ 5', font=('Segoe UI', 9, 'bold'),
                 bg='#eef2f7').pack(anchor=tk.W)
        example_text = 'a = [70, 60, 20, 30]\nb = [10, 40, 40, 50, 10, 30]\nC = [2 3 6 8 1 4; 1 7 2 6 5 2;\n     3 6 1 2 4 5; 7 4 3 5 2 1]'
        tk.Label(theory_right, text=example_text, font=('Consolas', 9),
                 bg='#eef2f7', justify=tk.LEFT).pack(anchor=tk.W, pady=2)
        tk.Label(theory_right, text='→ Bấm "Ví dụ 5" rồi "Giải"',
                 font=('Segoe UI', 8), fg='#c43e00', bg='#eef2f7').pack(anchor=tk.W)

        # Input section
        input_frame = tk.LabelFrame(self.root, text=' 1. Nhập dữ liệu bài toán ',
                                    font=('Segoe UI', 10, 'bold'), fg='#1565c0')
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        control_frame = tk.Frame(input_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(control_frame, text='Số trạm phát (m):', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        self.m_var = tk.IntVar(value=4)
        tk.Spinbox(control_frame, from_=2, to=10, textvariable=self.m_var, width=5,
                  font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text='Số trạm thu (n):', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        self.n_var = tk.IntVar(value=6)
        tk.Spinbox(control_frame, from_=2, to=10, textvariable=self.n_var, width=5,
                  font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text='Tạo bảng vận tải', command=self.create_table,
                 bg='#1565c0', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=10, pady=2, cursor='hand2').pack(side=tk.LEFT, padx=10)
        tk.Label(control_frame, text='Chọn m, n rồi bấm tạo bảng để nhập C, a, b.',
                 font=('Segoe UI', 8), fg='#666').pack(side=tk.LEFT, padx=5)

        # Matrix table area
        self.table_frame = tk.Frame(input_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text='Giải – Cực tiểu cước phí', command=self.solve_moc,
                 bg='#2e7d32', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Giải – Góc trên-trái', command=self.solve_nw,
                 bg='#6a1b9a', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Ví dụ 5', command=self.load_example5,
                 bg='#ef6c00', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Ví dụ (a)', command=self.load_image_a,
                 bg='#00838f', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Ví dụ (b)', command=self.load_image_b,
                 bg='#00695c', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Xóa', command=self.clear_all,
                 bg='#c62828', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)

        # Result section
        result_frame = tk.LabelFrame(self.root, text=' 2. Kết quả giải & Lịch sử bước ',
                                     font=('Segoe UI', 10, 'bold'), fg='#1565c0')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Summary bar: method name + total cost
        self.summary_frame = tk.Frame(result_frame, bg='#e3f2fd', highlightbackground='#90caf9',
                                      highlightthickness=1)
        self.summary_frame.pack(fill=tk.X, padx=5, pady=(5, 2))

        self.lbl_method = tk.Label(self.summary_frame, text='⏳ Phương pháp: --',
                                   font=('Segoe UI', 10, 'bold'), bg='#e3f2fd', fg='#0d47a1')
        self.lbl_method.pack(side=tk.LEFT, padx=10, pady=6)

        self.lbl_cost = tk.Label(self.summary_frame, text='💰 Tổng chi phí Z = --',
                                 font=('Segoe UI', 12, 'bold'), bg='#e3f2fd', fg='#c62828')
        self.lbl_cost.pack(side=tk.RIGHT, padx=10, pady=6)

        # Treeview table for result
        table_container = tk.Frame(result_frame)
        table_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        self.result_tree = ttk.Treeview(table_container, show='headings', height=8)
        vsb = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.result_tree.yview)
        hsb = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.result_tree.xview)
        self.result_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.result_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Style for Treeview
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=28,
                             background='#ffffff', fieldbackground='#ffffff')
        self.style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'),
                             background='#1565c0', foreground='white')
        self.style.map('Treeview.Heading', background=[('active', '#1976d2')])
        self.style.map('Treeview', background=[('selected', '#bbdefb')])

        # Info label
        self.lbl_info = tk.Label(result_frame, text='ℹ️ Chưa có kết quả. Hãy nhập dữ liệu và bấm "Giải".',
                                 font=('Segoe UI', 9), fg='#555', bg='#fff8e1',
                                 anchor=tk.W, padx=10, pady=4)
        self.lbl_info.pack(fill=tk.X, padx=5, pady=(0, 5))

    def create_table(self):
        self.m = self.m_var.get()
        self.n = self.n_var.get()
        if self.m < 2 or self.n < 2:
            messagebox.showwarning('Lỗi', 'm, n phải >= 2')
            return

        # Clear old table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create new table
        frame = tk.Frame(self.table_frame)
        frame.pack()

        # Header row
        tk.Label(frame, text='i\\j', bg='#1565c0', fg='white', width=6, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='nsew')
        for j in range(self.n):
            tk.Label(frame, text=f'B_{j+1}', bg='#1565c0', fg='white', width=8, relief=tk.RIDGE,
                    font=('Segoe UI', 9, 'bold')).grid(row=0, column=j+1, sticky='nsew')
        tk.Label(frame, text='a_i', bg='#1565c0', fg='white', width=8, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=0, column=self.n+1, sticky='nsew')

        # Input cells
        self.c_entries = []
        self.sup_entries = []
        self.dem_entries = []

        for i in range(self.m):
            tk.Label(frame, text=f'A_{i+1}', bg='#1565c0', fg='white', width=6, relief=tk.RIDGE,
                    font=('Segoe UI', 9, 'bold')).grid(row=i+1, column=0, sticky='nsew')
            row_entries = []
            for j in range(self.n):
                e = tk.Entry(frame, width=8, font=('Segoe UI', 9), justify=tk.CENTER)
                e.insert(0, '0')
                e.grid(row=i+1, column=j+1, padx=1, pady=1, sticky='nsew')
                row_entries.append(e)
            self.c_entries.append(row_entries)

            e = tk.Entry(frame, width=8, font=('Segoe UI', 9), justify=tk.CENTER)
            e.insert(0, '0')
            e.grid(row=i+1, column=self.n+1, padx=1, pady=1, sticky='nsew')
            self.sup_entries.append(e)

        # Demand row
        tk.Label(frame, text='b_j', bg='#1565c0', fg='white', width=6, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=self.m+1, column=0, sticky='nsew')
        dem_row = []
        for j in range(self.n):
            e = tk.Entry(frame, width=8, font=('Segoe UI', 9), justify=tk.CENTER)
            e.insert(0, '0')
            e.grid(row=self.m+1, column=j+1, padx=1, pady=1, sticky='nsew')
            dem_row.append(e)
        self.dem_entries = dem_row

        tk.Label(frame, text='Σ = Σ', bg='#e8f5e9', width=8, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=self.m+1, column=self.n+1, sticky='nsew')

        # Configure grid weights
        for i in range(self.m + 2):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(self.n + 2):
            frame.grid_columnconfigure(j, weight=1)

        self.lbl_method.config(text='⏳ Phương pháp: --')
        self.lbl_cost.config(text='💰 Tổng chi phí Z = --')
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree['columns'] = []
        self.lbl_info.config(text='ℹ️ Đã tạo bảng mới. Nhập dữ liệu và bấm "Giải".',
                             bg='#fff8e1', fg='#555')

    def read_input(self):
        self.c = []
        self.supply = []
        self.demand = []

        for i in range(self.m):
            row = []
            for j in range(self.n):
                try:
                    val = float(self.c_entries[i][j].get())
                except ValueError:
                    val = 0.0
                row.append(val)
            self.c.append(row)

        for i in range(self.m):
            try:
                val = float(self.sup_entries[i].get())
            except ValueError:
                val = 0.0
            self.supply.append(val)

        for j in range(self.n):
            try:
                val = float(self.dem_entries[j].get())
            except ValueError:
                val = 0.0
            self.demand.append(val)

        total_sup = sum(self.supply)
        total_dem = sum(self.demand)
        if abs(total_sup - total_dem) > 1e-9:
            if total_sup > total_dem:
                dummy_demand = total_sup - total_dem
                self.demand.append(dummy_demand)
                for i in range(self.m):
                    self.c[i].append(0.0)
                self.n += 1
            else:
                dummy_supply = total_dem - total_sup
                self.supply.append(dummy_supply)
                self.c.append([0.0] * self.n)
                self.m += 1
            messagebox.showinfo('Cân bằng', f'Đã tự cân bằng: Tổng phát = {total_sup}, Tổng thu = {sum(self.demand)} (đã thêm dòng/cột giả).')

    def fmt(self, n):
        return f'{n:.2f}'

    def least_cost(self):
        sup = self.supply[:]
        dem = self.demand[:]
        x = [[0.0] * self.n for _ in range(self.m)]
        used = [[False] * self.n for _ in range(self.m)]

        remaining = self.m * self.n
        while remaining > 0:
            candidates = []
            for i in range(self.m):
                if sup[i] <= 0:
                    continue
                for j in range(self.n):
                    if dem[j] <= 0 or used[i][j]:
                        continue
                    candidates.append({
                        'i': i, 'j': j,
                        'cost': self.c[i][j],
                        'amt': min(sup[i], dem[j])
                    })
            if not candidates:
                break

            candidates.sort(key=lambda x: (x['cost'], -x['amt']))
            best = candidates[0]
            i, j = best['i'], best['j']
            amt = min(sup[i], dem[j])
            x[i][j] = amt
            sup[i] -= amt
            dem[j] -= amt
            used[i][j] = True
            if sup[i] <= 0:
                for jj in range(self.n):
                    used[i][jj] = True
            if dem[j] <= 0:
                for ii in range(self.m):
                    used[ii][j] = True
            remaining -= 1

        return x

    def northwest_corner(self):
        sup = self.supply[:]
        dem = self.demand[:]
        x = [[0.0] * self.n for _ in range(self.m)]
        i, j = 0, 0
        while i < self.m and j < self.n:
            amt = min(sup[i], dem[j])
            x[i][j] = amt
            sup[i] -= amt
            dem[j] -= amt
            if sup[i] == 0:
                i += 1
            else:
                j += 1
        return x

    def total_cost(self, alloc):
        cost = 0.0
        for i in range(self.m):
            for j in range(self.n):
                cost += alloc[i][j] * self.c[i][j]
        return cost

    def solve_moc(self):
        self.read_input()
        self.x = self.least_cost()
        self.show_result('Cực tiểu cước phí')

    def solve_nw(self):
        self.read_input()
        self.x = self.northwest_corner()
        self.show_result('Góc trên-trái')

    def show_result(self, method_name):
        alloc = [row[:] for row in self.x]
        basic_count = sum(1 for i in range(self.m) for j in range(self.n) if alloc[i][j] > 0)
        need = self.m + self.n - 1
        padded = basic_count < need

        if padded:
            for i in range(self.m):
                for j in range(self.n):
                    if alloc[i][j] == 0 and basic_count < need:
                        alloc[i][j] = 0.0
                        basic_count += 1

        cost = self.total_cost(alloc)

        # Update summary bar
        self.lbl_method.config(text=f'📊 Phương pháp: {method_name}')
        self.lbl_cost.config(text=f'💰 Tổng chi phí Z = {self.fmt(cost)}')

        # Build columns for Treeview: i\j | B_1 ... B_n | a_i
        columns = ['col_label'] + [f'col_{j}' for j in range(self.n)] + ['col_sup']

        self.result_tree['columns'] = columns

        # Configure columns
        self.result_tree.column('col_label', width=60, minwidth=50, anchor=tk.CENTER, stretch=False)
        for j in range(self.n):
            self.result_tree.column(f'col_{j}', width=90, minwidth=70, anchor=tk.CENTER)
        self.result_tree.column('col_sup', width=80, minwidth=60, anchor=tk.CENTER, stretch=False)

        # Configure headings
        self.result_tree.heading('col_label', text='i\\j')
        for j in range(self.n):
            self.result_tree.heading(f'col_{j}', text=f'B_{j+1}')
        self.result_tree.heading('col_sup', text='a_i')

        # Clear old rows
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # Tags for alternating row colors
        self.result_tree.tag_configure('row_even', background='#f5f9ff')
        self.result_tree.tag_configure('row_odd', background='#ffffff')
        self.result_tree.tag_configure('row_total', background='#e8f5e9', font=('Segoe UI', 9, 'bold'))

        # Insert data rows
        for i in range(self.m):
            values = [f'A_{i+1}']
            for j in range(self.n):
                values.append(self.fmt(alloc[i][j]))
            values.append('−')  # supply column shows dash
            tag = 'row_even' if i % 2 == 0 else 'row_odd'
            self.result_tree.insert('', tk.END, values=values, tags=(tag,))

        # Insert demand row
        dem_values = ['b_j']
        for j in range(self.n):
            dem_values.append('−')
        dem_values.append('Σ=Σ')
        self.result_tree.insert('', tk.END, values=dem_values, tags=('row_total',))

        # Update info label
        status_icon = '✅' if not padded else '⚠️'
        info = f'{status_icon} Số ô cơ bản: {basic_count} / cần ≥ {need} (m + n - 1). '
        info += 'Đã thêm ô 0 để đủ số ô cơ bản.' if padded else 'Đã đủ số ô cơ bản.'
        bg_color = '#e8f5e9' if not padded else '#fff3e0'
        fg_color = '#2e7d32' if not padded else '#e65100'
        self.lbl_info.config(text=info, bg=bg_color, fg=fg_color)

    def load_example5(self):
        self.m_var.set(4)
        self.n_var.set(6)
        self.create_table()

        # Fill example data
        c_vals = [
            [2, 3, 6, 8, 1, 4],
            [1, 7, 2, 6, 5, 2],
            [3, 6, 1, 2, 4, 5],
            [7, 4, 3, 5, 2, 1]
        ]
        a_vals = [70, 60, 20, 30]
        b_vals = [10, 40, 40, 50, 10, 30]

        for i in range(self.m):
            for j in range(self.n):
                self.c_entries[i][j].delete(0, tk.END)
                self.c_entries[i][j].insert(0, str(c_vals[i][j]))
            self.sup_entries[i].delete(0, tk.END)
            self.sup_entries[i].insert(0, str(a_vals[i]))

        for j in range(self.n):
            self.dem_entries[j].delete(0, tk.END)
            self.dem_entries[j].insert(0, str(b_vals[j]))

        messagebox.showinfo('Ví dụ 5', 'Đã điền sẵn dữ liệu Ví dụ 5. Bấm "Giải" để xem kết quả.')

    def load_image_a(self):
        self.m_var.set(4)
        self.n_var.set(5)
        self.create_table()
        c_vals = [
            [7, 4, 17, 5, 8],
            [8, 9, 10, 4, 20],
            [13, 6, 14, 16, 30],
            [44, 29, 18, 26, 35],
        ]
        a_vals = [50, 200, 100, 200]
        b_vals = [150, 80, 180, 60, 80]

        for i in range(self.m):
            for j in range(self.n):
                self.c_entries[i][j].delete(0, tk.END)
                self.c_entries[i][j].insert(0, str(c_vals[i][j]))
            self.sup_entries[i].delete(0, tk.END)
            self.sup_entries[i].insert(0, str(a_vals[i]))

        for j in range(self.n):
            self.dem_entries[j].delete(0, tk.END)
            self.dem_entries[j].insert(0, str(b_vals[j]))

        messagebox.showinfo('Ảnh (a)', 'Đã điền sẵn dữ liệu từ ảnh a. Bấm "Giải" để xem kết quả.')

    def load_image_b(self):
        self.m_var.set(4)
        self.n_var.set(5)
        self.create_table()
        c_vals = [
            [10, 7, 4, 1, 4],
            [2, 7, 10, 6, 11],
            [8, 5, 3, 2, 2],
            [11, 8, 12, 16, 13],
        ]
        a_vals = [100, 250, 200, 300]
        b_vals = [200, 200, 100, 100, 150]

        for i in range(self.m):
            for j in range(self.n):
                self.c_entries[i][j].delete(0, tk.END)
                self.c_entries[i][j].insert(0, str(c_vals[i][j]))
            self.sup_entries[i].delete(0, tk.END)
            self.sup_entries[i].insert(0, str(a_vals[i]))

        for j in range(self.n):
            self.dem_entries[j].delete(0, tk.END)
            self.dem_entries[j].insert(0, str(b_vals[j]))

        messagebox.showinfo('Ví dụ (b)', 'Đã điền sẵn dữ liệu từ ảnh b. Bấm "Giải" để xem kết quả.')

    def clear_all(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.c_entries = []
        self.sup_entries = []
        self.dem_entries = []
        self.x = []

        # Clear result display
        self.lbl_method.config(text='⏳ Phương pháp: --')
        self.lbl_cost.config(text='💰 Tổng chi phí Z = --')
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree['columns'] = []
        self.lbl_info.config(text='ℹ️ Chưa có kết quả. Hãy nhập dữ liệu và bấm "Giải".',
                             bg='#fff8e1', fg='#555')


def main():
    root = tk.Tk()
    app = TransportationApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
