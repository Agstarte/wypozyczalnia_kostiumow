import tkinter as tk
from tkinter import ttk
from tkinter import Text
import os
import mysql.connector
from tkinter import *
from tkinter import messagebox

# TODO treści komunikatów błędów i dodawanie rezerwacji

def reservations(database, root):
    root.withdraw()  # minimalizowanie głównego okna
    top = Toplevel()
    top.title("Zarządzanie rezerwacjami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    blank = Label(top)

    def show_function():
        show_reservation = Toplevel()
        show_reservation.title("Wyświetl rezerwację")
        show_reservation.geometry(f"350x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(show_reservation)
        blank.grid(row=0, column=1)
        blank = Label(show_reservation, width=6)
        blank.grid(row=0, column=0)
        Label(show_reservation, text="Podaj identyfikator rezerwacji").grid(row=1, column=1, columnspan=2)
        reservation_id_field = Entry(show_reservation, width=20)
        reservation_id_field.grid(row=2, column=1, columnspan=2)

        row_count = 6
        rows = ["id_rezerwacji", "id_osoby", "data_poczatku_rezerwacji", "data_konca_rezerwacji", "cena", "status"]
        for i in range(row_count):
            e = tk.Entry(show_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, rows[i])
            e.config(state='disabled')
            e = tk.Entry(show_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM rezerwacja WHERE id_rezerwacji = {reservation_id_field.get()}")
                client = cursor.fetchall()

                if str(client[0][0]) == 'None':
                    return

                for i in range(row_count):
                    e = tk.Entry(show_reservation, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(client[0][i]))
                    e.config(state='disabled')
            except:
                messagebox.showerror("Błąd", "Wprowadzono niepoprawny identyfikator.")

        blank = Label(show_reservation)
        blank.grid(row=3, column=1)
        Button(show_reservation, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=1,
                                                                                            columnspan=2)
        blank = Label(show_reservation)
        blank.grid(row=5, column=1)

        show_reservation.mainloop()

    def add_function():
        add_reservation = Toplevel()
        add_reservation.title("Dodaj rezerwację")
        add_reservation.geometry(f"450x250+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(add_reservation)
        blank.grid(row=0, column=1)
        blank = Label(add_reservation, width=6)
        blank.grid(row=0, column=0)
        Label(add_reservation, text="Podaj dane nowej rezerwacji").grid(row=1, column=1, columnspan=2)

        Label(add_reservation, text="status").grid(row=12, column=1)
        # combo box
        combo_box = ttk.Combobox(add_reservation, values=
                                [
                                    "w trakcie",
                                    "zakonczono"
                                ])
        combo_box.grid(row=12, column=2)
        combo_box.current(0)

        # Table
        row_count = 5
        rows = ["id_rezerwacji", "id_osoby", "data_poczatku_rezerwacji(yyyy-mm-dd)", "data_konca_rezerwacji(yyyy-mm-dd)", "cena"]
        dane = []
        for i in range(row_count):
            e = tk.Entry(add_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, rows[i])
            e.config(state='disabled')
            e = tk.Entry(add_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            dane.append(e)

        def add():
            cursor = database.cursor()
            # cursor.execute(f"SELECT * FROM klient WHERE id_osoby = {client_id.get()}")
            # client = cursor.fetchall()

            # textfield valułes

            id_rezerwacji = dane[0].get()
            id_osoby = dane[1].get()
            data_poczatku_rezerwacji = dane[2].get()
            data_konca_rezerwacji = dane[3].get()
            cena = dane[4].get()
            status = combo_box.get()

            # data for testing purposes
            # id_rezerwacji = 7
            # id_osoby = 13
            # data_poczatku_rezerwacji = '2020-10-10'
            # data_konca_rezerwacji = '2020-10-10'
            # cena = 56.42
            # status = 'w trakcie'

            # neccessary fields can not be null
            if not id_osoby or not data_poczatku_rezerwacji or not cena or not status:
                messagebox.showerror("Błąd", "Uzupełnij niezbędne pola(id_osoby, data_poczatku_rezerwacji, cena, status)")
                return

            # prepare query
            if str(id_rezerwacji) == '':
                query = f'INSERT INTO rezerwacja(`id_osoby`, ' \
                        f'`data_poczatku_rezerwacji`, `data_konca_rezerwacji`, ' \
                        f'`cena`, `status`)' \
                        f"VALUES ({id_osoby}," \
                        f"'{data_poczatku_rezerwacji}','{data_konca_rezerwacji}'," \
                        f"{cena}, '{status}')"
            else:
                query = f'INSERT INTO rezerwacja(`id_rezerwacji`, `id_osoby`, ' \
                        f'`data_poczatku_rezerwacji`, `data_konca_rezerwacji`, ' \
                        f'`cena`, `status`)' \
                        f"VALUES ({id_rezerwacji},{id_osoby}," \
                        f"'{data_poczatku_rezerwacji}','{data_konca_rezerwacji}'," \
                        f"{cena}, '{status}')"

            print(query)

            # execute query
            try:
                cursor.execute(query)
            except Exception as ex:
                messagebox.showerror("Błąd podczas wykonywania zapytania.")

            try:
                database.commit()
            except Exception as ex:
                messagebox.showerror("Błąd podczas dodawania do bazy.")
                return

            # check how many rows were added
            if cursor.rowcount != -1:
                messagebox.showinfo("Informacja", f"Pomyślnie dodano {cursor.rowcount} rezerwacje.")
            else:
                messagebox.showerror("Błąd", f"Nie dodano rezerwacji.")


        blank = Label(add_reservation)
        blank.grid(row=11, column=1)
        Button(add_reservation, text="Dodaj", fg="black", bg="#bfa7a8", command=add).grid(row=13, column=1, columnspan=3)
        blank = Label(add_reservation)
        blank.grid(row=5, column=1)

        add_reservation.mainloop()


    def exit_function():
        top.destroy()
        root.deiconify()

    # layout
    # label
    blank = Label(top)
    blank.pack()
    blank = Label(top)
    blank.pack()
    blank = Label(top, text="Zarządzaj rezerwacjami")
    blank.pack()
    blank = Label(top)
    blank.pack()

    # dodaj btn
    add_reservation_button = tk.Button(top, text="Dodaj rezerwacje", width=25, pady=5, fg="black", bg="#bfa7a8",
                                       command=add_function)
    add_reservation_button.pack()
    blank = Label(top)
    blank.pack()

    # zwroc btn
    return_reservation_button = tk.Button(top, text="Zwrot rezerwacji", width=25, pady=5, fg="black", bg="#bfa7a8",
                                          command=show_function)
    return_reservation_button.pack()
    blank = Label(top)
    blank.pack()

    # wyswietl btn
    show_reservation_button = tk.Button(top, text="Wyświetl rezerwacje", width=25, pady=5, fg="black", bg="#bfa7a8",
                                        command=show_function)
    show_reservation_button.pack()
    blank = Label(top)
    blank.pack()

    # modyfikuj btn
    modify_reservation_button = tk.Button(top, text="Modyfikuj rezerwacje", width=25, pady=5, fg="black", bg="#bfa7a8",
                                        command=show_function)
    modify_reservation_button.pack()
    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", width=15, pady=5, fg="black", bg="#bfa7a8",
                            command=exit_function)
    exit_button.pack()
    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
