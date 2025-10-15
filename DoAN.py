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
center_window(root, 900, 700)
root.resizable(False, False)
# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ Tuyến Du Lịch", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)
# ====== Frame nhập thông tin ======
# ...existing code...

frame_info = tk.LabelFrame(root, text="Thông tin tuyến du lịch", font=("Arial", 12, "bold"), bg="#cce6ff", fg="black")
frame_info.pack(pady=10, padx=10, fill="x")

tk.Label(frame_info, text="Mã Tuyến Du Lịch:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_matuyen = tk.Entry(frame_info, width=15)
entry_matuyen.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Tên Tuyến:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_tentuyen = tk.Entry(frame_info, width=25)
entry_tentuyen.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Điểm Khởi Hành:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_diemkhoihanh = tk.Entry(frame_info, width=15)
entry_diemkhoihanh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Địa điểm đến:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_diemden = tk.Entry(frame_info, width=15)
entry_diemden.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Thời lượng:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_thoiluong = tk.Entry(frame_info, width=15)
entry_thoiluong.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Giá tour:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=5, pady=5, sticky="w")
entry_giatour = tk.Entry(frame_info, width=15)
entry_giatour.grid(row=2, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Mô tả:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_mota = tk.Entry(frame_info, width=40)
entry_mota.grid(row=3, column=1, columnspan=4, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Hướng dẫn viên:", bg="#00e1ff", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_huongdanvien = tk.Entry(frame_info, width=15)
entry_huongdanvien.grid(row=4, column=1, padx=5, pady=5, sticky="w")
# ...existing code...

lbl_ds = tk.Label(root, text="Danh sách tuyến du lịch", font=("Arial", 10, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("matuyen", "tentuyen", "diemkhoihanh", "diemden", "thoiluong", "giatour", "mota", "huongdanvien")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.column("matuyen", width=80, anchor="center")
tree.column("tentuyen", width=150)
tree.column("diemkhoihanh", width=120)
tree.column("diemden", width=120)
tree.column("thoiluong", width=100)
tree.column("giatour", width=100, anchor="e")
tree.column("mota", width=200)
tree.column("huongdanvien", width=120)
tree.pack(padx=10, pady=5, fill="both")

# ====== Chức năng clear input ======
def clear_input():
    entry_matuyen.delete(0, tk.END)
    entry_tentuyen.delete(0, tk.END)
    entry_diemkhoihanh.delete(0, tk.END)
    entry_diemden.delete(0, tk.END)
    entry_thoiluong.delete(0, tk.END)
    entry_giatour.delete(0, tk.END)
    entry_mota.delete(0, tk.END)
    entry_huongdanvien.delete(0, tk.END)

# ...existing code...

def them_tuyendulich():
    matuyen = entry_matuyen.get()
    tentuyen = entry_tentuyen.get()
    diemkhoihanh = entry_diemkhoihanh.get()
    diemden = entry_diemden.get()
    thoiluong = entry_thoiluong.get()
    giatour = entry_giatour.get()
    mota = entry_mota.get()
    huongdanvien = entry_huongdanvien.get()
    if not (matuyen and tentuyen and diemkhoihanh and diemden):
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin!")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO tuyendulich VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (matuyen, tentuyen, diemkhoihanh, diemden, thoiluong, giatour, mota, huongdanvien)
        )
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_tuyendulich():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn tuyến du lịch để xóa!")
        return
    matuyen = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tuyendulich WHERE matuyen=%s", (matuyen,))
    conn.commit()
    conn.close()
    load_data()

def sua_tuyendulich():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn tuyến du lịch để sửa!")
        return
    values = tree.item(selected)["values"]
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, values[0])
    entry_tentuyen.delete(0, tk.END)
    entry_tentuyen.insert(0, values[1])
    entry_diemkhoihanh.delete(0, tk.END)
    entry_diemkhoihanh.insert(0, values[2])
    entry_diemden.delete(0, tk.END)
    entry_diemden.insert(0, values[3])
    entry_thoiluong.delete(0, tk.END)
    entry_thoiluong.insert(0, values[4])
    entry_giatour.delete(0, tk.END)
    entry_giatour.insert(0, values[5])
    entry_mota.delete(0, tk.END)
    entry_mota.insert(0, values[6])
    entry_huongdanvien.delete(0, tk.END)
    entry_huongdanvien.insert(0, values[7])

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tuyendulich")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def clear_input():
    entry_matuyen.delete(0, tk.END)
    entry_tentuyen.delete(0, tk.END)
    entry_diemkhoihanh.delete(0, tk.END)
    entry_diemden.delete(0, tk.END)
    entry_thoiluong.delete(0, tk.END)
    entry_giatour.delete(0, tk.END)
    entry_mota.delete(0, tk.END)
    entry_huongdanvien.delete(0, tk.END)
# ...existing code...
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

btn_them = tk.Button(frame_btn, text="Thêm", width=10, command=them_tuyendulich)
btn_them.pack(side="left", padx=5)

btn_sua = tk.Button(frame_btn, text="Sửa", width=10, command=sua_tuyendulich)
btn_sua.pack(side="left", padx=5)

btn_xoa = tk.Button(frame_btn, text="Xóa", width=10, command=xoa_tuyendulich)
btn_xoa.pack(side="left", padx=5)

btn_clear = tk.Button(frame_btn, text="Clear", width=10, command=clear_input)
btn_clear.pack(side="left", padx=5)
# ...existing code...

load_data()
root.mainloop()