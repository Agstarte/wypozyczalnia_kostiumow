import tkinter as tk
from tkinter import *
from tkinter import Text
import os
import mysql.connector
import clients


def main_window(database, root):
    root = tk.Tk()
    root.title('Wypożyczalnia kostiumów')
    w = 350
    h = 350
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # canvas = tk.Canvas(root, height=350, width=350, bg="#c3a7a8")
    # canvas.pack()

    def clients_function():
        clients.clients(database, root)

    def products_function():
        print("Zarządzanie produktami")
        # clients.clients(database, root)

    def reservations_function():
        print("Zarządzanie rezerwacjami")
        # clients.clients(database, root)

    blank = Label(root)
    blank.pack()
    blank = Label(root)
    blank.pack()
    blank = Label(root, text="Menu")
    blank.pack()
    blank = Label(root)
    blank.pack()

    clients_button = tk.Button(root, text="Zarządzanie klientami", padx=10, pady=5, fg="black", bg="#bfa7a8",
                               command=clients_function)
    clients_button.pack()

    blank = Label(root)
    blank.pack()

    products_button = tk.Button(root, text="Zarządzanie klientami", padx=10, pady=5, fg="black", bg="#bfa7a8",
                                command=products_function)
    products_button.pack()

    blank = Label(root)
    blank.pack()

    reservations_button = tk.Button(root, text="Zarządzanie klientami", padx=10, pady=5, fg="black", bg="#bfa7a8",
                                    command=reservations_function)
    reservations_button.pack()

    root.mainloop()
