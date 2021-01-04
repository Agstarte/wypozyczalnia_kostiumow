import tkinter as tk
from tkinter import Text
import os
import mysql.connector
from tkinter import *
from tkinter import messagebox


def reservations(database, root):
    root.withdraw()  # minimalizowanie głównego okna
    top = Toplevel()
    top.title("Zarządzanie rezerwacjami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    def exit_function():
        top.destroy()
        root.deiconify()

    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
