"""
app.py - Cua so chinh cua ung dung truc quan hoa bai toan van tai.

Giu nguyen giao dien tu file vantai.py goc (mau sac, font, bo cuc).
Cac nut bam goi den TransportationData (doc CSV) va TransportationSolver.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from src.solver.models import TransportationData
from src.solver.core import TransportationSolver


class TransportationApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Chuong 5 - Bai toan Van tai - Nhom 6')
        self.root.geometry('1200x700')

        self.m = 4
        self.n = 6
        self.c = []
        self.supply = []
        self.demand = []
        self.x = []

        self.solver = None

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(title_frame, text='Chuong 5: Bai toan Van tai',
                 font=('Segoe UI', 16, 'bold'), fg='#0d47a1').pack()
        tk.Label(title_frame, text='Trinh bay: Nhom 6',
                 font=('Segoe UI', 10), fg='#555').pack()

        # Theory summary
        theory_frame = tk.LabelFrame(self.root, text=' Tom tat ly thuyet nhanh ',
                                     font=('Segoe UI', 10, 'bold'), fg='#1565c0')
        theory_frame.pack(fill=tk.X, padx=10, pady=5)

        theory_left = tk.Frame(theory_frame)
        theory_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(theory_left, text='Mo hinh: Z = min SumSum c_ij * x_ij',
                 font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W)
        tk.Label(theory_left, text='. Du tru: Sum x_ij = a_i (voi moi i)',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=10)
        tk.Label(theory_left, text='. Nhu cau: Sum x_ij = b_j (voi moi j)',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=10)
        tk.Label(theory_left, text='. Can bang: Sum a_i = Sum b_j',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=10)
        tk.Label(theory_left, text='Luu y: Phan mem lap phuong an co ban ban dau, sau do kiem tra so o co ban co du m + n - 1.',
                 font=('Segoe UI', 8), fg='#666').pack(anchor=tk.W, pady=2)

        theory_right = tk.Frame(theory_frame, bg='#eef2f7', padx=10, pady=5)
        theory_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(theory_right, text='Vi du mau - Vi du 5', font=('Segoe UI', 9, 'bold'),
                 bg='#eef2f7').pack(anchor=tk.W)
        example_text = 'a = [70, 60, 20, 30]\nb = [10, 40, 40, 50, 10, 30]\nC = [2 3 6 8 1 4; 1 7 2 6 5 2;\n     3 6 1 2 4 5; 7 4 3 5 2 1]'
        tk.Label(theory_right, text=example_text, font=('Consolas', 9),
                 bg='#eef2f7', justify=tk.LEFT).pack(anchor=tk.W, pady=2)
        tk.Label(theory_right, text='-> Bam "Vi du 5" roi "Giai"',
                 font=('Segoe UI', 8), fg='#c43e00', bg='#eef2f7').pack(anchor=tk.W)

        # Input section
        input_frame = tk.LabelFrame(self.root, text=' 1. Nhap du lieu bai toan ',
                                    font=('Segoe UI', 10, 'bold'), fg='#1565c0')
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        control_frame = tk.Frame(input_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(control_frame, text='So tram phat (m):', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        self.m_var = tk.IntVar(value=4)
        tk.Spinbox(control_frame, from_=2, to=10, textvariable=self.m_var, width=5,
                  font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text='So tram thu (n):', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        self.n_var = tk.IntVar(value=6)
        tk.Spinbox(control_frame, from_=2, to=10, textvariable=self.n_var, width=5,
                  font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text='Tao bang van tai', command=self.create_table,
                 bg='#1565c0', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=10, pady=2, cursor='hand2').pack(side=tk.LEFT, padx=10)
        tk.Label(control_frame, text='Chon m, n roi bam tao bang de nhap C, a, b.',
                 font=('Segoe UI', 8), fg='#666').pack(side=tk.LEFT, padx=5)

        # Matrix table area
        self.table_frame = tk.Frame(input_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text='Giai - Cuc tieu cuoc phi', command=self.solve_moc,
                 bg='#2e7d32', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Giai - Goc tren-trai', command=self.solve_nw,
                 bg='#6a1b9a', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Vi du 5', command=self.load_example5,
                 bg='#ef6c00', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Vi du (a)', command=self.load_image_a,
                 bg='#00838f', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Vi du (b)', command=self.load_image_b,
                 bg='#00695c', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Xoa', command=self.clear_all,
                 bg='#c62828', fg='white', font=('Segoe UI', 9, 'bold'),
                 padx=12, pady=4, cursor='hand2').pack(side=tk.LEFT, padx=4)

        # Result section
        result_frame = tk.LabelFrame(self.root, text=' 2. Ket qua giai & Lich su buoc ',
                                     font=('Segoe UI', 10, 'bold'), fg='#1565c0')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Summary bar
        self.summary_frame = tk.Frame(result_frame, bg='#e3f2fd', highlightbackground='#90caf9',
                                      highlightthickness=1)
        self.summary_frame.pack(fill=tk.X, padx=5, pady=(5, 2))

        self.lbl_method = tk.Label(self.summary_frame, text='Phuong phap: --',
                                   font=('Segoe UI', 11, 'bold'), bg='#e3f2fd', fg='#1565c0')
        self.lbl_method.pack(side=tk.LEFT, padx=10, pady=6)

        self.lbl_cost = tk.Label(self.summary_frame, text='Tong chi phi Z = --',
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

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=28,
                             background='#ffffff', fieldbackground='#ffffff')
        self.style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'),
                             background='#1565c0', foreground='white')
        self.style.map('Treeview.Heading', background=[('active', '#1976d2')])
        self.style.map('Treeview', background=[('selected', '#bbdefb')])

        # Info label
        self.lbl_info = tk.Label(result_frame, text='Chua co ket qua. Hay nhap du lieu va bam "Giai".',
                                 font=('Segoe UI', 9), fg='#555', bg='#fff8e1',
                                 anchor=tk.W, padx=10, pady=4)
        self.lbl_info.pack(fill=tk.X, padx=5, pady=(0, 5))

    # ------------------------------------------------------------------
    # Tao bang nhap lieu
    # ------------------------------------------------------------------

    def create_table(self):
        self.m = self.m_var.get()
        self.n = self.n_var.get()
        if self.m < 2 or self.n < 2:
            messagebox.showwarning('Loi', 'm, n phai >= 2')
            return

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.table_frame)
        frame.pack()

        # Header
        tk.Label(frame, text='i\\j', bg='#1565c0', fg='white', width=6, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='nsew')
        for j in range(self.n):
            tk.Label(frame, text=f'B_{j+1}', bg='#1565c0', fg='white', width=8, relief=tk.RIDGE,
                    font=('Segoe UI', 9, 'bold')).grid(row=0, column=j+1, sticky='nsew')
        tk.Label(frame, text='a_i', bg='#1565c0', fg='white', width=8, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=0, column=self.n+1, sticky='nsew')

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

        tk.Label(frame, text='Sum = Sum', bg='#e8f5e9', width=8, relief=tk.RIDGE,
                font=('Segoe UI', 9, 'bold')).grid(row=self.m+1, column=self.n+1, sticky='nsew')

        for i in range(self.m + 2):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(self.n + 2):
            frame.grid_columnconfigure(j, weight=1)

        self.lbl_method.config(text='Phuong phap: --')
        self.lbl_cost.config(text='Tong chi phi Z = --')
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree['columns'] = []
        self.lbl_info.config(text='Da tao bang moi. Nhap du lieu va bam "Giai".',
                             bg='#fff8e1', fg='#555')

    # ------------------------------------------------------------------
    # Doc du lieu tu bang Entry
    # ------------------------------------------------------------------

    def read_input(self):
        """Doc du lieu tu bang Entry, xu ly can bang, tao Solver."""
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

        import numpy as np
        data = TransportationData(
            a=np.array(self.supply, dtype=float),
            b=np.array(self.demand, dtype=float),
            c=np.array(self.c, dtype=float),
        )

        # Kiem tra can bang
        if not data.is_balanced():
            total_sup = data.total_supply
            total_dem = data.total_demand
            diff = abs(total_sup - total_dem)
            if total_sup > total_dem:
                msg = f'Da tu can bang: Tong phat {total_sup} > Tong thu {total_dem}, them tram thu ao voi luong {diff:.2f}.'
            else:
                msg = f'Da tu can bang: Tong thu {total_dem} > Tong phat {total_sup}, them tram phat ao voi luong {diff:.2f}.'
            messagebox.showinfo('Can bang', msg)

        self.solver = TransportationSolver(data)

    # ------------------------------------------------------------------
    # Cac lenh giai
    # ------------------------------------------------------------------

    def solve_moc(self):
        self.read_input()
        if self.solver is None:
            return
        result = self.solver.find_initial_solution('least_cost')
        self.x = result['x']
        self.show_result('Cuc tieu cuoc phi', result)

    def solve_nw(self):
        self.read_input()
        if self.solver is None:
            return
        result = self.solver.find_initial_solution('northwest_corner')
        self.x = result['x']
        self.show_result('Goc tren-trai', result)

    # ------------------------------------------------------------------
    # Hien thi ket qua
    # ------------------------------------------------------------------

    def fmt(self, n):
        return f'{n:.2f}'

    def show_result(self, method_name, result=None):
        if result is None:
            alloc = [row[:] for row in self.x]
            basic_count = sum(1 for i in range(self.m) for j in range(self.n) if alloc[i][j] > 0)
            need = self.m + self.n - 1
            padded = basic_count < need
            cost = sum(alloc[i][j] * self.c[i][j] for i in range(self.m) for j in range(self.n))
        else:
            alloc = result['x']
            self.m = len(alloc)
            self.n = len(alloc[0]) if alloc else 0
            basic_count = result['basic_count']
            need = result['need']
            padded = result['padded']
            cost = result['cost']
            self.c = result.get('c', self.c)


        self.lbl_method.config(text=f'Phuong phap: {method_name}')
        self.lbl_cost.config(text=f'Tong chi phi Z = {self.fmt(cost)}')

        columns = ['col_label'] + [f'col_{j}' for j in range(self.n)] + ['col_sup']
        self.result_tree['columns'] = columns

        self.result_tree.column('col_label', width=60, minwidth=50, anchor=tk.CENTER, stretch=False)
        for j in range(self.n):
            self.result_tree.column(f'col_{j}', width=90, minwidth=70, anchor=tk.CENTER)
        self.result_tree.column('col_sup', width=80, minwidth=60, anchor=tk.CENTER, stretch=False)

        self.result_tree.heading('col_label', text='i\\j')
        for j in range(self.n):
            self.result_tree.heading(f'col_{j}', text=f'B_{j+1}')
        self.result_tree.heading('col_sup', text='a_i')

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.result_tree.tag_configure('row_even', background='#f5f9ff')
        self.result_tree.tag_configure('row_odd', background='#ffffff')
        self.result_tree.tag_configure('row_total', background='#e8f5e9', font=('Segoe UI', 9, 'bold'))

        for i in range(self.m):
            values = [f'A_{i+1}']
            for j in range(self.n):
                values.append(self.fmt(alloc[i][j]))
            values.append('-')
            tag = 'row_even' if i % 2 == 0 else 'row_odd'
            self.result_tree.insert('', tk.END, values=values, tags=(tag,))

        dem_values = ['b_j']
        for j in range(self.n):
            dem_values.append('-')
        dem_values.append('Sum=Sum')
        self.result_tree.insert('', tk.END, values=dem_values, tags=('row_total',))

        status_icon = 'OK' if not padded else '!!'
        info = f'{status_icon} So o co ban: {basic_count} / can >= {need} (m + n - 1). '
        info += 'Da them o 0 de du so o co ban.' if padded else 'Da du so o co ban.'
        bg_color = '#e8f5e9' if not padded else '#fff3e0'
        fg_color = '#2e7d32' if not padded else '#e65100'
        self.lbl_info.config(text=info, bg=bg_color, fg=fg_color)

    # ------------------------------------------------------------------
    # Nap du lieu tu CSV
    # ------------------------------------------------------------------

    def _load_from_csv(self, path: str, title: str):
        """Nap du lieu tu file CSV, tao bang va hien thi."""
        import numpy as np
        data = TransportationData.from_csv(path)
        self.m_var.set(data.num_supply)
        self.n_var.set(data.num_demand)
        self.create_table()

        # Fill entries
        c_vals = data.c.tolist()
        a_vals = data.a.tolist()
        b_vals = data.b.tolist()

        for i in range(self.m):
            for j in range(self.n):
                self.c_entries[i][j].delete(0, tk.END)
                self.c_entries[i][j].insert(0, str(c_vals[i][j]))
            self.sup_entries[i].delete(0, tk.END)
            self.sup_entries[i].insert(0, str(a_vals[i]))

        for j in range(self.n):
            self.dem_entries[j].delete(0, tk.END)
            self.dem_entries[j].insert(0, str(b_vals[j]))

        messagebox.showinfo(title, f'Da dien san du lieu {title}. Bam "Giai" de xem ket qua.')

    def load_example5(self):
        csv_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'example_5.csv'
        if not csv_path.exists():
            csv_path = Path('data/example_5.csv')
        self._load_from_csv(str(csv_path), 'Vi du 5')

    def load_image_a(self):
        csv_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'example_a.csv'
        if not csv_path.exists():
            csv_path = Path('data/example_a.csv')
        self._load_from_csv(str(csv_path), 'Anh (a)')

    def load_image_b(self):
        csv_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'example_b.csv'
        if not csv_path.exists():
            csv_path = Path('data/example_b.csv')
        self._load_from_csv(str(csv_path), 'Anh (b)')

    # ------------------------------------------------------------------
    # Xoa
    # ------------------------------------------------------------------

    def clear_all(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.c_entries = []
        self.sup_entries = []
        self.dem_entries = []
        self.x = []
        self.solver = None

        self.lbl_method.config(text='Phuong phap: --')
        self.lbl_cost.config(text='Tong chi phi Z = --')
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree['columns'] = []
        self.lbl_info.config(text='Chua co ket qua. Hay nhap du lieu va bam "Giai".',
                             bg='#fff8e1', fg='#555')


def main():
    root = tk.Tk()
    app = TransportationApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
