import tkinter as tk
from tkinter import ttk, messagebox, Menu
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime, date
import sys

# --- Database Connection ---
def connect_db():
    """Thiết lập và kiểm tra kết nối CSDL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user='root',
            password='1234', 
            database="qltuyendulich"
        )
        if conn.is_connected():
            return conn
        return None
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Kết Nối", f"Không thể kết nối đến CSDL: {err}")
        return None

# Attempt connection once
conn = connect_db()
if conn is None or not conn.is_connected():
    print("Kết nối thất bại! Vui lòng kiểm tra MySQL.")

# --- Utility Functions ---
def center_window(win, w=850, h=700):
    """Căn giữa cửa sổ ứng dụng."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

def check_db_connection():
    """Kiểm tra và thông báo nếu kết nối CSDL không khả dụng."""
    if not conn or not conn.is_connected():
        messagebox.showerror("Lỗi CSDL", "Kết nối CSDL không khả dụng. Vui lòng kiểm tra MySQL.")
        return False
    return True

# --- CRUD Functions (Đã cập nhật để cho phép nhập mahdv) ---

def clear_entries():
    """Làm sạch tất cả các trường nhập liệu trên tab HDV."""
    
    # 1. Mã HDV: Đã xóa state='readonly' nên chỉ cần xóa nội dung
    entry_mahdv.delete(0, tk.END)
    
    entry_tenhdv.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    
    # Reset date to today's date
    entry_ngaysinh.set_date(date.today()) 
    
    # Reset Spinbox
    entry_kinhnghiem.delete(0, tk.END)
    entry_kinhnghiem.insert(0, 0)
    
    tree_hdv.selection_remove(tree_hdv.selection()) # Deselect any row

def load_data():
    """Tải dữ liệu hướng dẫn viên từ CSDL và hiển thị lên Treeview HDV."""
    if not check_db_connection():
        return

    # Clear old data
    for item in tree_hdv.get_children():
        tree_hdv.delete(item)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT mahdv, tenhdv, sodienthoai, email, DATE_FORMAT(ngaysinh, '%d/%m/%Y'), kinhnghiem FROM huongdanvien")
            records = cursor.fetchall()
            
            for record in records:
                tree_hdv.insert('', tk.END, values=record)
                
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")

def add_hdv():
    """Thêm một hướng dẫn viên mới vào CSDL (với Mã HDV nhập thủ công)."""
    if not check_db_connection():
        return
        
    try:
        # Lấy và kiểm tra Mã HDV (bắt buộc phải là số nguyên)
        mahdv = int(entry_mahdv.get())
    except ValueError:
        messagebox.showerror("Lỗi Dữ Liệu", "Mã HDV phải là số nguyên và không được để trống.")
        return
        
    tenhdv = entry_tenhdv.get()
    sdt = entry_sdt.get()
    email = entry_email.get()
    ngaysinh_str = entry_ngaysinh.get_date().strftime('%Y-%m-%d')
    try:
        kinhnghiem = int(entry_kinhnghiem.get())
    except ValueError:
        messagebox.showerror("Lỗi Dữ Liệu", "Kinh nghiệm phải là số nguyên.")
        return

    if not all([tenhdv, email]):
        messagebox.showerror("Lỗi Nhập Liệu", "Tên và Email không được để trống.")
        return

    # Thêm mahdv vào câu lệnh INSERT và values
    sql = "INSERT INTO huongdanvien (mahdv, tenhdv, sodienthoai, email, ngaysinh, kinhnghiem) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (mahdv, tenhdv, sdt, email, ngaysinh_str, kinhnghiem) 
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Thành Công", "Thêm hướng dẫn viên thành công.")
            clear_entries()
            load_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi SQL", f"Lỗi khi thêm dữ liệu: {err}")

