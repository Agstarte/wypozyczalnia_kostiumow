import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import Text
import os
import mysql.connector



def clients(database, root):
    top = Toplevel()
    top.title("Zarządzanie klientami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    def add_function():
        add_client = Toplevel()
        add_client.title("Dodaj klienta")
        add_client.geometry(f"350x350+{top.winfo_x()}+{top.winfo_y()}")

    def show_function():
        global client_id

        show_client = Toplevel()
        show_client.title("Wyświetl klienta")
        show_client.geometry(f"350x350+{top.winfo_x()}+{top.winfo_y()}")

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
                    e.grid(row=6+i, column=2)
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
        edit_client.geometry(f"350x350+{top.winfo_x()}+{top.winfo_y()}")

    def exit_function():
        top.destroy()

    blank = Label(top)
    blank.pack()
    blank = Label(top)
    blank.pack()
    blank = Label(top, text="Zarządzaj klientami")
    blank.pack()
    blank = Label(top)
    blank.pack()

    clients_button = tk.Button(top, text="         Dodaj klienta         ", padx=15, pady=5, fg="black", bg="#bfa7a8",
                               command=add_function)
    clients_button.pack()

    blank = Label(top)
    blank.pack()

    products_button = tk.Button(top, text="      Wyświetl klienta      ", padx=15, pady=5, fg="black", bg="#bfa7a8",
                                command=show_function)
    products_button.pack()

    blank = Label(top)
    blank.pack()

    reservations_button = tk.Button(top, text="Modyfikuj dane klienta", padx=15, pady=5, fg="black", bg="#bfa7a8",
                                    command=edit_function)
    reservations_button.pack()

    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", padx=30, pady=5, fg="black", bg="#bfa7a8",
                                    command=exit_function)
    exit_button.pack()
