# main_app.py

import tkinter as tk
from tkinter import ttk, Menu, messagebox
import sys

# Import modules
from database import conn, check_db_connection 
from hdv_module import HDVManager
from tuyen_module import TuyenManager 

# --- Helper Functions ---
def center_window(win, w=850, h=700):
    """Căn giữa cửa sổ ứng dụng."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# --- Main Application Setup ---
root = tk.Tk()
root.title("Quản Lý Tuyến Du Lịch & Hướng Dẫn Viên")
center_window(root)
root.resizable(False, False)

# KIỂM TRA KẾT NỐI CSDL: Nếu thất bại, ứng dụng sẽ tự động đóng.
if not check_db_connection(root):
    # check_db_connection sẽ gọi root.destroy() và sys.exit() nếu lỗi
    pass 

# --- Menu Bar ---
menu = Menu(root)
file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label='Exit', command=root.quit)
menu.add_cascade(label='File', menu=file_menu)
help_menu = Menu(menu, tearoff=0)
help_menu.add_command(label='About')
menu.add_cascade(label='Help', menu=help_menu)
root.config(menu=menu)

# --- Notebook (Tab Control) ---
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control) # Tuyến Du Lịch
tab2 = ttk.Frame(tab_control) # Hướng Dẫn Viên
tab3 = ttk.Frame(tab_control) # Địa Điểm

tab_control.add(tab1, text='Quản Lý Tuyến Du Lịch')
tab_control.add(tab2, text='Chi tiết huóng dẫn viên')
tab_control.add(tab3, text='Chi tiết các đia điểm')
tab_control.pack(expand=1, fill='both')

# =================================================================
# KHỞI TẠO CÁC MODULE QUẢN LÝ (Giao diện và logic)
# =================================================================

# 1. Khởi tạo Tab 1: Quản lý Tuyến Du Lịch
tuyen_manager = TuyenManager(tab1) 

# 2. Khởi tạo Tab 2: Chi tiết Hướng Dẫn Viên
hdv_manager = HDVManager(tab2) 

# 3. Tab 3 (Chưa có logic)
frame_title_tab3 = tk.Frame(tab3, bg="#f2f6fc")
frame_title_tab3.pack(fill="x", pady=12, padx=15)
tk.Label(frame_title_tab3, text="QUẢN LÝ ĐỊA ĐIỂM DU LỊCH", font=("Arial", 20, "bold"), bg="#f2f6fc", fg="#2d5c88").pack(side="left")

# Khởi chạy ứng dụng
root.mainloop()

# Đóng kết nối khi ứng dụng thoát
if conn and conn.is_connected():
    conn.close()