import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
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


root.mainloop()