import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

from database import conn, check_db_connection 

# --- Định nghĩa màu sắc theo bảng của bạn ---
COLOR_BACKGROUND_MAIN = "#3da9fc" # Main Background / Button / Highlight
COLOR_HEADLINE = "#094067" # Headline / Stroke
COLOR_PARAGRAPH = "#5f6c7b" # Paragraph
COLOR_BUTTON_TEXT = "#fffffe" # Button text / Main
COLOR_SECONDARY = "#90b4ce" # Secondary
COLOR_TERTIARY = "#ef4565" # Tertiary (cho lỗi/cảnh báo)

class UserApp:
    """Giao diện chính cho Người dùng (User)"""
    def __init__(self, root):
        self.root = root
        self.root.title("Chào mừng Khách hàng")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        self.hovered_item = None
        
        self._create_layout()
        self._create_left_menu()
        self._create_content_area()
        
        self.load_tour_data()

    def _create_layout(self):
        """Tạo 2 khung chính: Menu (trái) và Nội dung (phải)"""
        # 1. Khung Menu bên trái
        self.menu_frame = tk.Frame(self.root, bg=COLOR_HEADLINE, width=200) # Nền xanh đậm
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)

        # 2. Khung Nội dung bên phải
        self.content_frame = tk.Frame(self.root, bg=COLOR_BUTTON_TEXT) # Nền trắng
        self.content_frame.pack(side="right", fill="both", expand=True)

    def _create_left_menu(self):
        """Tạo các nút bấm hoạt động như Menu bên trái"""
        
        tk.Label(self.menu_frame, text="MENU", font=("Poppins", 16, "bold"),
                 bg=COLOR_HEADLINE, fg=COLOR_BUTTON_TEXT).pack(pady=20) # Chữ trắng trên nền xanh đậm

        menu_items = [
            ("Xem Tours", self.show_tour_view),
            ("Đặt Vé", self.open_booking_window),
            ("Thoát", self.root.quit)
        ]

        for (text, command) in menu_items:
            btn = tk.Button(self.menu_frame, text=text, font=("Poppins", 11),
                            bg=COLOR_BACKGROUND_MAIN, fg=COLOR_BUTTON_TEXT, # Nút xanh sáng, chữ trắng
                            relief="flat", anchor="w",
                            padx=20, cursor="hand2")
            btn.config(command=command)
            btn.pack(fill="x", pady=5, padx=10)
            
            # Thay đổi màu khi hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_SECONDARY, fg=COLOR_HEADLINE)) # Hover: xanh xám nhạt, chữ xanh đậm
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BACKGROUND_MAIN, fg=COLOR_BUTTON_TEXT))


    def _create_content_area(self):
        """Tạo khu vực hiển thị Treeview (List view)"""
        
        lbl_title = tk.Label(self.content_frame, text="DANH SÁCH CÁC TOUR HIỆN CÓ", 
                             font=("Arial", 18, "bold"), fg=COLOR_HEADLINE, bg=COLOR_BUTTON_TEXT) # Tiêu đề xanh đậm trên nền trắng
        lbl_title.pack(pady=15)
        
        tree_frame = tk.Frame(self.content_frame, padx=10, bg=COLOR_BUTTON_TEXT) # Nền trắng
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass 
        
        # Style cho Treeview
        style.configure("Treeview.Heading", 
                        font=("Arial", 10, "bold"), 
                        background=COLOR_SECONDARY, # Nền heading xanh xám nhạt
                        foreground=COLOR_HEADLINE) # Chữ heading xanh đậm
        style.configure("Treeview", 
                        background=COLOR_BUTTON_TEXT, # Nền trắng cho dòng thường
                        foreground=COLOR_PARAGRAPH, # Chữ xám xanh cho dòng thường
                        rowheight=25)
        style.map("Treeview", 
                  background=[('selected', COLOR_BACKGROUND_MAIN)], # Dòng chọn: nền xanh sáng
                  foreground=[('selected', COLOR_BUTTON_TEXT)]) # Dòng chọn: chữ trắng

        columns = ('maso', 'tentuyen', 'khoihanh', 'diemden', 'thoiluong', 'giatour_display', 'giatour_raw', 'hdv', 'loai', 'mota')
        self.tree_tours = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Thẻ tag cho hover (nền nhẹ hơn một chút)
        self.tree_tours.tag_configure('normal', background=COLOR_BUTTON_TEXT, foreground=COLOR_PARAGRAPH)
        self.tree_tours.tag_configure('hover', background='#e0f2f7', foreground=COLOR_HEADLINE) # Xanh nhạt khi hover

        self.tree_tours.config(displaycolumns=('tentuyen', 'khoihanh', 'diemden', 'thoiluong', 'giatour_display', 'hdv', 'loai', 'mota'))

        self.tree_tours.heading('tentuyen', text='Tên Tuyến'); self.tree_tours.column('tentuyen', width=180)
        self.tree_tours.heading('khoihanh', text='Khởi Hành'); self.tree_tours.column('khoihanh', width=120)
        self.tree_tours.heading('diemden', text='Điểm Đến'); self.tree_tours.column('diemden', width=120)
        self.tree_tours.heading('thoiluong', text='Thời Lượng'); self.tree_tours.column('thoiluong', width=80, anchor='center')
        self.tree_tours.heading('giatour_display', text='Giá Tour'); self.tree_tours.column('giatour_display', width=100, anchor='e')
        self.tree_tours.heading('hdv', text='HDV'); self.tree_tours.column('hdv', width=120)
        self.tree_tours.heading('loai', text='Loại'); self.tree_tours.column('loai', width=80, anchor='center')
        self.tree_tours.heading('mota', text='Mô Tả'); self.tree_tours.column('mota', width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_tours.yview)
        self.tree_tours.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tours.pack(fill="both", expand=True)
        
        self.tree_tours.bind('<Motion>', self._on_tree_hover)
        self.tree_tours.bind('<Leave>', self._on_tree_leave)
        self.tree_tours.bind('<Double-1>', self.open_booking_window)


    def load_tour_data(self):
        if not check_db_connection(self.root): return
        for item in self.tree_tours.get_children(): self.tree_tours.delete(item)

        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT 
                    T.maso,
                    T.tentuyen, 
                    DD_KhoiHanh.TenDiaDiem AS DiemKhoiHanh,
                    DD_Den.TenDiaDiem AS DiemDen,
                    T.thoiluong, 
                    CONCAT(FORMAT(T.giatour, 0), ' VNĐ') AS GiaTourDisplay,
                    T.giatour, 
                    H.tenhdv AS TenHDV,
                    T.loaitour,
                    T.mota
                FROM tuyendulich AS T
                LEFT JOIN DiaDiem AS DD_KhoiHanh ON T.MaDiemKhoiHanh = DD_KhoiHanh.MaDiaDiem
                LEFT JOIN DiaDiem AS DD_Den ON T.MaDiemDen = DD_Den.MaDiaDiem
                LEFT JOIN huongdanvien AS H ON T.MaHDV = H.mahdv
                ORDER BY T.tentuyen
                """
                cursor.execute(sql)
                for record in cursor.fetchall():
                    self.tree_tours.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu Tours", f"Lỗi: {err}")

    # --- THÊM: Chức năng Đặt Vé ---
    
    def open_booking_window(self, event=None):
        selected_item = self.tree_tours.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn Tour", "Vui lòng chọn một tour từ danh sách để đặt vé.")
            return

        values = self.tree_tours.item(selected_item, 'values')
        
        try:
            ma_tuyen = int(values[0])
            ten_tuyen = values[1]
            gia_tour_raw = float(values[6])
        except (IndexError, ValueError):
            messagebox.showerror("Lỗi Dữ Liệu", "Không thể lấy thông tin tour. Dữ liệu bị lỗi.")
            return

        self.book_window = tk.Toplevel(self.root)
        self.book_window.title("Xác Nhận Đặt Vé")
        self.book_window.geometry("400x350")
        self.book_window.transient(self.root) 
        self.book_window.grab_set() 

        form_frame = tk.Frame(self.book_window, padx=20, pady=20, bg=COLOR_BUTTON_TEXT) # Nền trắng
        form_frame.pack(fill="both", expand=True)

        tk.Label(form_frame, text="ĐẶT VÉ TOUR", font=("Arial", 16, "bold"), fg=COLOR_HEADLINE, bg=COLOR_BUTTON_TEXT).pack(pady=10) # Tiêu đề xanh đậm, nền trắng

        tk.Label(form_frame, text=f"Tour: {ten_tuyen}", font=("Arial", 11, "bold"), fg=COLOR_PARAGRAPH, bg=COLOR_BUTTON_TEXT).pack(anchor="w", pady=5) # Chữ xám xanh, nền trắng
        tk.Label(form_frame, text=f"Giá vé: {gia_tour_raw:,.0f} VNĐ/vé", font=("Arial", 10), fg=COLOR_PARAGRAPH, bg=COLOR_BUTTON_TEXT).pack(anchor="w") # Chữ xám xanh, nền trắng

        tk.Label(form_frame, text="Số lượng vé:", font=("Arial", 10), fg=COLOR_PARAGRAPH, bg=COLOR_BUTTON_TEXT).pack(anchor="w", pady=(10,0)) # Chữ xám xanh, nền trắng
        entry_soluong = tk.Spinbox(form_frame, from_=1, to=50, width=10, font=("Arial", 10),
                                  bg=COLOR_BUTTON_TEXT, fg=COLOR_HEADLINE, highlightbackground=COLOR_SECONDARY) # Nền trắng, chữ xanh đậm
        entry_soluong.pack(anchor="w", fill="x", pady=5)
        
        # Nút Xác nhận
        submit_btn = ttk.Button(form_frame, text="Xác nhận Đặt Vé", 
                                style="TButton", # Sử dụng style đã định nghĩa
                                command=lambda: self.submit_booking(
                                    ma_tuyen, 
                                    gia_tour_raw,
                                    entry_soluong.get()
                                ))
        submit_btn.pack(pady=20)


    def submit_booking(self, ma_tuyen, gia_tour_mot_ve, so_luong_str):
        try:
            so_luong = int(so_luong_str)
            if so_luong <= 0:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương.", parent=self.book_window)
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ.", parent=self.book_window)
            return

        tong_tien = gia_tour_mot_ve * so_luong
        ngay_dat = date.today().strftime('%Y-%m-%d')

        if not check_db_connection(self.root): return

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(MaVe) FROM DatVe")
                max_mave = cursor.fetchone()[0]
                new_mave = (max_mave if max_mave is not None else 0) + 1
                
                sql = "INSERT INTO DatVe (MaVe, MaTuyen, NgayDatVe, SoLuongVe, TongTien) VALUES (%s, %s, %s, %s, %s)"
                values = (new_mave, ma_tuyen, ngay_dat, so_luong, tong_tien)
                
                cursor.execute(sql, values)
                conn.commit()
                
                messagebox.showinfo("Thành Công", 
                                    f"Đặt vé thành công!\nMã vé của bạn là: {new_mave}\nTổng tiền: {tong_tien:,.0f} VNĐ",
                                    parent=self.book_window)
                
                self.book_window.destroy() 
                
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể đặt vé: {err}", parent=self.book_window)

    def show_tour_view(self):
        pass 

    def _on_tree_hover(self, event):
        item = self.tree_tours.identify_row(event.y)
        selected_item = self.tree_tours.selection()[0] if self.tree_tours.selection() else None
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_tours.item(self.hovered_item, tags=('normal',))
        if item and item != selected_item:
            self.tree_tours.item(item, tags=('hover',))
            self.hovered_item = item
        else: self.hovered_item = None
    
    def _on_tree_leave(self, event):
        selected_item = self.tree_tours.selection()[0] if self.tree_tours.selection() else None
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_tours.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None

def open_user_app(previous_window):
    if previous_window:
        previous_window.destroy()
    root = tk.Tk()
    if not check_db_connection(root):
        return 
    app = UserApp(root)
    root.mainloop()
    if conn and conn.is_connected():
        conn.close()

if __name__ == "__main__":
    open_user_app(None)