import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import webbrowser
def connect_db():
 return mysql.connector.connect(
 host="localhost",
 user='root',
 password='1234', 
 database="qltuyendulich"
 )
conn = connect_db()
if conn.is_connected():
    print("Kết nối thành công!")
else:
    print("Kết nối thất bại!")
# CREATE DATABASE qltuyendulich CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# USE qltuyendulich;
# CREATE TABLE tuyendulich (
#  INT PRIMARY KEY,
# tentuyen VARCHAR(255),
# diemkhoihanh VARCHAR(100),
# diemden VARCHAR(100),
# thoiluong VARCHAR(50),
# giatour DECIMAL(10, 2),
# mota TEXT,
# huongdanvien VARCHAR(100)
# );
def center_window(win, w=700, h=500):
 ws = win.winfo_screenwidth()
 hs = win.winfo_screenheight()
 x = (ws // 2) - (w // 2)
 y = (hs // 2) - (h // 2)
 win.geometry(f'{w}x{h}+{x}+{y}')
# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý Tuyến Du Lịch")
center_window(root, 700, 500)
root.resizable(False, False)
# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ Tuyến Du Lịch", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)
# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")
tk.Label(frame_info, text="Mã Tuyến Du Lịch").grid(row=0, column=0, padx=5, pady=5, 
sticky="w")
entry_matuyen = tk.Entry(frame_info, width=10)
entry_matuyen.grid(row=0, column=1, padx=5, pady=5, sticky="w")
tk.Label(frame_info, text="Tên Tuyến").grid(row=0, column=2, padx=5, pady=5, 
sticky="w")
entry_tentuyen = tk.Entry(frame_info, width=30)
entry_tentuyen.grid(row=0, column=3, padx=5, pady=5, sticky="w")
#----------------------------------------
tk.Label(frame_info, text="Điểm Khởi Hành").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_diemkhoihanh = tk.Entry(frame_info, width=25)
entry_diemkhoihanh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

def open_map():
    address = entry_diemkhoihanh.get()
    if address:
        url = f"https://www.google.com/maps/search/{address}"
        webbrowser.open(url)
    else:
        messagebox.showwarning("Thông báo", "Vui lòng nhập địa chỉ điểm khởi hành!")

btn_chon_diem = tk.Button(frame_info, text="Kiểm Tra Vị TRí", command=open_map)
btn_chon_diem.grid(row=1, column=2, padx=5, pady=5, sticky="w")
tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_ten = tk.Entry(frame_info, width=15)
entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")
tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5, sticky="w")
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, 
value="Nam").grid(row=2, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, 
column=1, padx=60, sticky="w")
root.mainloop()
