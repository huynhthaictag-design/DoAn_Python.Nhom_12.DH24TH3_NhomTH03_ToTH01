
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
        
        self.hovered_item = None 
        
        # SỬA: Tạo các "map" để lưu ID và Tên
        self.diadiem_map_name_to_id = {} # Key: Tên, Value: ID
        self.diadiem_map_id_to_name = {} # Key: ID, Value: Tên
        self.hdv_map_name_to_id = {}
        self.hdv_map_id_to_name = {}
        
        self._create_widgets()
        self._load_combobox_data() # Tải dữ liệu cho dropdown
        self.load_data()

    def _load_combobox_data(self):
        """Tải dữ liệu cho các Combobox Địa Điểm và HDV từ CSDL."""
        try:
            with conn.cursor() as cursor:
                # 1. Tải Địa Điểm
                cursor.execute("SELECT MaDiaDiem, TenDiaDiem FROM DiaDiem")
                diadiem_records = cursor.fetchall()
                diadiem_names = []
                for (madd, tendd) in diadiem_records:
                    self.diadiem_map_name_to_id[tendd] = madd
                    self.diadiem_map_id_to_name[madd] = tendd
                    diadiem_names.append(tendd)
                
                # Gán danh sách tên vào Combobox
                self.combo_MaDiemKhoiHanh['values'] = diadiem_names
                self.combo_MaDiemDen['values'] = diadiem_names

                # 2. Tải Hướng Dẫn Viên
                cursor.execute("SELECT mahdv, tenhdv FROM huongdanvien")
                hdv_records = cursor.fetchall()
                hdv_names = []
                for (mahdv, tenhdv) in hdv_records:
                    self.hdv_map_name_to_id[tenhdv] = mahdv
                    self.hdv_map_id_to_name[mahdv] = tenhdv
                    hdv_names.append(tenhdv)
                    
                self.combo_MaHDV['values'] = hdv_names
                
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dropdown", f"Không thể tải dữ liệu Địa Điểm/HDV: {err}")


    def _create_widgets(self):
        """Thiết lập tất cả widgets trên tab1."""
        label_bg = "#b3d1ff"
        label_fg = "#1a3c6e"
        entry_bg = "#ffffff"
        entry_fg = "#2d5c88"

        # 1. Tiêu đề và Tìm kiếm (Giữ nguyên)
        frame_title = tk.Frame(self.parent_tab, bg="#f2f6fc")
        frame_title.pack(fill="x", pady=12, padx=15)
        lbl_title = tk.Label(frame_title, text="QUẢN LÝ Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#f2f6fc", fg="#2d5c88")
        lbl_title.pack(side="left")
        # ... (Code tìm kiếm giữ nguyên)
        tk.Label(frame_title, text="Tìm Mã số:", bg="#f2f6fc", fg="#2d5c88", font=("Arial", 10)).pack(side="left", padx=(20,5))
        self.entry_search_id = tk.Entry(frame_title, width=10, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
        self.entry_search_id.pack(side="left")
        tk.Button(frame_title, text="Tìm", command=self.search_by_maso, bg="#4da6ff", fg="white", font=("Arial", 9)).pack(side="left", padx=(6,0))
        tk.Button(frame_title, text="Xem Tất Cả", command=self.load_data, bg="#99CCFF", fg="black", font=("Arial", 9)).pack(side="left", padx=(15, 0))


        # 2. Khung nhập thông tin (Entries)
        frame_info = tk.LabelFrame(self.parent_tab, text="Thông tin tuyến du lịch", font=("Arial", 13, "bold"), bg="#e3ecfa", fg="#2d5c88", bd=2)
        frame_info.pack(pady=10, padx=15, fill="x")

        # Hàng 0
        tk.Label(frame_info, text="Mã số (Tuyến):", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=7, pady=7, sticky="w")
        self.entry_matuyen = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_matuyen.grid(row=0, column=1, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Tên Tuyến:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=7, pady=7, sticky="w")
        self.entry_tentuyen = tk.Entry(frame_info, width=25, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_tentuyen.grid(row=0, column=3, padx=7, pady=7, sticky="w")
        
        # Hàng 1 (SỬA: Dùng Combobox)
        tk.Label(frame_info, text="Điểm Khởi Hành:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=7, pady=7, sticky="w")
        self.combo_MaDiemKhoiHanh = ttk.Combobox(frame_info, width=13, state="readonly"); 
        self.combo_MaDiemKhoiHanh.grid(row=1, column=1, padx=7, pady=7, sticky="w")
        
        tk.Label(frame_info, text="Điểm Đến:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=1, column=2, padx=7, pady=7, sticky="w")
        self.combo_MaDiemDen = ttk.Combobox(frame_info, width=23, state="readonly"); 
        self.combo_MaDiemDen.grid(row=1, column=3, padx=7, pady=7, sticky="w")
        
        # Hàng 2
        tk.Label(frame_info, text="Thời lượng:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=7, pady=7, sticky="w")
        self.entry_thoiluong = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_thoiluong.grid(row=2, column=1, padx=7, pady=7, sticky="w")
        tk.Label(frame_info, text="Giá tour:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=2, column=2, padx=7, pady=7, sticky="w")
        self.entry_giatour = tk.Entry(frame_info, width=25, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_giatour.grid(row=2, column=3, padx=7, pady=7, sticky="w")
        
        # Hàng 3 (Mô tả)
        tk.Label(frame_info, text="Mô tả:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=3, column=0, padx=7, pady=7, sticky="w")
        self.entry_mota = tk.Entry(frame_info, width=40, bg=entry_bg, fg=entry_fg, font=("Arial", 10)); self.entry_mota.grid(row=3, column=1, columnspan=3, padx=7, pady=7, sticky="w")
        
        # Hàng 4 (SỬA: Dùng Combobox)
        tk.Label(frame_info, text="H. Dẫn Viên:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=4, column=0, padx=7, pady=7, sticky="w")
        self.combo_MaHDV = ttk.Combobox(frame_info, width=13, state="readonly"); 
        self.combo_MaHDV.grid(row=4, column=1, padx=7, pady=7, sticky="w")

        tk.Label(frame_info, text="Loại Tour:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=4, column=2, padx=7, pady=7, sticky="w")
        self.combo_loaitour = ttk.Combobox(frame_info, width=23, state="readonly", values=["Trong Nước", "Nước Ngoài"])
        self.combo_loaitour.grid(row=4, column=3, padx=7, pady=7, sticky="w")
        self.combo_loaitour.set("Trong Nước") 

        # 3. Khung nút chức năng (Giữ nguyên)
        frame_buttons_tuyen = tk.Frame(self.parent_tab, pady=10); frame_buttons_tuyen.pack(pady=5)
        tk.Button(frame_buttons_tuyen, text="Thêm Tuyến", width=12, bg="#008CBA", fg="white", command=self.add_tuyen).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons_tuyen, text="Sửa Tuyến", width=12, bg="#FFA500", fg="black", command=self.update_tuyen).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons_tuyen, text="Xóa Tuyến", width=12, bg="#DC143C", fg="white", command=self.delete_tuyen).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons_tuyen, text="Làm Mới", width=12, command=self.clear_entries).pack(side=tk.LEFT, padx=10)

        # 4. Treeview
        tree_frame_tuyen = tk.Frame(self.parent_tab, padx=10); tree_frame_tuyen.pack(pady=10, padx=10, fill="both", expand=True)
        
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass 
        style.map("Treeview", background=[('selected', '#007bff')], foreground=[('selected', 'white')])

        # SỬA: Hiển thị TÊN thay vì MÃ
        columns_tuyen = ('maso', 'tentuyen', 'TenDiemKhoiHanh', 'TenDiemDen', 'thoiluong', 'giatour', 'TenHDV', 'loaitour')
        self.tree_tuyendulich = ttk.Treeview(tree_frame_tuyen, columns=columns_tuyen, show='headings')

        self.tree_tuyendulich.tag_configure('normal', background='white', foreground='black')
        self.tree_tuyendulich.tag_configure('hover', background='#e6f2ff', foreground='black')

        self.tree_tuyendulich.heading('maso', text='Mã số'); self.tree_tuyendulich.column('maso', width=50, anchor='center')
        self.tree_tuyendulich.heading('tentuyen', text='Tên Tuyến'); self.tree_tuyendulich.column('tentuyen', width=150)
        self.tree_tuyendulich.heading('TenDiemKhoiHanh', text='Khởi Hành'); self.tree_tuyendulich.column('TenDiemKhoiHanh', width=120)
        self.tree_tuyendulich.heading('TenDiemDen', text='Điểm Đến'); self.tree_tuyendulich.column('TenDiemDen', width=120)
        self.tree_tuyendulich.heading('thoiluong', text='Thời Lượng'); self.tree_tuyendulich.column('thoiluong', width=70, anchor='center')
        self.tree_tuyendulich.heading('giatour', text='Giá Tour'); self.tree_tuyendulich.column('giatour', width=80, anchor='center')
        self.tree_tuyendulich.heading('TenHDV', text='Tên HDV'); self.tree_tuyendulich.column('TenHDV', width=120)
        self.tree_tuyendulich.heading('loaitour', text='Loại Tour'); self.tree_tuyendulich.column('loaitour', width=80, anchor='center') 

        scrollbar_tuyen = ttk.Scrollbar(tree_frame_tuyen, orient=tk.VERTICAL, command=self.tree_tuyendulich.yview)
        self.tree_tuyendulich.configure(yscrollcommand=scrollbar_tuyen.set)
        scrollbar_tuyen.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tuyendulich.pack(fill="both", expand=True)
        
        self.tree_tuyendulich.bind('<<TreeviewSelect>>', self.select_record)
        self.tree_tuyendulich.bind('<Motion>', self._on_tree_hover)
        self.tree_tuyendulich.bind('<Leave>', self._on_tree_leave)

    # --- Logic Hover (Giữ nguyên) ---
    def _on_tree_hover(self, event):
        item = self.tree_tuyendulich.identify_row(event.y)
        selected_item = self.tree_tuyendulich.selection()[0] if self.tree_tuyendulich.selection() else None
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_tuyendulich.item(self.hovered_item, tags=('normal',))
        if item and item != selected_item:
            self.tree_tuyendulich.item(item, tags=('hover',))
            self.hovered_item = item
        else: self.hovered_item = None
    def _on_tree_leave(self, event):
        selected_item = self.tree_tuyendulich.selection()[0] if self.tree_tuyendulich.selection() else None
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_tuyendulich.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None
    
    # --- Các hàm Logic CRUD (Đã SỬA) ---

    def clear_entries(self):
        self.entry_matuyen.delete(0, tk.END)
        self.entry_tentuyen.delete(0, tk.END)
        self.combo_MaDiemKhoiHanh.set('') # Sửa
        self.combo_MaDiemDen.set('') # Sửa
        self.entry_thoiluong.delete(0, tk.END)
        self.entry_giatour.delete(0, tk.END)
        self.entry_mota.delete(0, tk.END)
        self.combo_MaHDV.set('') # Sửa
        self.combo_loaitour.set("Trong Nước") 
        self.tree_tuyendulich.selection_remove(self.tree_tuyendulich.selection())
        self.entry_search_id.delete(0, tk.END)
        self._on_tree_leave(None)

    def load_data(self):
        """SỬA: Load dữ liệu dùng JOIN để lấy TÊN."""
        if not check_db_connection(self.root): return
        self._load_combobox_data() # Cập nhật lại dropdown
        for item in self.tree_tuyendulich.get_children(): self.tree_tuyendulich.delete(item)
        
        try:
            with conn.cursor() as cursor:
                # SỬA SQL: Dùng JOIN để lấy Tên thay vì Mã
                sql = """
                SELECT 
                    T.maso, T.tentuyen, 
                    DD_KH.TenDiaDiem AS TenKhoiHanh, 
                    DD_Den.TenDiaDiem AS TenDen,
                    T.thoiluong, T.giatour, 
                    H.tenhdv AS TenHDV,
                    T.loaitour
                FROM tuyendulich AS T
                LEFT JOIN DiaDiem AS DD_KH ON T.MaDiemKhoiHanh = DD_KH.MaDiaDiem
                LEFT JOIN DiaDiem AS DD_Den ON T.MaDiemDen = DD_Den.MaDiaDiem
                LEFT JOIN huongdanvien AS H ON T.MaHDV = H.mahdv
                """
                cursor.execute(sql)
                for record in cursor.fetchall():
                    self.tree_tuyendulich.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}.")
            
    def search_by_maso(self):
        # (Sửa hàm này để JOIN luôn)
        if not check_db_connection(self.root): return
        timkiem = self.entry_search_id.get().strip()
        if not timkiem: return self.load_data()
        
        for i in self.tree_tuyendulich.get_children(): self.tree_tuyendulich.delete(i)
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT 
                    T.maso, T.tentuyen, 
                    DD_KH.TenDiaDiem, DD_Den.TenDiaDiem,
                    T.thoiluong, T.giatour, H.tenhdv, T.loaitour
                FROM tuyendulich AS T
                LEFT JOIN DiaDiem AS DD_KH ON T.MaDiemKhoiHanh = DD_KH.MaDiaDiem
                LEFT JOIN DiaDiem AS DD_Den ON T.MaDiemDen = DD_Den.MaDiaDiem
                LEFT JOIN huongdanvien AS H ON T.MaHDV = H.mahdv
                WHERE T.maso=%s
                """
                cur.execute(sql, (timkiem,))
                rows = cur.fetchall()
                if not rows:
                    messagebox.showwarning("Không Tìm Thấy", f"Không tìm thấy Tuyến có Mã số: {timkiem}"); self.load_data(); return
                for row in rows:
                    self.tree_tuyendulich.insert("", tk.END, values=row, tags=('normal',))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")

    def select_record(self, event):
        """SỬA: Hiển thị TÊN trên Combobox."""
        selected_item = self.tree_tuyendulich.focus()
        if self.hovered_item and self.hovered_item != selected_item:
             self.tree_tuyendulich.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None
        
        # Xóa thủ công
        self.entry_matuyen.delete(0, tk.END)
        self.entry_tentuyen.delete(0, tk.END)
        self.entry_thoiluong.delete(0, tk.END)
        self.entry_giatour.delete(0, tk.END)
        self.entry_mota.delete(0, tk.END) # (Lưu ý: Mô tả không có trong treeview, không thể chọn)
        
        if not selected_item: 
            self.combo_MaDiemKhoiHanh.set('')
            self.combo_MaDiemDen.set('')
            self.combo_MaHDV.set('')
            self.combo_loaitour.set("Trong Nước")
            return
        
        values = self.tree_tuyendulich.item(selected_item, 'values')
        
        if values:
            self.entry_matuyen.insert(0, values[0]) 
            self.entry_tentuyen.insert(0, values[1])
            self.combo_MaDiemKhoiHanh.set(values[2]) # Sửa
            self.combo_MaDiemDen.set(values[3]) # Sửa
            self.entry_thoiluong.insert(0, values[4])
            self.entry_giatour.insert(0, values[5])
            self.combo_MaHDV.set(values[6]) # Sửa
            self.combo_loaitour.set(values[7]) 
            # (Thiếu entry_mota, vì SQL SELECT không lấy mota)

    def _validate_input(self):
        """SỬA: Lấy ID từ TÊN của Combobox."""
        maso = self.entry_matuyen.get().strip()
        tentuyen = self.entry_tentuyen.get().strip()
        giatour = self.entry_giatour.get().strip()
        loaitour = self.combo_loaitour.get().strip() 
        
        # SỬA: Lấy Tên từ Combobox
        ten_khoihanh = self.combo_MaDiemKhoiHanh.get().strip()
        ten_diemden = self.combo_MaDiemDen.get().strip()
        ten_hdv = self.combo_MaHDV.get().strip()

        if not all([maso, tentuyen, giatour, loaitour, ten_khoihanh, ten_diemden]):
            messagebox.showerror("Lỗi Nhập Liệu", "Các trường (trừ HDV, Mô tả) không được để trống.")
            return None
        
        try:
            maso_int = int(maso)
            giatour_float = float(giatour)
            
            # SỬA: Lấy ID từ Tên
            ma_khoihanh_int = self.diadiem_map_name_to_id.get(ten_khoihanh)
            ma_diemden_int = self.diadiem_map_name_to_id.get(ten_diemden)
            
            # HDV có thể trống
            ma_hdv_int = self.hdv_map_name_to_id.get(ten_hdv) if ten_hdv else None

            if ma_khoihanh_int is None or ma_diemden_int is None:
                messagebox.showerror("Lỗi Dữ Liệu", "Địa điểm khởi hành hoặc điểm đến không hợp lệ.")
                return None

        except ValueError as e:
            messagebox.showerror("Lỗi Dữ Liệu", f"Mã số hoặc Giá tour phải là số.")
            return None
            
        return (maso_int, tentuyen, ma_khoihanh_int, ma_diemden_int,
                self.entry_thoiluong.get().strip(), giatour_float, 
                self.entry_mota.get().strip(), ma_hdv_int, loaitour)

    def add_tuyen(self):
        if not check_db_connection(self.root): return
        data = self._validate_input()
        if not data: return

        # SQL này đúng (dùng Mã ID)
        sql = "INSERT INTO tuyendulich (maso, tentuyen, MaDiemKhoiHanh, MaDiemDen, thoiluong, giatour, mota, MaHDV, loaitour) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()
                messagebox.showinfo("Thành Công", "Thêm Tuyến Du Lịch thành công.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.Error as err:
            if err.errno == 1452:
                messagebox.showerror("Lỗi SQL (Thêm Tuyến)", f"Lỗi Khóa Ngoại: Mã Địa Điểm hoặc Mã HDV không tồn tại.")
            elif err.errno == 1062:
                messagebox.showerror("Lỗi SQL (Thêm Tuyến)", f"Lỗi: Mã Tuyến {data[0]} đã tồn tại.")
            else:
                messagebox.showerror("Lỗi SQL (Thêm Tuyến)", f"Lỗi: {err}")
    
    def update_tuyen(self):
        if not check_db_connection(self.root): return
        data_tuple = self._validate_input()
        if not data_tuple: return
        
        maso = data_tuple[0]
        data = data_tuple[1:] + (maso,) 
        
        # SQL này đúng (dùng Mã ID)
        sql = "UPDATE tuyendulich SET tentuyen=%s, MaDiemKhoiHanh=%s, MaDiemDen=%s, thoiluong=%s, giatour=%s, mota=%s, MaHDV=%s, loaitour=%s WHERE maso=%s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Cập nhật Tuyến Du Lịch thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", "Không có dữ liệu nào được cập nhật.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.Error as err:
            if err.errno == 1452:
                messagebox.showerror("Lỗi SQL (Sửa Tuyến)", f"Lỗi Khóa Ngoại: Mã Địa Điểm hoặc Mã HDV không tồn tại.")
            else:
                messagebox.showerror("Lỗi SQL (Sửa Tuyến)", f"Lỗi: {err}")

    def delete_tuyen(self):
        # (Giữ nguyên)
        if not check_db_connection(self.root): return
        maso = self.entry_matuyen.get().strip()
        if not maso:
            messagebox.showerror("Lỗi", "Vui lòng chọn Tuyến cần xóa.")
            return
        if not messagebox.askyesno("Xác Nhận Xóa", f"Bạn có chắc chắn muốn xóa Tuyến có Mã số {maso}?"): return
        
        sql = "DELETE FROM tuyendulich WHERE maso = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (maso,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Xóa Tuyến Du Lịch thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", "Không tìm thấy Tuyến để xóa.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Xóa Tuyến)", f"Lỗi: {err}")