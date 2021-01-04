import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
import main_window

root = tk.Tk()
root.title('Wypożyczalnia kostiumów - login')

w = 350
h = 175
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))



blank = Label(root)
blank.pack()

login = Entry(root, width=20)
password = Entry(root, width=20, show="*")
login_label = Label(root, text="Login", width=10)
password_label = Label(root, text="Haslo")

login_label.pack()
login.pack()
password_label.pack()
password.pack()


def log_me():
    try:
        database = mysql.connector.connect(
            host="localhost",
            user=login.get(),
            password=password.get(),
            database="wypozyczalnia_kostiumow"
        )
        root.destroy()
        main_window.main_window(database, root)
    except:
        messagebox.showerror("Błąd", "Wprowadzono niepoprawne dane.")


blank = Label(root)
blank.pack()
login_button = Button(root, text="Zaloguj się", command=log_me)
login_button.pack()

root.mainloop()
