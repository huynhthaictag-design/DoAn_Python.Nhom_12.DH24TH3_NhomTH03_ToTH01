import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import hashlib

def dangnhap():
        return mysql.connector.connect(
        host="localhost",
        user='root',
        password='1234',
        database="login"
    )
# CREATE TABLE login (
#     tendangnhap VARCHAR(50) PRIMARY KEY,
#     matkhau VARCHAR(255)
# );
conn = dangnhap()
if conn and conn.is_connected():
    print("Kết nối thành công!")
else:
    messagebox.showerror("Lỗi kết nối", "Không thể kết nối tới MySQL. Kiểm tra cấu hình.")

def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

root = tk.Tk()
root.title("Tạo tài khoản")
center_window(root, 700, 500)
root.resizable(False, False)
frame_info = tk.Frame(root)
frame_info.pack(padx=10, pady=10)

tk.Label(frame_info, text="Tên đăng nhập").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_ttdn = tk.Entry(frame_info, width=30)
entry_ttdn.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Mật khẩu").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_tmk = tk.Entry(frame_info, width=30, show="*")
entry_tmk.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Nhập lại mật khẩu").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_nlmk = tk.Entry(frame_info, width=30, show="*")
entry_nlmk.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# --- Thêm chức năng tạo tài khoản và lưu vào bảng login ---
def hash_password(matkhau: str) -> str:
    # Dùng SHA-256 cho mục học; production nên dùng bcrypt/PBKDF2 + salt
    return hashlib.sha256(matkhau.encode('utf-8')).hexdigest()

def user_exists(username: str) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM `login` WHERE tendangnhap = %s LIMIT 1", (username,))
        exists = cur.fetchone() is not None
        cur.close()
        return exists
    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi DB", f"Lỗi kiểm tra người dùng: {e}")
        return False

def create_user_db(tendangnhap: str, matkhau: str) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO `login` (tendangnhap, matkhau) VALUES (%s, %s)",
                    (tendangnhap, hash_password(matkhau)))
        conn.commit()
        cur.close()
        return True
    except mysql.connector.IntegrityError:
        return False
    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi DB", f"Lỗi khi tạo tài khoản: {e}")
        return False

def tao_tk():
    tendangnhap = entry_ttdn.get().strip()
    matkhau = entry_tmk.get()
    pw2 = entry_nlmk.get()
    if not tendangnhap or not matkhau:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên đăng nhập và mật khẩu.")
        return
    if pw != pw2:
        messagebox.showwarning("Sai mật khẩu", "Mật khẩu và xác nhận không khớp.")
        return
    if user_exists(tendangnhap):
        messagebox.showinfo("Đã tồn tại", "Tên đăng nhập đã tồn tại, hãy chọn tên khác.")
        return
    ok = create_user_db(tendangnhap, matkhau)
    if ok:
        messagebox.showinfo("Thành công", "Tạo tài khoản thành công.")
        entry_ttdn.delete(0, tk.END)
        entry_tmk.delete(0, tk.END)
        entry_nlmk.delete(0, tk.END)
    else:
        messagebox.showerror("Thất bại", "Không thể tạo tài khoản. Xem logs.")

frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)
tk.Button(frame_btn, text="Tạo", width=8, command=tao_tk).grid(row=0, column=0, padx=5)

def on_closing():
    try:
        if conn:
            conn.close()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()