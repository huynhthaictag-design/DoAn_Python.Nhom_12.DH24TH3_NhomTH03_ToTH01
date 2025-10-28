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
# maso INT PRIMARY KEY,
# tentuyen VARCHAR(255),
# diemkhoihanh VARCHAR(100),
# diemden VARCHAR(100),
# thoiluong VARCHAR(50),
# giatour DECIMAL(10, 2),
# mota TEXT,
# huongdanvien VARCHAR(100)
# );
def center_window(win, w=900, h=700):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý Tuyến Du Lịch")
root.configure(bg="#f2f6fc")
center_window(root, 900, 700)
root.resizable(False, False)


frame_title = tk.Frame(root, bg="#f2f6fc")
frame_title.pack(fill="x", pady=12, padx=15)

lbl_title = tk.Label(frame_title, text="QUẢN LÝ Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#f2f6fc", fg="#2d5c88")
lbl_title.pack(side="left")

tk.Label(frame_title, text="Tìm Mã Tuyến:", bg="#f2f6fc", fg="#2d5c88", font=("Arial", 10)).pack(side="left", padx=(20,5))
entry_search_id = tk.Entry(frame_title, width=10, bg="#ffffff", fg="#2d5c88", font=("Arial", 10))
entry_search_id.pack(side="left")

def search_by_matuyen():
    timkiem = entry_search_id.get().strip()
    # nếu rỗng thì load lại tất cả
    if not timkiem:
        load_data()
        return
    # tìm theo Mã tuyến chính xác
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tuyendulich WHERE matuyen=%s", (timkiem,))
        # xóa tree hiện tại
        for i in tree.get_children():
            tree.delete(i)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        conn.close()

btn_search_id = tk.Button(frame_title, text="Tìm", command=search_by_matuyen, bg="#4da6ff", fg="white", font=("Arial", 9))
btn_search_id.pack(side="left", padx=(6,0))

# cho phép nhấn Enter để tìm
entry_search_id.bind("<Return>", lambda e: search_by_matuyen())

# ====== Frame nhập thông tin ======
frame_info = tk.LabelFrame(root, text="Thông tin tuyến du lịch", font=("Arial", 13, "bold"), bg="#e3ecfa", fg="#2d5c88", bd=2)
frame_info.pack(pady=10, padx=15, fill="x")

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

# ====== Danh sách tuyến du lịch ======
lbl_ds = tk.Label(root, text="Danh sách tuyến du lịch", font=("Arial", 11, "bold"), bg="#f2f6fc", fg="#2d5c88")
lbl_ds.pack(pady=7, anchor="w", padx=15)

columns = ("matuyen", "tentuyen", "diemkhoihanh", "diemden", "thoiluong", "giatour", "mota", "huongdanvien")

style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#e3ecfa", foreground="#2d5c88", fieldbackground="#e3ecfa", font=("Arial", 10))
style.configure("Treeview.Heading", background="#b3d1ff", foreground="#1a3c6e", font=("Arial", 10, "bold"))

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
tree.pack(padx=15, pady=7, fill="both")

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

# ====== Chức năng thêm, xóa, sửa ======
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

# ====== Frame nút chức năng ======
frame_btn = tk.Frame(root, bg="#f2f6fc")
frame_btn.pack(pady=10)

btn_them = tk.Button(frame_btn, text="Thêm", width=10, command=them_tuyendulich, bg="#4da6ff", fg="white", font=("Arial", 10, "bold"))
btn_them.pack(side="left", padx=7)

btn_sua = tk.Button(frame_btn, text="Sửa", width=10, command=sua_tuyendulich, bg="#66cc99", fg="white", font=("Arial", 10, "bold"))
btn_sua.pack(side="left", padx=7)

btn_xoa = tk.Button(frame_btn, text="Xóa", width=10, command=xoa_tuyendulich, bg="#ff6666", fg="white", font=("Arial", 10, "bold"))
btn_xoa.pack(side="left", padx=7)

btn_clear = tk.Button(frame_btn, text="Clear", width=10, command=clear_input, bg="#b3b3b3", fg="white", font=("Arial", 10, "bold"))
btn_clear.pack(side="left", padx=7)

# ====== Load dữ liệu ban đầu ======
load_data()
root.mainloop()