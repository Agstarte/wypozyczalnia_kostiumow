import tkinter as tk
from tkinter import Text
import os
import mysql.connector

def main_window(database):
    print(database)
    root = tk.Tk()
    root.title('Wypozyczalnia kostiumow')
    root.geometry("350x350")

    # canvas = tk.Canvas(root, height=350, width=350, bg="#c3a7a8")
    # canvas.pack()


    def button1_function():
        print("You clicked button1")


    def button2_function():
        print("You clicked button2")


    text = tk.Label(root, text='tutaj tekst', padx=50, pady=5)
    text.grid(row=0, column=2)

    button1 = tk.Button(root, text="Button", padx=10, pady=5, fg="black", bg="#bfa7a8", command=button1_function)
    button1.grid(row=2, column=2)

    button2 = tk.Button(root, text="Button2", padx=10, pady=5, bg="#bfa7a8", fg="black", command=button2_function)
    button2.grid(row=2, column=4)

    root.mainloop()
