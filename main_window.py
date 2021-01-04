import tkinter as tk
from tkinter import Text
import os
import mysql.connector
import test



def main_window(database, root):
    print(database)
    root = tk.Tk()
    root.title('Wypozyczalnia kostiumow')
    w = 350
    h = 350
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


    # canvas = tk.Canvas(root, height=350, width=350, bg="#c3a7a8")
    # canvas.pack()


    def button1_function():
        print("You clicked button1")
        test.test(database, root)


    def button2_function():
        print("You clicked button2")


    text = tk.Label(root, text='tutaj tekst', padx=50, pady=5)
    text.grid(row=0, column=2)

    button1 = tk.Button(root, text="Button", padx=10, pady=5, fg="black", bg="#bfa7a8", command=button1_function)
    button1.grid(row=2, column=2)

    button2 = tk.Button(root, text="Button2", padx=10, pady=5, bg="#bfa7a8", fg="black", command=button2_function)
    button2.grid(row=2, column=4)

    root.mainloop()
