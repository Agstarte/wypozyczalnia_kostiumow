import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import Text
import os
import mysql.connector


def clients(database, root):
    root.withdraw()     # minimalizowanie głównego okna
    top = Toplevel()
    top.title("Zarządzanie klientami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    def add_function():
        add_client = Toplevel()
        add_client.title("Dodaj klienta")
        add_client.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(add_client)
        blank.grid(row=0, column=1)
        blank = Label(add_client, width=6)
        blank.grid(row=0, column=0)
        Label(add_client, text="Podaj dane nowego klienta").grid(row=1, column=1, columnspan=2)

        columns = ["id_osoby", "imię", "nazwisko", "numer telefonu", "e-mail"]
        dane = []
        for i in range(5):
            e = tk.Entry(add_client, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(add_client, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            dane.append(e)

        def add():
            cursor = database.cursor()
            # cursor.execute(f"SELECT * FROM klient WHERE id_osoby = {client_id.get()}")
            # client = cursor.fetchall()

            if str(dane[1].get()) == '' or str(dane[2].get()) == '' or str(dane[3].get()) == '':
                messagebox.showerror("Błąd", "Imię, Nazwisko i numer telefonu nie mogą być puste!")
                return
            try:
                if str(dane[0].get()) != '' and str(dane[4].get()) != '':
                    cursor.execute(f"INSERT INTO klient (id_osoby, imie, nazwisko, nr_tel, email)"
                                   f"VALUES ({dane[0].get()},'{dane[1].get()}','{dane[2].get()}','{dane[3].get()}','{dane[4].get()}')")
                elif str(dane[0].get()) != '' and str(dane[4].get()) == '':
                    cursor.execute(f"INSERT INTO klient (id_osoby, imie, nazwisko, nr_tel)"
                                   f"VALUES ({dane[0].get()},'{dane[1].get()}','{dane[2].get()}','{dane[3].get()}')")
                elif str(dane[0].get()) == '' and str(dane[4].get()) != '':
                    cursor.execute(f"INSERT INTO klient (imie, nazwisko, nr_tel, email)"
                                   f"VALUES ('{dane[1].get()}','{dane[2].get()}','{dane[3].get()}','{dane[4].get()}')")
                else:
                    cursor.execute(f"INSERT INTO klient (imie, nazwisko, nr_tel)"
                                   f"VALUES ('{dane[1].get()}','{dane[2].get()}','{dane[3].get()}')")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            database.commit()
            if str(dane[0].get()) == '':
                messagebox.showinfo("Informacja", f"Pomyślnie dodano klienta o id: {cursor.lastrowid}")
            else:
                messagebox.showinfo("Informacja", f"Pomyślnie dodano klienta o id: {str(dane[0].get())}")


        blank = Label(add_client)
        blank.grid(row=11, column=1)
        Button(add_client, text="Dodaj", fg="black", bg="#bfa7a8", command=add).grid(row=12, column=1, columnspan=2)
        blank = Label(add_client)
        blank.grid(row=5, column=1)

        add_client.mainloop()

    def show_function():
        show_client = Toplevel()
        show_client.title("Wyświetl klienta")
        show_client.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(show_client)
        blank.grid(row=0, column=1)
        blank = Label(show_client, width=6)
        blank.grid(row=0, column=0)
        Label(show_client, text="Podaj identyfikator klienta").grid(row=1, column=1, columnspan=2)
        client_id = Entry(show_client, width=20)
        client_id.grid(row=2, column=1, columnspan=2)

        columns = ["id_osoby", "imię", "nazwisko", "numer telefonu", "e-mail"]
        for i in range(5):
            e = tk.Entry(show_client, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(show_client, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM klient WHERE id_osoby = {client_id.get()}")
                client = cursor.fetchall()

                if str(client[0][0]) == 'None':
                    return

                for i in range(5):
                    e = tk.Entry(show_client, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(client[0][i]))
                    e.config(state='disabled')
            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        blank = Label(show_client)
        blank.grid(row=3, column=1)
        Button(show_client, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=1, columnspan=2)
        blank = Label(show_client)
        blank.grid(row=5, column=1)

        show_client.mainloop()

    def edit_function():
        edit_client = Toplevel()
        edit_client.title("Modyfikuj dane klienta")
        edit_client.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(edit_client)
        blank.grid(row=0, column=1)
        blank = Label(edit_client, width=6)
        blank.grid(row=0, column=0)
        Label(edit_client, text="Podaj identyfikator klienta").grid(row=1, column=1, columnspan=2)
        client_id = Entry(edit_client, width=20)
        client_id.grid(row=2, column=1, columnspan=2)

        dane = []
        columns = ["id_osoby", "imię", "nazwisko", "numer telefonu", "e-mail"]
        for i in range(5):
            e = tk.Entry(edit_client, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, columns[i])
            e.config(state='disabled')
            e = tk.Entry(edit_client, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')
            dane.append(e)

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM klient WHERE id_osoby = {client_id.get()}")
                client = cursor.fetchall()

                if str(client[0][0]) == 'None':
                    return
                for i in range(5):
                    dane[i].config(state='normal')
                    dane[i].insert(END, str(client[0][i]))
                update_button.configure(state=NORMAL)
            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        def update():
            cursor = database.cursor()
            # cursor.execute(f"SELECT * FROM klient WHERE id_osoby = {client_id.get()}")
            # client = cursor.fetchall()
            if str(dane[0].get()) == '' or str(dane[1].get()) == '' or str(dane[2].get()) == '' or str(
                    dane[3].get()) == '':
                messagebox.showerror("Błąd", "Identyfikator, Imię, Nazwisko i numer telefonu nie mogą być puste!")
                return
            try:
                cursor.execute(f"UPDATE klient SET id_osoby = {dane[0].get()}, imie = '{dane[1].get()}',"
                               f" nazwisko = '{dane[2].get()}', nr_tel = '{dane[3].get()}', email = '{dane[4].get()}' "
                               f"WHERE id_osoby = {client_id.get()}")
            except Exception as e:
                messagebox.showerror("Błąd", e)
                return
            messagebox.showinfo("Informacja", "Pomyślnie zmieniono dane klienta")
            database.commit()

        blank = Label(edit_client)
        blank.grid(row=3, column=1)
        Button(edit_client, text="Pokaż", fg="black", bg="#bfa7a8", width=10, command=show).grid(row=4, column=1)
        blank = Label(edit_client)
        blank.grid(row=5, column=1)

        update_button = Button(edit_client, text="Aktualizuj", fg="black", bg="#bfa7a8", width=10, command=update)
        update_button.grid(row=4, column=2)
        update_button.configure(state=DISABLED)

        edit_client.mainloop()

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

    clients_button = tk.Button(top, text="Dodaj klienta", width=25, pady=5, fg="black", bg="#bfa7a8",
                               command=add_function)
    clients_button.pack()

    blank = Label(top)
    blank.pack()

    products_button = tk.Button(top, text="Wyświetl klienta", width=25, pady=5, fg="black", bg="#bfa7a8",
                                command=show_function)
    products_button.pack()

    blank = Label(top)
    blank.pack()

    reservations_button = tk.Button(top, text="Modyfikuj dane klienta", width=25, pady=5, fg="black", bg="#bfa7a8",
                                    command=edit_function)
    reservations_button.pack()

    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", width=15, pady=5, fg="black", bg="#bfa7a8",
                            command=exit_function)
    exit_button.pack()
    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
