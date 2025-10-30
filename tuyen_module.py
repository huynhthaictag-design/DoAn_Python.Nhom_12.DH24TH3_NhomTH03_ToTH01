# tuyen_module.py

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

from database import conn, check_db_connection 

class TuyenManager:
    """Quản lý giao diện, dữ liệu và logic CRUD cho Tab Tuyến Du Lịch."""
    
    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.root = parent_tab.winfo_toplevel()
        
        self._create_widgets()
        self.load_data()

    def _create_widgets(self):
        """Thiết lập tất cả widgets trên tab1."""
        label_bg = "#b3d1ff"
        label_fg = "#1a3c6e"
        entry_bg = "#ffffff"
        entry_fg = "#2d5c88"

        # 1. Tiêu đề và Tìm kiếm
        frame_title = tk.Frame(self.parent_tab, bg="#f2f6fc")
        frame_title.pack(fill="x", pady=12, padx=15)
        lbl_title = tk.Label(frame_title, text="QUẢN LÝ Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#f2f6fc", fg="#2d5c88")
        lbl_title.pack(side="left")

        tk.Label(frame_title, text="Tìm Mã Tuyến:", bg="#f2f6fc", fg="#2d5c88", font=("Arial", 10)).pack(side="left", padx=(20,5))
        self.entry_search_id = tk.Entry(frame_title, width=10, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
        self.entry_search_id.pack(side="left")
        tk.Button(frame_title, text="Tìm", command=self.search_by_matuyen, bg="#4da6ff", fg="white", font=("Arial", 9)).pack(side="left", padx=(6,0))
        tk.Button(frame_title, text="Xem Tất Cả", command=self.load_data, bg="#99CCFF", fg="black", font=("Arial", 9)).pack(side="left", padx=(15, 0))


        # 2. Khung nhập thông tin (Entries)
        frame_info = tk.LabelFrame(self.parent_tab, text="Thông tin tuyến du lịch", font=("Arial", 13, "bold"), bg="#e3ecfa", fg="#2d5c88", bd=2)
        frame_info.pack(pady=10, padx=15, fill="x")

        tk.Label(frame_info, text="Mã Tuyến Du Lịch:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=7, pady=7, sticky="w")
        self.entry_matuyen = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_matuyen.grid(row=0, column=1, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Tên Tuyến:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=7, pady=7, sticky="w")
        self.entry_tentuyen = tk.Entry(frame_info, width=25, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_tentuyen.grid(row=0, column=3, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Điểm Khởi Hành:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=7, pady=7, sticky="w")
        self.entry_diemkhoihanh = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_diemkhoihanh.grid(row=1, column=1, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Địa điểm đến:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=1, column=2, padx=7, pady=7, sticky="w")
        self.entry_diemden = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_diemden.grid(row=1, column=3, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Thời lượng:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=7, pady=7, sticky="w")
        self.entry_thoiluong = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_thoiluong.grid(row=2, column=1, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Giá tour:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=2, column=2, padx=7, pady=7, sticky="w")
        self.entry_giatour = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_giatour.grid(row=2, column=3, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Mô tả:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=3, column=0, padx=7, pady=7, sticky="w")
        self.entry_mota = tk.Entry(frame_info, width=40, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_mota.grid(row=3, column=1, columnspan=3, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Hướng dẫn viên:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=4, column=0, padx=7, pady=7, sticky="w")
        self.entry_huongdanvien = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_huongdanvien.grid(row=4, column=1, padx=7, pady=7, sticky="w")

        # 3. Khung nút chức năng
        frame_buttons_tuyen = tk.Frame(self.parent_tab, pady=10); frame_buttons_tuyen.pack(pady=5)
        tk.Button(frame_buttons_tuyen, text="Thêm Tuyến", width=12, bg="#008CBA", fg="white", command=self.add_tuyen).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons_tuyen, text="Sửa Tuyến", width=12, bg="#FFA500", fg="black", command=self.update_tuyen).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons_tuyen, text="Xóa Tuyến", width=12, bg="#DC143C", fg="white", command=self.delete_tuyen).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons_tuyen, text="Làm Mới", width=12, command=self.clear_entries).pack(side=tk.LEFT, padx=10)

        # 4. Treeview
        tree_frame_tuyen = tk.Frame(self.parent_tab, padx=10); tree_frame_tuyen.pack(pady=10, padx=10, fill="both", expand=True)
        columns_tuyen = ('matuyen', 'tentuyen', 'diemkhoihanh', 'diemden', 'thoiluong', 'giatour', 'mota', 'huongdanvien')
        self.tree_tuyendulich = ttk.Treeview(tree_frame_tuyen, columns=columns_tuyen, show='headings')

        self.tree_tuyendulich.heading('matuyen', text='Mã Tuyến'); self.tree_tuyendulich.column('matuyen', width=60, anchor='center')
        self.tree_tuyendulich.heading('tentuyen', text='Tên Tuyến'); self.tree_tuyendulich.column('tentuyen', width=150)
        self.tree_tuyendulich.heading('diemkhoihanh', text='Khởi Hành'); self.tree_tuyendulich.column('diemkhoihanh', width=100)
        self.tree_tuyendulich.heading('diemden', text='Địa Điểm Đến'); self.tree_tuyendulich.column('diemden', width=100)
        self.tree_tuyendulich.heading('thoiluong', text='Thời Lượng'); self.tree_tuyendulich.column('thoiluong', width=80, anchor='center')
        self.tree_tuyendulich.heading('giatour', text='Giá Tour'); self.tree_tuyendulich.column('giatour', width=80, anchor='center')
        self.tree_tuyendulich.heading('mota', text='Mô Tả'); self.tree_tuyendulich.column('mota', width=200)
        self.tree_tuyendulich.heading('huongdanvien', text='Mã HDV'); self.tree_tuyendulich.column('huongdanvien', width=60, anchor='center')

        scrollbar_tuyen = ttk.Scrollbar(tree_frame_tuyen, orient=tk.VERTICAL, command=self.tree_tuyendulich.yview)
        self.tree_tuyendulich.configure(yscrollcommand=scrollbar_tuyen.set)
        scrollbar_tuyen.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tuyendulich.pack(fill="both", expand=True)
        self.tree_tuyendulich.bind('<<TreeviewSelect>>', self.select_record)

    # --- Các hàm Logic (Sử dụng self.ten_bien) ---

    def clear_entries(self):
        self.entry_matuyen.delete(0, tk.END)
        self.entry_tentuyen.delete(0, tk.END)
        self.entry_diemkhoihanh.delete(0, tk.END)
        self.entry_diemden.delete(0, tk.END)
        self.entry_thoiluong.delete(0, tk.END)
        self.entry_giatour.delete(0, tk.END)
        self.entry_mota.delete(0, tk.END)
        self.entry_huongdanvien.delete(0, tk.END)
        self.tree_tuyendulich.selection_remove(self.tree_tuyendulich.selection())
        self.entry_search_id.delete(0, tk.END)

    def load_data(self):
        if not check_db_connection(self.root): return
        for item in self.tree_tuyendulich.get_children(): self.tree_tuyendulich.delete(item)
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT matuyen, tentuyen, diemkhoihanh, diemden, thoiluong, giatour, mota, mahdv FROM tuyendulich")
                for record in cursor.fetchall():
                    self.tree_tuyendulich.insert('', tk.END, values=record)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")
            
    def search_by_matuyen(self):
        if not check_db_connection(self.root): return
        timkiem = self.entry_search_id.get().strip()
        if not timkiem: return self.load_data()
        
        for i in self.tree_tuyendulich.get_children(): self.tree_tuyendulich.delete(i)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT matuyen, tentuyen, diemkhoihanh, diemden, thoiluong, giatour, mota, mahdv FROM tuyendulich WHERE matuyen=%s", (timkiem,))
                for row in cur.fetchall():
                    self.tree_tuyendulich.insert("", tk.END, values=row)
                if not cur.rowcount:
                     messagebox.showwarning("Không Tìm Thấy", f"Không tìm thấy Tuyến có Mã: {timkiem}"); self.load_data();
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")

    def select_record(self, event):
        self.clear_entries() 
        selected = self.tree_tuyendulich.focus()
        if not selected: return
        values = self.tree_tuyendulich.item(selected, 'values')
        
        if values:
            self.entry_matuyen.insert(0, values[0])
            self.entry_tentuyen.insert(0, values[1])
            self.entry_diemkhoihanh.insert(0, values[2])
            self.entry_diemden.insert(0, values[3])
            self.entry_thoiluong.insert(0, values[4])
            self.entry_giatour.insert(0, values[5])
            self.entry_mota.insert(0, values[6])
            self.entry_huongdanvien.insert(0, values[7])

    def add_tuyen(self):
        messagebox.showinfo("Chức Năng", "Thêm Tuyến chưa được lập trình chi tiết."); self.load_data()
    
    def update_tuyen(self):
        messagebox.showinfo("Chức Năng", "Sửa Tuyến chưa được lập trình chi tiết."); self.load_data()

    def delete_tuyen(self):
        messagebox.showinfo("Chức Năng", "Xóa Tuyến chưa được lập trình chi tiết."); self.load_data()