import tkinter as tk
from tkinter import ttk
from tkinter import Text
import os
import mysql.connector
from tkinter import *
from tkinter import messagebox


def products(database, root):
    root.withdraw()  # minimalizowanie głównego okna
    top = Toplevel()
    top.title("Zarządzanie produktami")
    top.geometry(f"350x550+{root.winfo_x()}+{root.winfo_y()}")

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
        edit_product.geometry(f"400x250+{top.winfo_x()}+{top.winfo_y() + 50}")

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
                dane[0].delete(0, 'end')
                dane[0].insert(END, str(product[0][0]))
                dane[0].config(state='disabled')

                for i in range(1, 6):
                    dane[i].config(state='normal')
                    dane[i].delete(0, 'end')
                    dane[i].insert(END, str(product[0][i]))
                    if i == 2 or i == 3:
                        dane[i].config(state='disabled')

                update_button.configure(state=NORMAL)
                delete_button.configure(state=NORMAL)

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
                database.commit()
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            messagebox.showinfo("Informacja", "Pomyślnie zmieniono dane produktu")
            # query = f"CALL aktualizacja_liczby_sztuk_produktu({product_id.get()})"
            # print (query)
            # try:
            #     cursor.execute(query)
            #     database.commit()
            # except Exception as e:
            #     messagebox.showerror("Błąd", e)
            #     return

        def delete():
            cursor = database.cursor()
            try:
                cursor.execute(f"DELETE FROM produkt WHERE id_produktu = {product_id.get()}")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            messagebox.showinfo("Informacja", "Pomyślnie usunięto produkt")
            database.commit()

        blank = Label(edit_product)
        blank.grid(row=3, column=1)
        Button(edit_product, text="Pokaż", fg="black", bg="#bfa7a8", width=10, command=show).grid(row=4, column=1)
        blank = Label(edit_product)
        blank.grid(row=5, column=1)

        update_button = Button(edit_product, text="Aktualizuj", fg="black", bg="#bfa7a8", width=10, command=update)
        update_button.grid(row=4, column=2)
        update_button.configure(state=DISABLED)

        delete_button = Button(edit_product, text="Usun", fg="black", bg="#bfa7a8", width=10, command=delete)
        delete_button.grid(row=4, column=3)
        delete_button.configure(state=DISABLED)

        edit_product.mainloop()

    def add_copies():
        add_copy = Toplevel()
        add_copy.title("Dodaj egzemplarz")
        add_copy.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(add_copy)
        blank.grid(row=0, column=1)
        blank = Label(add_copy, width=6)
        blank.grid(row=0, column=0)
        Label(add_copy, text="Podaj dane nowego egzemplarzu").grid(row=1, column=1, columnspan=2)

        columns = ["id_egzemplarza", "id_produktu", "rozmiar", "stan"]
        dane = []

        Label(add_copy, text="Stan").grid(row=10, column=1)

        # combo box
        combo_box = ttk.Combobox(add_copy,
                                 state="readonly",
                                 values=["dobry", "uszkodzony"])
        combo_box.grid(row=10, column=2)
        combo_box.current(0)

        for i in range(3):
            e = tk.Entry(add_copy, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(add_copy, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            dane.append(e)

        dane[2].insert(END, "S/M/L/XL")

        def add():
            cursor = database.cursor()

            if str(dane[1].get()) == '':
                messagebox.showerror("Błąd", "Id_produktu nie może być puste")
                return

            try:
                if dane[2].get() == '':
                    cursor.execute(
                        f"INSERT INTO egzemplarz (id_egzemplarza, id_produktu, stan)"
                        f"VALUES ('{dane[0].get()}','{dane[1].get()}','{combo_box.get()}')")
                else:
                    cursor.execute(
                        f"INSERT INTO egzemplarz (id_egzemplarza, id_produktu, rozmiar, stan)"
                        f"VALUES ('{dane[0].get()}','{dane[1].get()}','{dane[2].get()}','{combo_box.get()}')")

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

    def edit_copy_function():
        edit_copy = Toplevel()
        edit_copy.title("Edytuj/usuń egzemplarz")
        edit_copy.geometry(f"400x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(edit_copy)
        blank.grid(row=0, column=1)
        blank = Label(edit_copy, width=6)
        blank.grid(row=0, column=0)
        Label(edit_copy, text="Podaj identyfikator egzemplarza").grid(row=1, column=1, columnspan=2)
        copy_id = Entry(edit_copy, width=20)
        copy_id.grid(row=2, column=1, columnspan=2)

        Label(edit_copy, text="Stan").grid(row=10, column=1)

        # combo box
        combo_box = ttk.Combobox(edit_copy,
                                 state="readonly",
                                 values=["dobry", "uszkodzony"])
        combo_box.grid(row=10, column=2)
        combo_box.current(0)

        columns = ["id_egzemplarza", "id_produktu", "id_rezerwacji", "rozmiar"]
        dane = []

        for i in range(4):
            e = tk.Entry(edit_copy, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(edit_copy, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')
            dane.append(e)

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM egzemplarz WHERE id_egzemplarza = {copy_id.get()}")
                copy = cursor.fetchall()

                if str(copy[0][0]) == 'None':
                    return
                if str(copy[0][4] == 'dobry'):
                    combo_box.current(1)
                else:
                    combo_box.current(0)

                dane[0].config(state='normal')
                dane[0].delete(0, 'end')
                dane[0].insert(END, str(copy[0][0]))
                dane[0].config(state='disabled')

                dane[1].config(state='normal')
                dane[1].delete(0, 'end')
                dane[1].insert(END, str(copy[0][0]))
                dane[1].config(state='disabled')

                dane[2].config(state='normal')
                dane[2].delete(0, 'end')
                dane[2].insert(END, str(copy[0][0]))
                dane[2].config(state='disabled')

                for i in range(3, 4):
                    dane[i].delete(0, 'end')
                    dane[i].config(state='normal')
                    dane[i].insert(END, str(copy[0][i]))
                delete_cp_button.configure(state=NORMAL)
                update_cp_button.configure(state=NORMAL)

            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")
                return

        def update_cp():
            cursor = database.cursor()
            try:
                cursor.execute(f"UPDATE egzemplarz SET rozmiar = '{dane[3].get()}', stan = '{combo_box.get()}'"
                               f"WHERE id_egzemplarza = {copy_id.get()}")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            messagebox.showinfo("Informacja", "Pomyślnie zmieniono dane produktu")
            database.commit()
            query = f"CALL aktualizacja_liczby_sztuk_produktu({copy_id.get()})"
            print(query)
            try:
                cursor.execute(query)
                database.commit()
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return

        def delete_cp():
            cursor = database.cursor()
            try:
                cursor.execute(f"DELETE FROM egzemplarz WHERE id_egzemplarza = {copy_id.get()}")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            messagebox.showinfo("Informacja", "Pomyślnie usunięto egzemplarz")
            database.commit()

        blank = Label(edit_copy)
        blank.grid(row=3, column=1)
        Button(edit_copy, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=1)
        blank = Label(edit_copy)
        blank.grid(row=5, column=1)

        update_cp_button = Button(edit_copy, text="Aktualizuj", fg="black", bg="#bfa7a8", width=10, command=update_cp)
        update_cp_button.grid(row=4, column=2)
        update_cp_button.configure(state=DISABLED)

        delete_cp_button = Button(edit_copy, text="Usun", fg="black", bg="#bfa7a8", width=10, command=delete_cp)
        delete_cp_button.grid(row=4, column=3)
        delete_cp_button.configure(state=DISABLED)

        edit_copy.mainloop()

    def show_copies_function():
        show_copies = Toplevel()
        show_copies.title("Wyświetl egzemplarzr produktu")
        show_copies.geometry(f"650x250+{top.winfo_x() - 150}+{top.winfo_y() + 50}")

        blank = Label(show_copies)
        blank.grid(row=0, column=1)
        blank = Label(show_copies, width=6)
        blank.grid(row=0, column=0)
        Label(show_copies, text="Podaj identyfikator produktu").grid(row=1, column=2)
        product_id = Entry(show_copies, width=20)
        product_id.grid(row=2, column=2)

        columns = ["id_egzemplarza", "id_produktu", "id_rezerwacji", "rozmiar", "stan"]

        # Table product

        nr_of_rows_product = 5
        cols_product = ["id_egzemplarza", "id_produktu", "id_rezerwacji", "rozmiar", "stan"]
        # stworzyc tabele
        for i in range(nr_of_rows_product):
            e = tk.Entry(show_copies, disabledforeground="black")
            e.grid(row=6, column=0 + i)
            e.insert(END, cols_product[i])
            e.config(state='disabled')

        def show():
            try:
                cursor = database.cursor()
                query = f"SELECT * FROM egzemplarz WHERE id_produktu = {product_id.get()}"
                print(query)
                cursor.execute(query)
                items = cursor.fetchall()

                if str(items[0][0]) == 'None':
                    messagebox.showerror("Error", "Wystąpił błąd.")
                    return

               # res = [str(i or '') for i in items]

                print(items)
                for index in range(len(items)):
                    for i in range(nr_of_rows_product):
                        e = tk.Entry(show_copies, disabledforeground="black")
                        e.grid(row=7 + index, column=0 + i)
                        e.insert(END, items[index][i])
                        e.config(state='disabled')
            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        blank = Label(show_copies)
        blank.grid(row=3, column=1)
        Button(show_copies, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=2)
        blank = Label(show_copies)
        blank.grid(row=5, column=1)

        show_copies.mainloop()

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

    edit_button = tk.Button(top, text="Modyfikuj/usuń dany produkt", width=25, pady=5, fg="black", bg="#bfa7a8",
                            command=edit_function)
    edit_button.pack()

    blank = Label(top)
    blank.pack()

    add_cp_button = tk.Button(top, text="Dodaj egzemplarz", width=25, pady=5, fg="black", bg="#bfa7a8",
                              command=add_copies)
    add_cp_button.pack()

    blank = Label(top)
    blank.pack()

    edit_cp_button = tk.Button(top, text="Modyfikuj/usuń dany egzemplarz", width=25, pady=5, fg="black", bg="#bfa7a8",
                               command=edit_copy_function)
    edit_cp_button.pack()

    blank = Label(top)
    blank.pack()

    show_cp_button = tk.Button(top, text="Wyświetl egzemplarze produktu", width=25, pady=5, fg="black", bg="#bfa7a8",
                               command=show_copies_function)
    show_cp_button.pack()

    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", width=15, pady=5, fg="black", bg="#bfa7a8",
                            command=exit_function)
    exit_button.pack()
    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
