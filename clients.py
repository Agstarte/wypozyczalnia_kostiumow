import tkinter as tk
from tkinter import *
from tkinter import Text
import os
import mysql.connector



def clients(database, root):
    top = Toplevel()
    top.title("Zarządzanie klientami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    label = Label(top, text='tutaj tekst', padx=50, pady=5).pack()