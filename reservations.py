import tkinter as tk
from tkinter import Text
import os
import mysql.connector
from tkinter import *
from tkinter import messagebox

# TODO logicc

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
        reservation_id = Entry(show_reservation, width=20)
        reservation_id.grid(row=2, column=1, columnspan=2)

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
                cursor.execute(f"SELECT * FROM rezerwacja WHERE id_rezerwacji = {reservation_id.get()}")
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
                                       command=show_function)
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
