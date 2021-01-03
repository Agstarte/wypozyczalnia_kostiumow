import tkinter as tk
from tkinter import *
import mysql.connector


root = tk.Tk()
root.title('Wypozyczalnia kostiumow - login')
root.geometry('350x175')


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
    database = mysql.connector.connect(
        host="localhost",
        user=login.get(),
        password=password.get(),
        database="wypozyczalnia_kostiumow"
    )
    print(database)


blank = Label(root)
blank.pack()
login_button = Button(root, text="Zaloguj sie", command=log_me)
login_button.pack()

root.mainloop()
