import tkinter as tk
from tkinter import *
from tkinter import Text
import os
import mysql.connector



def clients(database, root):
    top = Toplevel()
    top.title("Zarządzanie klientami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    def add_function():
        pass

    def show_function():
        pass

    def edit_function():
        pass

    def exit_function():
        top.destroy()

    blank = Label(top)
    blank.pack()
    blank = Label(top)
    blank.pack()
    blank = Label(top, text="Zarządzaj klientami")
    blank.pack()
    blank = Label(top)
    blank.pack()

    clients_button = tk.Button(top, text="         Dodaj klienta         ", padx=15, pady=5, fg="black", bg="#bfa7a8",
                               command=add_function)
    clients_button.pack()

    blank = Label(top)
    blank.pack()

    products_button = tk.Button(top, text="      Wyświetl klienta      ", padx=15, pady=5, fg="black", bg="#bfa7a8",
                                command=show_function)
    products_button.pack()

    blank = Label(top)
    blank.pack()

    reservations_button = tk.Button(top, text="Modyfikuj dane klienta", padx=15, pady=5, fg="black", bg="#bfa7a8",
                                    command=edit_function)
    reservations_button.pack()

    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", padx=30, pady=5, fg="black", bg="#bfa7a8",
                                    command=exit_function)
    exit_button.pack()
