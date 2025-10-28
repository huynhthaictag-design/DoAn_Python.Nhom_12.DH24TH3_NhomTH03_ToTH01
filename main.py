import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import mysql.connector
from tkinter import *
from tkinter import Menu
# --- Database Connection ---
# Giữ lại hàm kết nối CSDL nếu cần
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user='root',
            password='1234',
            database="qltuyendulich"
        )
        if conn.is_connected():
            print("Kết nối thành công!")
            return conn
        return None
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối MySQL: {err}")
        return None

# --- Utility Function ---
window = Tk()
window.title("Quản Lý Tuyến Du Lịch")

menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='New File')
new_item.add_separator()
new_item.add_command(label='Open File')
menu.add_cascade(label='File', menu=new_item)
window.config(menu=menu)
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Quản Lý Tuyến Du Lịch')
tab_control.add(tab2, text='Chi tiết huóng dẫn viên')
tab_control.pack(expand=1, fill='both')
window.mainloop()