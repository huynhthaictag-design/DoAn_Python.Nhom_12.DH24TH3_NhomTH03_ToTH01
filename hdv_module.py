# hdv_module.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import mysql.connector

from database import conn, check_db_connection 

class HDVManager:
    """Quản lý giao diện, dữ liệu và logic CRUD cho Tab Hướng Dẫn Viên."""

    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.root = parent_tab.winfo_toplevel()
        
        # Gọi hàm tạo giao diện
        self._create_widgets()
        
        # Tải dữ liệu ban đầu
        self.load_data()

    def _create_widgets(self):
        """Thiết lập tất cả widgets trên tab2."""
        
        # 1. Tiêu đề và Khung Tìm kiếm
        lbl_title = tk.Label(self.parent_tab, text="CHI TIẾT HƯỚNG DẪN VIÊN", font=("Arial", 18, "bold"), fg="blue")
        lbl_title.pack(pady=10)

        frame_title_search_hdv = tk.Frame(self.parent_tab, padx=10)
        frame_title_search_hdv.pack(fill="x", pady=5)

        tk.Label(frame_title_search_hdv, text="Tìm Mã HDV:", font=("Arial", 10)).pack(side="left", padx=(10, 5))
        self.entry_search_mahdv = tk.Entry(frame_title_search_hdv, width=15)
        self.entry_search_mahdv.pack(side="left")

        tk.Button(frame_title_search_hdv, text="Tìm", command=self.search_by_mahdv, bg="#4da6ff", fg="white", font=("Arial", 9)).pack(side="left", padx=(6, 0))
        tk.Button(frame_title_search_hdv, text="Xem Tất Cả", command=self.load_data, bg="#99CCFF", fg="black", font=("Arial", 9)).pack(side="left", padx=(15, 0))

        # 2. Khung nhập thông tin (Entries)
        frame_info = tk.Frame(self.parent_tab, padx=20, pady=10, relief=tk.GROOVE, borderwidth=1)
        frame_info.pack(pady=5, padx=10, fill="x")
        frame_info.columnconfigure(1, weight=1); frame_info.columnconfigure(3, weight=1) 

        tk.Label(frame_info, text="Mã HDV:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_mahdv = tk.Entry(frame_info, width=30); self.entry_mahdv.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Tên HDV:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_tenhdv = tk.Entry(frame_info, width=30); self.entry_tenhdv.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Số Điện Thoại:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_sdt = tk.Entry(frame_info, width=30); self.entry_sdt.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Email:", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_email = tk.Entry(frame_info, width=30); self.entry_email.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Ngày Sinh:", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.entry_ngaysinh = DateEntry(frame_info, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', year=1990); self.entry_ngaysinh.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Kinh nghiệm (năm):", font=("Arial", 10)).grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.entry_kinhnghiem = tk.Spinbox(frame_info, from_=0, to=50, width=5); self.entry_kinhnghiem.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.entry_kinhnghiem.delete(0, tk.END); self.entry_kinhnghiem.insert(0, 0)
        
        # 3. Khung nút chức năng
        frame_buttons = tk.Frame(self.parent_tab, pady=10); frame_buttons.pack(pady=10)
        tk.Button(frame_buttons, text="Thêm", width=12, bg="#4CAF50", fg="white", command=self.add_hdv).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Sửa", width=12, bg="#FFC107", fg="black", command=self.update_hdv).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Xóa", width=12, bg="#F44336", fg="white", command=self.delete_hdv).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Làm Mới", width=12, command=self.clear_entries).pack(side=tk.LEFT, padx=10)

        # 4. Treeview
        tree_frame = tk.Frame(self.parent_tab, padx=10); tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ('mahdv', 'tenhdv', 'sodienthoai', 'email', 'ngaysinh', 'kinhnghiem')
        self.tree_hdv = ttk.Treeview(tree_frame, columns=columns, show='headings')

        self.tree_hdv.heading('mahdv', text='Mã HDV'); self.tree_hdv.column('mahdv', width=60, anchor='center')
        self.tree_hdv.heading('tenhdv', text='Tên HDV'); self.tree_hdv.column('tenhdv', width=150)
        self.tree_hdv.heading('sodienthoai', text='SĐT'); self.tree_hdv.column('sodienthoai', width=100, anchor='center')
        self.tree_hdv.heading('email', text='Email'); self.tree_hdv.column('email', width=200)
        self.tree_hdv.heading('ngaysinh', text='Ngày Sinh'); self.tree_hdv.column('ngaysinh', width=100, anchor='center')
        self.tree_hdv.heading('kinhnghiem', text='Kinh Nghiệm'); self.tree_hdv.column('kinhnghiem', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_hdv.yview)
        self.tree_hdv.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_hdv.pack(fill="both", expand=True)
        self.tree_hdv.bind('<<TreeviewSelect>>', self.select_record)

    # --- Các hàm Logic (Sử dụng self.ten_bien) ---
    
    def clear_entries(self):
        # ... (Nội dung hàm đã chỉnh sửa sử dụng self.) ...
        self.entry_mahdv.delete(0, tk.END)
        self.entry_tenhdv.delete(0, tk.END)
        self.entry_sdt.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_ngaysinh.set_date(date.today()) 
        self.entry_kinhnghiem.delete(0, tk.END)
        self.entry_kinhnghiem.insert(0, 0)
        self.tree_hdv.selection_remove(self.tree_hdv.selection()) 
        self.entry_search_mahdv.delete(0, tk.END)

    def load_data(self):
        if not check_db_connection(self.root): return
        for item in self.tree_hdv.get_children(): self.tree_hdv.delete(item)
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT mahdv, tenhdv, sodienthoai, email, DATE_FORMAT(ngaysinh, '%d/%m/%Y'), kinhnghiem FROM huongdanvien")
                for record in cursor.fetchall():
                    self.tree_hdv.insert('', tk.END, values=record)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")
            
    def search_by_mahdv(self):
        if not check_db_connection(self.root): return
        timkiem = self.entry_search_mahdv.get().strip()
        if not timkiem: return self.load_data()
        try: mahdv_search = int(timkiem)
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Mã HDV phải là số nguyên."); return self.load_data()

        for item in self.tree_hdv.get_children(): self.tree_hdv.delete(item)
        try:
            with conn.cursor() as cursor:
                sql = "SELECT mahdv, tenhdv, sodienthoai, email, DATE_FORMAT(ngaysinh, '%d/%m/%Y'), kinhnghiem FROM huongdanvien WHERE mahdv = %s"
                cursor.execute(sql, (mahdv_search,))
                records = cursor.fetchall()
                if not records:
                    messagebox.showwarning("Không Tìm Thấy", f"Không tìm thấy HDV có Mã: {mahdv_search}"); self.load_data(); return
                for record in records:
                    self.tree_hdv.insert('', tk.END, values=record)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")
            
    def select_record(self, event):
        self.clear_entries() 
        selected = self.tree_hdv.focus()
        if not selected: return
        values = self.tree_hdv.item(selected, 'values')
        
        if values:
            self.entry_mahdv.insert(0, values[0])
            self.entry_tenhdv.insert(0, values[1])
            self.entry_sdt.insert(0, values[2])
            self.entry_email.insert(0, values[3])
            try:
                date_obj = datetime.strptime(values[4], '%d/%m/%Y').date()
                self.entry_ngaysinh.set_date(date_obj)
            except:
                self.entry_ngaysinh.set_date(date.today()) 
            self.entry_kinhnghiem.delete(0, tk.END)
            self.entry_kinhnghiem.insert(0, values[5])

    def add_hdv(self):
        # Dán logic add_hdv của bạn vào đây, thay entry_X bằng self.entry_X
        messagebox.showinfo("Chức Năng", "Thêm HDV chưa được lập trình chi tiết."); self.load_data()
    
    def update_hdv(self):
        # Dán logic update_hdv của bạn vào đây, thay entry_X bằng self.entry_X
        messagebox.showinfo("Chức Năng", "Sửa HDV chưa được lập trình chi tiết."); self.load_data()

    def delete_hdv(self):
        # Dán logic delete_hdv của bạn vào đây, thay entry_X bằng self.entry_X
        messagebox.showinfo("Chức Năng", "Xóa HDV chưa được lập trình chi tiết."); self.load_data()