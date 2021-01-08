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

                if str(dane[1].get()) == '' or str(dane[2].get()) == '' or str(dane[3].get()) == '' or str(
                        dane[4].get()) == '' or str(dane[5].get()) == '':
                    messagebox.showerror("Błąd", "Nazwa, liczba wszystkich sztuk, liczba dostępnych "
                                                 "sztuk, id_opisu ani cena nie mogą być puste!")
                    return

                try:
                    cursor.execute(
                        f"INSERT INTO produkt (id_produktu, nazwa, liczba_wszystkich_sztuk, liczba_dostepnych_sztuk, "
                        f"id_opisu, cena) "
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

    def show_function():
        show_product = Toplevel()
        show_product.title("Wyświetl produkt")
        show_product.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(show_product)
        blank.grid(row=0, column=1)
        blank = Label(show_product, width=6)
        blank.grid(row=0, column=0)
        Label(show_product, text="Podaj identyfikator produktu").grid(row=1, column=1, columnspan=2)
        product_id = Entry(show_product, width=20)
        product_id.grid(row=2, column=1, columnspan=2)

        columns = ["id_produktu", "nazwa", "liczba_wszystkich_sztuk", "liczba_dostepnych_sztuk", "id_opisu", "cena"]

        for i in range(6):
            e = tk.Entry(show_product, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(show_product, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM produkt WHERE id_produktu = {product_id.get()}")
                product = cursor.fetchall()

                if str(product[0][0]) == 'None':
                    return

                for i in range(6):
                    e = tk.Entry(show_product, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(product[0][i]))
                    e.config(state='disabled')
            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        #
        blank = Label(show_product)
        blank.grid(row=3, column=1)
        Button(show_product, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=1,
                                                                                        columnspan=2)
        blank = Label(show_product)
        blank.grid(row=5, column=1)

        show_product.mainloop()

    def edit_function():

        edit_product = Toplevel()
        edit_product.title("Modyfikuj dane produktu")
        edit_product.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(edit_product)
        blank.grid(row=0, column=1)
        blank = Label(edit_product, width=6)
        blank.grid(row=0, column=0)
        Label(edit_product, text="Podaj identyfikator produktu").grid(row=1, column=1, columnspan=2)
        product_id = Entry(edit_product, width=20)
        product_id.grid(row=2, column=1, columnspan=2)

        columns = ["id_produktu", "nazwa", "liczba_wszystkich_sztuk", "liczba_dostepnych_sztuk", "id_opisu", "cena"]
        dane = []

        for i in range(6):
            e = tk.Entry(edit_product, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(edit_product, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')
            dane.append(e)

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM produkt WHERE id_produktu = {product_id.get()}")
                product = cursor.fetchall()

                if str(product[0][0]) == 'None':
                    return

                dane[0].delete(0, 'end')
                dane[0].config(state='normal')
                dane[0].insert(END, str(product[0][0]))
                dane[0].config(state='disabled')

                # for i in range(6):
                #     if i==0:
                #         dane[0].delete(0, 'end')
                #         dane[0].config(state='normal')
                #         dane[0].insert(END, str(product[0][0]))
                #         dane[0].config(state='disabled')
                #     dane[i].delete(0, 'end')
                #     dane[i].config(state='normal')
                #     dane[i].insert(END, str(product[0][i]))
                # update_button.configure(state=NORMAL)

                for i in range(1, 6):
                    dane[i].delete(0, 'end')
                    dane[i].config(state='normal')
                    dane[i].insert(END, str(product[0][i]))
                update_button.configure(state=NORMAL)

            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        def update():
            cursor = database.cursor()
            if str(dane[1].get()) == '' or str(dane[2].get()) == '' or str(dane[3].get()) == '' or str(
                    dane[4].get()) == '' or str(dane[5].get()) == '':
                messagebox.showerror("Błąd", "Nazwa, liczba wszystkich sztuk, liczba dostępnych "
                                             "sztuk, id_opisu ani cena nie mogą być puste!")
                return
            try:
                cursor.execute(f"UPDATE produkt SET id_produktu = {dane[0].get()}, nazwa = '{dane[1].get()}',"
                               f" liczba_wszystkich_sztuk = '{dane[2].get()}', liczba_dostepnych_sztuk = '{dane[3].get()}', id_opisu = '{dane[4].get()}', cena = '{dane[5].get()}'"
                               f"WHERE id_produktu = {product_id.get()}")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            messagebox.showinfo("Informacja", "Pomyślnie zmieniono dane produktu")
            database.commit()

        blank = Label(edit_product)
        blank.grid(row=3, column=1)
        Button(edit_product, text="Pokaż", fg="black", bg="#bfa7a8", width=10, command=show).grid(row=4, column=1)
        blank = Label(edit_product)
        blank.grid(row=5, column=1)

        update_button = Button(edit_product, text="Aktualizuj", fg="black", bg="#bfa7a8", width=10, command=update)
        update_button.grid(row=4, column=2)
        update_button.configure(state=DISABLED)
        edit_product.mainloop()

    def add_copies():
        add_copy = Toplevel()
        add_copy.title("Dodaj produkt")
        add_copy.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(add_copy)
        blank.grid(row=0, column=1)
        blank = Label(add_copy, width=6)
        blank.grid(row=0, column=0)
        Label(add_copy, text="Podaj dane nowego egzemplarzu").grid(row=1, column=1, columnspan=2)

        columns = ["id_egzemplarza", "id_produktu", "id_rezerwacji", "rozmiar", "stan"]
        dane = []

        for i in range(5):
            e = tk.Entry(add_copy, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(add_copy, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            dane.append(e)

        def add():
            cursor = database.cursor()

            if str(dane[0].get()) == '' or str(dane[1].get()) == '':
                messagebox.showerror("Błąd", "Id_egzemplarza oraz id_produktu nie może być puste")
                return

            try:
                cursor.execute(
                    f"INSERT INTO egzemplarz (id_egzemplarza, id_produktu, id_rezerwacji, rozmiar, stan)"
                    f"VALUES ('{dane[0].get()}','{dane[1].get()}','{dane[2].get()}','{dane[3].get()}','{dane[4].get()}')")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return

            database.commit()
            messagebox.showinfo("Informacja", "Pomyślnie dodano egzemplarz")

        blank = Label(add_copy)
        blank.grid(row=11, column=1)
        Button(add_copy, text="Dodaj", fg="black", bg="#bfa7a8", command=add).grid(row=12, column=1, columnspan=2)
        blank = Label(add_copy)
        blank.grid(row=5, column=1)

        add_copy.mainloop()



    def show_copy_function():
        show_copy = Toplevel()
        show_copy.title("Wyświetl egzemplarz")
        show_copy.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(show_copy)
        blank.grid(row=0, column=1)
        blank = Label(show_copy, width=6)
        blank.grid(row=0, column=0)
        Label(show_copy, text="Podaj identyfikator produktu").grid(row=1, column=1, columnspan=2)
        copy_id = Entry(show_copy, width=20)
        copy_id.grid(row=2, column=1, columnspan=2)

        columns = ["id_egzemplarza", "id_produktu", "id_rezerwacji", "rozmiar", "stan"]

        for i in range(5):
            e = tk.Entry(show_copy, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(show_copy, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM egzemplarz WHERE id_produktu = {copy_id.get()}")
                product = cursor.fetchall()

                if str(product[0][0]) == 'None':
                    return

                for i in range(5):
                    e = tk.Entry(show_copy, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(product[0][i]))
                    e.config(state='disabled')
            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        #
        blank = Label(show_copy)
        blank.grid(row=3, column=1)
        Button(show_copy, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=1,
                                                                                        columnspan=2)
        blank = Label(show_copy)
        blank.grid(row=5, column=1)

        show_copy.mainloop()

    def exit_function():
        top.destroy()
        root.deiconify()

    blank = Label(top)
    blank.pack()
    blank = Label(top)
    blank.pack()
    blank = Label(top, text="Zarządzaj klientami")
    blank.pack()
    blank = Label(top)
    blank.pack()

    add_button = tk.Button(top, text="Dodaj produkt", width=25, pady=5, fg="black", bg="#bfa7a8",
                           command=add_function)
    add_button.pack()

    blank = Label(top)
    blank.pack()

    show_button = tk.Button(top, text="Wyświetl produkt", width=25, pady=5, fg="black", bg="#bfa7a8",
                            command=show_function)
    show_button.pack()

    blank = Label(top)
    blank.pack()

    edit_button = tk.Button(top, text="Modyfikuj dane produktu", width=25, pady=5, fg="black", bg="#bfa7a8",
                            command=edit_function)
    edit_button.pack()

    blank = Label(top)
    blank.pack()

    edit_button = tk.Button(top, text="Dodaj egzemplarz", width=25, pady=5, fg="black", bg="#bfa7a8",
                            command=add_copies)
    edit_button.pack()

    blank = Label(top)
    blank.pack()

    edit_button = tk.Button(top, text="Wyświetl egzemplarze", width=25, pady=5, fg="black", bg="#bfa7a8",
                            command=show_copy_function)
    edit_button.pack()

    blank = Label(top)
    blank.pack()



    exit_button = tk.Button(top, text="Powrót", width=15, pady=5, fg="black", bg="#bfa7a8",
                            command=exit_function)
    exit_button.pack()
    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
