import tkinter as tk
from tkinter import Text
import os
import mysql.connector
import clients



def main_window(database, root):
    print(database)
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
        print("You clicked button1")
        clients.clients(database, root)

    text = tk.Label(root, text='tutaj tekst', padx=50, pady=5)
    text.grid(row=0, column=2)

    clients_button = tk.Button(root, text="Zarządzanie klientami", padx=10, pady=5, fg="black", bg="#bfa7a8", command=clients_function)
    clients_button.grid(row=2, column=2)

    root.mainloop()
