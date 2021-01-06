import tkinter as tk
from tkinter import Text
import os
import mysql.connector
from tkinter import *
from tkinter import messagebox


def products(database, root):
    root.withdraw()  # minimalizowanie głównego okna
    top = Toplevel()
    top.title("Zarządzanie produktami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    def add_function():
        add_product = Toplevel()
        add_product.title("Dodaj produkt")
        add_product.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(add_product)
        blank.grid(row=0, column=1)
        blank = Label(add_product, width=6)
        blank.grid(row=0, column=0)
        Label(add_product, text="Podaj dane nowego produktu").grid(row=1, column=1, columnspan=2)

        columns = ["id_produktu", "nazwa", "liczba_wszystkich_sztuk", "liczba_dostepnych_sztuk", "id_opisu", "cena"]
        dane = []

        for i in range(6):
            e = tk.Entry(add_product, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(add_product, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            dane.append(e)

            def add():
                cursor = database.cursor()

                if str(dane[1].get()) == '' or str(dane[2].get()) == '' or str(dane[3].get()) == '' or str(dane[4].get()) == '' or str(dane[5].get()) == '':
                    messagebox.showerror("Błąd", "Id produktu, nazwa, liczba wszystkich sztuk, liczba dostępnych "
                                                 "sztuk, id_opisu ani cena nie mogą być puste!")
                    return

                try:
                    cursor.execute(
                        f"INSERT INTO produkt (id_produktu, nazwa, liczba_wszystkich_sztuk, liczba_dostepnych_sztuk, id_opisu, cena)"
                        f"VALUES ('{dane[0].get()}','{dane[1].get()}','{dane[2].get()}','{dane[3].get()}','{dane[4].get()}','{dane[5].get()}')")
                except Exception as e:
                    messagebox.showerror("Błąd", e)
                    return

                database.commit()
                messagebox.showinfo("Informacja", "Pomyślnie dodano produkt")



            blank = Label(add_product)
            blank.grid(row=21, column=1)
            Button(add_product, text="Dodaj", command=add).grid(row=22, column=1, columnspan=2)
            blank = Label(add_product)
            blank.grid(row=22, column=1)
        add_product.mainloop()

    def exit_function():
        top.destroy()
        root.deiconify()

    add_button = tk.Button(top, text="Dodaj produkt", width=25, pady=5, fg="black", bg="#bfa7a8",
                           command=add_function)
    add_button.pack()

    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", width=15, pady=5, fg="black", bg="#bfa7a8",
                            command=exit_function)
    exit_button.pack()
    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