def update_hdv():
    """Cập nhật thông tin hướng dẫn viên đã chọn."""
    if not check_db_connection():
        return
        
    try:
        # Lấy Mã HDV từ Entry (đã được điền khi chọn)
        mahdv = int(entry_mahdv.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng chọn Hướng dẫn viên cần sửa.")
        return
        
    tenhdv = entry_tenhdv.get()
    sdt = entry_sdt.get()
    email = entry_email.get()
    ngaysinh_str = entry_ngaysinh.get_date().strftime('%Y-%m-%d')
    try:
        kinhnghiem = int(entry_kinhnghiem.get())
    except ValueError:
        messagebox.showerror("Lỗi Dữ Liệu", "Kinh nghiệm phải là số nguyên.")
        return

    if not all([tenhdv, email]):
        messagebox.showerror("Lỗi Nhập Liệu", "Tên và Email không được để trống.")
        return

    sql = "UPDATE huongdanvien SET tenhdv=%s, sodienthoai=%s, email=%s, ngaysinh=%s, kinhnghiem=%s WHERE mahdv=%s"
    values = (tenhdv, sdt, email, ngaysinh_str, kinhnghiem, mahdv)
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Thành Công", "Cập nhật hướng dẫn viên thành công.")
            else:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu nào được cập nhật.")
            clear_entries()
            load_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi SQL", f"Lỗi khi sửa dữ liệu: {err}")

def delete_hdv():
    """Xóa hướng dẫn viên đã chọn."""
    if not check_db_connection():
        return
        
    try:
        mahdv = int(entry_mahdv.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng chọn Hướng dẫn viên cần xóa.")
        return

    if not messagebox.askyesno("Xác Nhận Xóa", f"Bạn có chắc chắn muốn xóa HDV có Mã {mahdv}?"):
        return

    sql = "DELETE FROM huongdanvien WHERE mahdv = %s"
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (mahdv,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Thành Công", "Xóa hướng dẫn viên thành công.")
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy HDV để xóa.")
            clear_entries()
            load_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi SQL", f"Lỗi khi xóa dữ liệu: {err}")

def select_record(event):
    """Hiển thị dữ liệu của dòng được chọn lên các ô nhập liệu."""
    clear_entries() 
    selected = tree_hdv.focus()
    if not selected:
        return

    values = tree_hdv.item(selected, 'values')
    
    # 1. Mã HDV (Bây giờ đã cho phép nhập/ghi đè)
    entry_mahdv.insert(0, values[0])
    
    # 2. Tên HDV
    entry_tenhdv.insert(0, values[1])
    
    # 3. SĐT
    entry_sdt.insert(0, values[2])
    
    # 4. Email
    entry_email.insert(0, values[3])
    
    # 5. Ngày Sinh (dd/mm/yyyy)
    try:
        date_obj = datetime.strptime(values[4], '%d/%m/%Y').date()
        entry_ngaysinh.set_date(date_obj)
    except:
        entry_ngaysinh.set_date(date.today()) 

    # 6. Kinh Nghiệm
    entry_kinhnghiem.delete(0, tk.END)
    entry_kinhnghiem.insert(0, values[5])

# --- Main Application Setup ---
root = tk.Tk()
root.title("Quản Lý Tuyến Du Lịch & Hướng Dẫn Viên")
center_window(root)
root.resizable(False, False)

# --- Menu Bar ---
menu = Menu(root)
file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label='New File')
file_menu.add_separator()
file_menu.add_command(label='Open File')
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)
menu.add_cascade(label='File', menu=file_menu)

help_menu = Menu(menu, tearoff=0)
help_menu.add_command(label='About')
menu.add_cascade(label='Help', menu=help_menu)
root.config(menu=menu)

# --- Notebook (Tab Control) ---
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Quản Lý Tuyến Du Lịch')
tab_control.add(tab2, text='Chi tiết huóng dẫn viên')
tab_control.pack(expand=1, fill='both')# =================================================================
#                         TAB 1: QUẢN LÝ TUYẾN DU LỊCH 
# =================================================================

# --- Loại bỏ tiêu đề placeholder:
# tk.Label(tab1, text="CHỨC NĂNG QUẢN LÝ TUYẾN DU LỊCH", font=("Arial", 16, "bold"), fg="gray").pack(pady=50)

# 1. Chuyển frame_title từ root sang tab1
frame_title = tk.Frame(tab1, bg="#f2f6fc")
frame_title.pack(fill="x", pady=12, padx=15)

lbl_title = tk.Label(frame_title, text="QUẢN LÝ Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#f2f6fc", fg="#2d5c88")
lbl_title.pack(side="left")

tk.Label(frame_title, text="Tìm Mã Tuyến:", bg="#f2f6fc", fg="#2d5c88", font=("Arial", 10)).pack(side="left", padx=(20,5))
entry_search_id = tk.Entry(frame_title, width=10, bg="#ffffff", fg="#2d5c88", font=("Arial", 10))
entry_search_id.pack(side="left")

# --- Hàm tìm kiếm (Giữ nguyên, nhưng cần định nghĩa Treeview trước) ---
# Thêm một Treeview cho Tab 1 để hàm tìm kiếm hoạt động
columns_tuyen = ('matuyen', 'tentuyen', 'diemkhoihanh', 'diemden', 'thoiluong', 'giatour', 'mota', 'huongdanvien')
tree_tuyendulich = ttk.Treeview(tab1, columns=columns_tuyen, show='headings') # Đặt trong tab1
tree = tree_tuyendulich # Sử dụng biến 'tree' mà hàm search_by_matuyen đang gọi

def load_data_tuyen():
    """Hàm placeholder để tải dữ liệu tuyến du lịch."""
    # Logic để tải dữ liệu từ CSDL vào tree_tuyendulich
    pass

def search_by_matuyen():
    timkiem = entry_search_id.get().strip()
    if not timkiem:
        load_data_tuyen() # Gọi hàm load data cho tuyến
        return
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT matuyen, tentuyen, diemkhoihanh, diemden, thoiluong, giatour, mota, mahdv FROM tuyendulich WHERE matuyen=%s", (timkiem,))
        for i in tree_tuyendulich.get_children(): # Dùng tree_tuyendulich
            tree_tuyendulich.delete(i)
        for row in cur.fetchall():
            tree_tuyendulich.insert("", tk.END, values=row)
    except Exception as e:
        # Nếu bảng tuyendulich không tồn tại, sẽ báo lỗi
        messagebox.showerror("Lỗi", f"Lỗi tìm kiếm (Có thể thiếu bảng tuyendulich): {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

btn_search_id = tk.Button(frame_title, text="Tìm", command=search_by_matuyen, bg="#4da6ff", fg="white", font=("Arial", 9))
btn_search_id.pack(side="left", padx=(6,0))

# 2. Chuyển frame_info từ root sang tab1
frame_info = tk.LabelFrame(tab1, text="Thông tin tuyến du lịch", font=("Arial", 13, "bold"), bg="#e3ecfa", fg="#2d5c88", bd=2)
frame_info.pack(pady=10, padx=15, fill="x")

# --- Các Labels và Entries (Giữ nguyên parent là frame_info) ---
label_bg = "#b3d1ff"
label_fg = "#1a3c6e"
entry_bg = "#ffffff"
entry_fg = "#2d5c88"

tk.Label(frame_info, text="Mã Tuyến Du Lịch:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=7, pady=7, sticky="w")
entry_matuyen = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_matuyen.grid(row=0, column=1, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Tên Tuyến:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=7, pady=7, sticky="w")
entry_tentuyen = tk.Entry(frame_info, width=25, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_tentuyen.grid(row=0, column=3, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Điểm Khởi Hành:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=7, pady=7, sticky="w")
entry_diemkhoihanh = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_diemkhoihanh.grid(row=1, column=1, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Địa điểm đến:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=1, column=2, padx=7, pady=7, sticky="w")
entry_diemden = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_diemden.grid(row=1, column=3, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Thời lượng:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=7, pady=7, sticky="w")
entry_thoiluong = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_thoiluong.grid(row=2, column=1, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Giá tour:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=2, column=2, padx=7, pady=7, sticky="w")
entry_giatour = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_giatour.grid(row=2, column=3, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Mô tả:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=3, column=0, padx=7, pady=7, sticky="w")
entry_mota = tk.Entry(frame_info, width=40, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_mota.grid(row=3, column=1, columnspan=3, padx=7, pady=7, sticky="w")

tk.Label(frame_info, text="Hướng dẫn viên:", bg=label_bg, fg=label_fg, font=("Arial", 10, "bold")).grid(row=4, column=0, padx=7, pady=7, sticky="w")
entry_huongdanvien = tk.Entry(frame_info, width=15, bg=entry_bg, fg=entry_fg, font=("Arial", 10))
entry_huongdanvien.grid(row=4, column=1, padx=7, pady=7, sticky="w")

# Thêm Khung nút bấm cho Tab 1
frame_buttons_tuyen = tk.Frame(tab1, pady=10)
frame_buttons_tuyen.pack(pady=5)
tk.Button(frame_buttons_tuyen, text="Thêm Tuyến", width=12, bg="#008CBA", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons_tuyen, text="Sửa Tuyến", width=12, bg="#FFA500", fg="black").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons_tuyen, text="Xóa Tuyến", width=12, bg="#DC143C", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons_tuyen, text="Làm Mới", width=12).pack(side=tk.LEFT, padx=10)

# Thêm Treeview và Scrollbar cho Tab 1
tree_frame_tuyen = tk.Frame(tab1, padx=10)
tree_frame_tuyen.pack(pady=10, padx=10, fill="both", expand=True)

# Đã định nghĩa tree_tuyendulich ở trên
tree_tuyendulich.heading('matuyen', text='Mã Tuyến')
tree_tuyendulich.heading('tentuyen', text='Tên Tuyến')
tree_tuyendulich.heading('diemkhoihanh', text='Khởi Hành')
tree_tuyendulich.heading('diemden', text='Địa Điểm Đến')
tree_tuyendulich.heading('thoiluong', text='Thời Lượng')
tree_tuyendulich.heading('giatour', text='Giá Tour')
tree_tuyendulich.heading('mota', text='Mô Tả')
tree_tuyendulich.heading('huongdanvien', text='Mã HDV')

tree_tuyendulich.column('matuyen', width=60, anchor='center')
tree_tuyendulich.column('tentuyen', width=150)
tree_tuyendulich.column('diemkhoihanh', width=100)
tree_tuyendulich.column('diemden', width=100)
tree_tuyendulich.column('thoiluong', width=80, anchor='center')
tree_tuyendulich.column('giatour', width=80, anchor='center')
tree_tuyendulich.column('mota', width=200)
tree_tuyendulich.column('huongdanvien', width=60, anchor='center')

scrollbar_tuyen = ttk.Scrollbar(tree_frame_tuyen, orient=tk.VERTICAL, command=tree_tuyendulich.yview)
tree_tuyendulich.configure(yscrollcommand=scrollbar_tuyen.set)
scrollbar_tuyen.pack(side=tk.RIGHT, fill=tk.Y)
tree_tuyendulich.pack(fill="both", expand=True)
load_data_tuyen() # Tải dữ liệu tuyến du lịch khi tab được tạo
# =================================================================
#                         TAB 2: CHI TIẾT HƯỚNG DẪN VIÊN 
# =================================================================

# ====== Tiêu đề ======
lbl_title = tk.Label(tab2, text="CHI TIẾT HƯỚNG DẪN VIÊN", font=("Arial", 18, "bold"), fg="blue")
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(tab2, padx=20, pady=10, relief=tk.GROOVE, borderwidth=1)
frame_info.pack(pady=5, padx=10, fill="x")

# Thiết lập khoảng cách cột
frame_info.columnconfigure(1, weight=1) 
frame_info.columnconfigure(3, weight=1) 

# --- Các trường nhập liệu ---
#1. Mã Hướng Dẫn Viên (mahdv)
tk.Label(frame_info, text="Mã HDV:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_mahdv = tk.Entry(frame_info, width=30) # KHÔNG CÓ state='readonly'
entry_mahdv.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# 2. Tên Hướng Dẫn Viên (tenhdv)
tk.Label(frame_info, text="Tên HDV:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_tenhdv = tk.Entry(frame_info, width=30)
entry_tenhdv.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# 3. Số Điện Thoại (sodienthoai)
tk.Label(frame_info, text="Số Điện Thoại:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_sdt = tk.Entry(frame_info, width=30)
entry_sdt.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# 4. Email (email)
tk.Label(frame_info, text="Email:", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
entry_email = tk.Entry(frame_info, width=30)
entry_email.grid(row=0, column=3, padx=10, pady=5, sticky="w")

# 5. Ngày Sinh (ngaysinh)
tk.Label(frame_info, text="Ngày Sinh:", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=5, sticky="w")
entry_ngaysinh = DateEntry(frame_info, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', year=1990)
entry_ngaysinh.grid(row=1, column=3, padx=10, pady=5, sticky="w")

# 6. Kinh Nghiệm (kinhnghiem)
tk.Label(frame_info, text="Kinh nghiệm (năm):", font=("Arial", 10)).grid(row=2, column=2, padx=10, pady=5, sticky="w")
entry_kinhnghiem = tk.Spinbox(frame_info, from_=0, to=50, width=5)
entry_kinhnghiem.grid(row=2, column=3, padx=10, pady=5, sticky="w")
entry_kinhnghiem.delete(0, tk.END) 
entry_kinhnghiem.insert(0, 0)


# ====== Frame nút chức năng ======
frame_buttons = tk.Frame(tab2, pady=10)
frame_buttons.pack(pady=10)

btn_them = tk.Button(frame_buttons, text="Thêm", width=12, bg="#4CAF50", fg="white", command=add_hdv)
btn_sua = tk.Button(frame_buttons, text="Sửa", width=12, bg="#FFC107", fg="black", command=update_hdv)
btn_xoa = tk.Button(frame_buttons, text="Xóa", width=12, bg="#F44336", fg="white", command=delete_hdv)
btn_lammoi = tk.Button(frame_buttons, text="Làm Mới", width=12, command=clear_entries)

btn_them.pack(side=tk.LEFT, padx=10)
btn_sua.pack(side=tk.LEFT, padx=10)
btn_xoa.pack(side=tk.LEFT, padx=10)
btn_lammoi.pack(side=tk.LEFT, padx=10)

# ====== Treeview để hiển thị dữ liệu HDV ======
tree_frame = tk.Frame(tab2, padx=10)
tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Define columns
columns = ('mahdv', 'tenhdv', 'sodienthoai', 'email', 'ngaysinh', 'kinhnghiem')
tree_hdv = ttk.Treeview(tree_frame, columns=columns, show='headings')

# Define headings and columns
tree_hdv.heading('mahdv', text='Mã HDV')
tree_hdv.heading('tenhdv', text='Tên HDV')
tree_hdv.heading('sodienthoai', text='SĐT')
tree_hdv.heading('email', text='Email')
tree_hdv.heading('ngaysinh', text='Ngày Sinh')
tree_hdv.heading('kinhnghiem', text='Kinh Nghiệm')

tree_hdv.column('mahdv', width=60, anchor='center')
tree_hdv.column('tenhdv', width=150)
tree_hdv.column('sodienthoai', width=100, anchor='center')
tree_hdv.column('email', width=200)
tree_hdv.column('ngaysinh', width=100, anchor='center')
tree_hdv.column('kinhnghiem', width=80, anchor='center')

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_hdv.yview)
tree_hdv.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree_hdv.pack(fill="both", expand=True)
tree_hdv.bind('<<TreeviewSelect>>', select_record)
load_data()
root.mainloop()
