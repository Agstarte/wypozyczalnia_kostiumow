import tkinter as tk
from tkinter import ttk
from tkinter import Text
import os
import mysql.connector
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import codecs

# TODO testy jednostkowe warstwy łącza

is_show_button_clicked = False
products_in_cart = []
products_in_cart_cntr = []
cart_table = []
data_ret_reservation = []
data_modify = []
curr_price = 0
data_add = ''

def reservations(database, root):
    root.withdraw()  # minimalizowanie głównego okna
    top = Toplevel()
    top.title("Zarządzanie rezerwacjami")
    top.geometry(f"350x350+{root.winfo_x()}+{root.winfo_y()}")

    blank = Label(top)

    def modify_function():
        modify_reservation = Toplevel()
        modify_reservation.title("Modyfikuj rezerwację")
        modify_reservation.geometry(f"350x300+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(modify_reservation)
        blank.grid(row=0, column=1)
        blank = Label(modify_reservation, width=6)
        blank.grid(row=0, column=0)
        Label(modify_reservation, text="Podaj identyfikator rezerwacji").grid(row=1, column=1, columnspan=2)
        reservation_id_field = Entry(modify_reservation, width=20)
        reservation_id_field.grid(row=2, column=1, columnspan=2)

        row_count = 6
        rows = ["id_rezerwacji", "id_osoby", "data_poczatku_rezerwacji", "data_konca_rezerwacji", "cena", "status"]
        for i in range(row_count):
            e = tk.Entry(modify_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, rows[i])
            e.config(state='disabled')
            e = tk.Entry(modify_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        def show():
            try:
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM rezerwacja WHERE id_rezerwacji = {reservation_id_field.get()}")
                reservation = cursor.fetchall()

                if str(reservation[0][0]) == 'None':
                    return

                for i in range(row_count):
                    e = tk.Entry(modify_reservation, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(reservation[0][i]))
                    e.config(state='normal')
                    data_modify.append(e)
            except Exception as ex:
                messagebox.showerror("Błąd", ex)
                return

        def modify():
            # check new data
            modified_reservation = []
            for i in range(row_count):
                modified_reservation.append(data_modify[i].get())
                if modified_reservation[i] == '':
                    messagebox.showerror('Błąd', 'Uzupełnij puste pola.')
                    return

            # query new data
            query = f"UPDATE rezerwacja "\
                    f"SET id_rezerwacji = {data_modify[0].get()}, "\
                    f"id_osoby = {data_modify[1].get()}, "\
                    f"data_poczatku_rezerwacji = '{data_modify[2].get()}', "\
                    f"data_konca_rezerwacji = '{data_modify[3].get()}', "\
                    f"cena = {data_modify[4].get()}, " \
                    f"status = '{data_modify[5].get()}' "\
                    f"WHERE id_rezerwacji = {reservation_id_field.get()}"
            print(query)
            try:
                cursor = database.cursor()
                cursor.execute(query)
                database.commit()
            except Exception as ex:
                messagebox.showerror("Błąd", ex)
                return

            messagebox.showinfo("INFO", f"Zapisano zmiany.")

        blank = Label(modify_reservation)
        blank.grid(row=3, column=1)
        Button(modify_reservation, text="Pokaż", fg="black", bg="#bfa7a8", command=show).grid(row=4, column=1,
                                                                                              columnspan=2)
        Button(modify_reservation, text="Modyfikuj", fg="black", bg="#bfa7a8", command=modify).grid(row=12, column=1,
                                                                                              columnspan=2)
        blank = Label(modify_reservation)
        blank.grid(row=5, column=1)

        modify_reservation.mainloop()

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
                reservation = cursor.fetchall()

                if str(reservation[0][0]) == 'None':
                    return

                for i in range(row_count):
                    e = tk.Entry(show_reservation, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(reservation[0][i]))
                    e.config(state='disabled')
            except Exception as ex:
                messagebox.showerror("Błąd", ex)
                return

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
        add_reservation.geometry(f"850x250+{top.winfo_x()-225}+{top.winfo_y() + 50}")
        products_in_cart.clear()
        products_in_cart_cntr.clear()

        # left panel
        blank = Label(add_reservation).grid(row=0, column=1)
        blank = Label(add_reservation, width=6).grid(row=0, column=0)
        Label(add_reservation, text="Podaj dane nowej rezerwacji:").grid(row=1, column=1, columnspan=2)
        blank = Label(add_reservation)
        blank.grid(row=11, column=1)
        Label(add_reservation, text="status").grid(row=12, column=1)
        # combo box
        combo_box = ttk.Combobox(add_reservation,
                                 state="readonly",
                                 values=["w trakcie", "zakonczono"])
        combo_box.grid(row=12, column=2)
        combo_box.current(0)

        # Table reservation
        nr_of_rows_reservation = 5
        rows_reservation = ["id_rezerwacji", "id_osoby", "data_poczatku_rezerwacji(yyyy-mm-dd)", "data_konca_rezerwacji(yyyy-mm-dd)", "cena"]
        data_reservation = []
        for i in range(nr_of_rows_reservation):
            e = tk.Entry(add_reservation, disabledforeground="black")
            e.grid(row=3 + i, column=1)
            e.insert(END, rows_reservation[i])
            e.config(state='disabled')
            e = tk.Entry(add_reservation, disabledforeground="black")
            e.grid(row=3 + i, column=2)
            e.insert(END, '')
            data_reservation.append(e)
        # init data

        today = str(datetime.today().strftime("%Y-%m-%d"))
        data_reservation[1].insert(END, '13')
        data_reservation[2].insert(END, today)
        data_reservation[3].insert(END, today)
        data_reservation[4].insert(END, curr_price)

        # right panel
        Label(add_reservation, text="Koszyk:").grid(row=1, column=4, columnspan=2)
        Label(add_reservation, text="ID produktu:"
              ).grid(row=2, column=3, columnspan=1)

        # id_product Textfield
        id_product_field = Entry(add_reservation, width=20)
        id_product_field.grid(row=2, column=4, columnspan=1)

        # Table product
        no_of_products_in_cart = 0
        nr_of_rows_product = 4
        cols_product = ['id_produktu', 'nazwa', 'cena', 'ilość']
        # stworzyc tabele
        for i in range(nr_of_rows_product):
            e = tk.Entry(add_reservation, disabledforeground="black")
            e.grid(row=3, column=3+i)
            e.insert(END, cols_product[i])
            e.config(state='disabled')

        def add_product():
            global curr_price
            global products_in_cart
            # sprawdzic czy wpisano cokolwiek
            if str(id_product_field.get()) == '':
                messagebox.showerror("Błąd", "Nie podano identyfikatora produktu.")
                return

            # get product data - query for given id_product
            query = f"SELECT id_produktu, nazwa, cena, liczba_dostepnych_sztuk FROM produkt " \
                    f"WHERE id_produktu = {id_product_field.get()}"

            try:
                cursor = database.cursor()
                cursor.execute(query)

                data_product = cursor.fetchall()

                # check if record is legit
                if str(data_product[0][0]) == 'None':
                    return

                # sprawdzenie czy produkt jest juz w koszyku
                is_new = True
                curr_repetition_idx = -1
                for i in range(len(products_in_cart)):
                    if data_product and products_in_cart[i][0][0] == data_product[0][0]:
                        is_new = False
                        # zliczaj wystapienia powtorzonych produktow
                        # dopoki ilosc > amount available
                        products_in_cart_cntr[i] += 1
                        if products_in_cart_cntr[i] > data_product[0][3]:
                            products_in_cart_cntr[i] = data_product[0][3]
                            messagebox.showerror("Błąd", f"Brak dostępnych egzemplarzy produktu: \n{data_product[0][1]}")
                        else:
                            curr_price += data_product[0][2]
                            data_reservation[4].delete(0, 'end')
                            data_reservation[4].insert(END, curr_price)
                        curr_repetition_idx = i
                        break

                if is_new and data_product[0][3] > 0:
                    products_in_cart.append(data_product)
                    products_in_cart_cntr.append(1)
                    curr_price += data_product[0][2]
                    data_reservation[4].delete(0, 'end')
                    data_reservation[4].insert(END, curr_price)
                elif data_product[0][3] <= 0:
                    messagebox.showerror("Błąd", f"Brak dostępnych egzemplarzy produktu: \n{data_product[0][1]}")

            except Exception as ex:
                messagebox.showerror("Błąd", ex)
                return

            # wyswietlenie zawartosci koszyka w tym aktualnie pobranego produktu
            # danych

            # dodanie nowego produktu do tabeli
            last_cart_product = len(products_in_cart) - 1
            for i in range(nr_of_rows_product):
                if i != nr_of_rows_product-1:
                    e = tk.Entry(add_reservation, disabledforeground="black")
                    e.grid(row=4 + last_cart_product, column=3 + i)
                    e.insert(END, products_in_cart[last_cart_product][0][i])
                    e.config(state='disabled')
                    cart_table.append(e)
                elif i == nr_of_rows_product-1:
                    e = tk.Entry(add_reservation, disabledforeground="black")
                    e.grid(row=4 + last_cart_product, column=3 + i)
                    e.insert(END, products_in_cart_cntr[curr_repetition_idx])
                    e.config(state='disabled')
                    cart_table.append(e)

            global data_add
            for i in range(len(products_in_cart)):
                data_add += f"nazwa: {products_in_cart[last_cart_product][0][1]} \
                ilość: {products_in_cart_cntr[last_cart_product]} \n"

        def remove_product():
            print('remove product')

        def update_items(id_rezerwacji):
            cursor = database.cursor()
            # znalezc egzemplarze, ktore sa w koszyku i mają id_produktu = products_in_cart[iteracja][0]0]
            # ustawic im id_rezerwacji = cursor.lastrowid
            # query
            if len(products_in_cart) == 0:
                messagebox.showerror("Błąd", "Wprowadź produkty do dodania.")
                return

            cursor = database.cursor()
            for i in range(len(products_in_cart)):
                curr_id_produktu = products_in_cart[i][0][0]
                nr_of_items = products_in_cart_cntr[i]
                query = f"UPDATE egzemplarz " \
                        f"SET id_rezerwacji = {id_rezerwacji} " \
                        f"WHERE id_produktu = {curr_id_produktu} " \
                        f"AND stan = 'Dobry' " \
                        f"AND id_rezerwacji IS NULL " \
                        f"LIMIT {nr_of_items};"
                print(query)

                # execute queries
                try:
                    cursor.execute(query)
                    database.commit()
                except Exception as ex:
                    messagebox.showerror(f"Błąd it[{str(i)}]", ex)
                    return
                itemscount = cursor.rowcount
                query = f'CALL aktualizacja_liczby_sztuk_produktu({curr_id_produktu});'
                print(query)
                try:
                    cursor.execute(query)
                    database.commit()
                except Exception as ex:
                    messagebox.showerror(f"Błąd it[{str(i)}]", ex)
                    return

        def add():

            # dane produktów do dodania
            # id_produktu = data_product[0].get()

            # dane rezerwacji do dodania

            id_rezerwacji = data_reservation[0].get()
            id_osoby = data_reservation[1].get()
            data_poczatku_rezerwacji = data_reservation[2].get()
            data_konca_rezerwacji = data_reservation[3].get()
            cena = data_reservation[4].get()
            status = combo_box.get()

            # neccessary fields can not be null
            if not id_osoby or not data_poczatku_rezerwacji or not cena or not status or not products_in_cart_cntr:
                messagebox.showerror("Błąd", "Uzupełnij niezbędne pola: "
                                             "\n-id_osoby, \n-data_poczatku_rezerwacji, \n-cena, "
                                             "\n-status\n-ID produktu")
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

            # execute query - add reservation
            try:
                cursor = database.cursor()
                cursor.execute(query)
                database.commit()
            except Exception:
                # if reservation exists - update reservatsion
                query = f'SELECT COUNT(*) ' \
                        f'FROM rezerwacja r ' \
                        f'WHERE r.id_rezerwacji = {id_rezerwacji}'
                cursor = database.cursor()
                cursor.execute(query)
                exists = cursor.fetchall()
                if exists[0][0] == 1:
                    # update egzemplarzy
                    update_items(id_rezerwacji)
                    messagebox.showinfo("Info", f"Zarezerwowano egzemplarze.")
                    after_add_clear()
                return

            # check how many rows were added
            if cursor.rowcount != -1:
                messagebox.showinfo("Informacja", f"Pomyślnie dodano rezerwacje\nid = {cursor.lastrowid}.")
            else:
                messagebox.showerror("Błąd", f"Nie dodano rezerwacji.")

            update_items(cursor.lastrowid)
            after_add_clear()

            # generate agreement
            # get client info
            query = f"SELECT imie, nazwisko, nr_tel, email FROM klient WHERE id_osoby = {data_reservation[1].get()}"
            print(query)
            data_client = []
            try:
                cursor.execute(query)
                data_client = cursor.fetchall()
            except Exception as ex:
                messagebox.showerror("Błąd", ex)
                return

            data = f"---WYPOZYCZALNIA KOSTIUMÓW sp. z.o.o.---\n" \
                   f"Wypożyczający zobowiązuje sie do oddania wypożyczonych produktów w terminie.\n" \
                   f"Imię i nazwisko: {data_client[0][0]} {data_client[0][1]}\n" \
                   f"Nr tel: {data_client[0][2]}\n" \
                   f"E-mail: {data_client[0][3]}\n" \
                   f"Data początku rezerwacji: {data_reservation[2].get()}\n" \
                   f"Data końca rezerwacji: {data_reservation[3].get()}\n" \
                   f"Cena: {data_reservation[4].get()}[PLN]\n" \
                   f"--WYPOŻYCZONE PRODUKTY--\n"

            data += data_add

            # write to file
            # file = codecs.open(f"umowy/{data_client[0][0]} {data_client[0][1]} "
            #             f"- umowa.txt", "w", "utf-8")
            try:
                if not os.path.isdir("./umowy"):
                    os.mkdir("umowy")
                file = codecs.open(f"umowy/{data_client[0][0]} {data_client[0][1]} "
                                   f"- umowa.txt", "w", "utf-8")
                file.write(data)
            except Exception as ex:
                messagebox.showerror("ERROR", ex)
            file.close()

        # cleenup
        def after_add_clear():
            for i in range(len(cart_table)):
                cart_table[i].destroy()
            cart_table.clear()
            products_in_cart_cntr.clear()
            products_in_cart.clear()

        blank = Label(add_reservation)
        blank.grid(row=11, column=1)
        Button(add_reservation, text="Dodaj rezerwację", fg="black", bg="#bfa7a8",
               command=add).grid(row=13, column=1, columnspan=3)
        Button(add_reservation, text="Dodaj egzemplarz", fg="black", bg="#bfa7a8",
               command=add_product).grid(row=2, column=5, columnspan=1)
        # Button(add_reservation, text="Usuń egzemplarz", fg="black", bg="#bfa7a8",
        #        command=remove_product).grid(row=2, column=6, columnspan=1)

        blank = Label(add_reservation)
        blank.grid(row=5, column=1)

        add_reservation.mainloop()

    def ret_function():
        ret_reservation = Toplevel()
        ret_reservation.title("Zwróć rezerwację")
        ret_reservation.geometry(f"350x400+{top.winfo_x()}+{top.winfo_y() + 50}")

        blank = Label(ret_reservation)
        blank.grid(row=0, column=1)
        blank = Label(ret_reservation, width=6)
        blank.grid(row=0, column=0)
        Label(ret_reservation, text="Podaj identyfikator rezerwacji").grid(row=1, column=1, columnspan=2)
        reservation_id_field = Entry(ret_reservation, width=20)
        reservation_id_field.grid(row=2, column=1, columnspan=2)
        Label(ret_reservation, text="Rezerwacja:").grid(row=4, column=1, columnspan=2)

        nr_of_rows_reservation = 6
        rows_reservation = ["id_rezerwacji", "id_osoby", "data_poczatku_rezerwacji", "data_konca_rezerwacji", "cena", "status"]
        for i in range(nr_of_rows_reservation):
            e = tk.Entry(ret_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=1)
            e.insert(END, rows_reservation[i])
            e.config(state='disabled')
            e = tk.Entry(ret_reservation, disabledforeground="black")
            e.grid(row=6 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        blank = Label(ret_reservation)
        blank.grid(row=12, column=1)
        Label(ret_reservation, text="Klient:").grid(row=12, column=1, columnspan=2)

        nr_of_rows_client = 5
        rows_clients = ["id_osoby", "imię", "nazwisko", "numer telefonu", "e-mail"]
        for i in range(nr_of_rows_client):
            e = tk.Entry(ret_reservation, disabledforeground="black")
            e.grid(row=13 + i, column=1)
            e.insert(END, rows_clients[i])
            e.config(state='disabled')
            e = tk.Entry(ret_reservation, disabledforeground="black")
            e.grid(row=13 + i, column=2)
            e.insert(END, '')
            e.config(state='disabled')

        global is_show_button_clicked
        is_show_button_clicked = False

        def show():
            try:
                global is_show_button_clicked
                global data_ret_reservation
                # reservation
                cursor = database.cursor()
                query = f"SELECT * FROM rezerwacja WHERE id_rezerwacji = {reservation_id_field.get()}"
                cursor.execute(query)
                print(query)
                reservation = cursor.fetchall()

                if str(reservation[0][0]) == 'None':
                    return

                data_ret_reservation = []
                for i in range(nr_of_rows_reservation):
                    e = tk.Entry(ret_reservation, disabledforeground="black")
                    e.grid(row=6 + i, column=2)
                    e.insert(END, str(reservation[0][i]))
                    e.config(state='disabled')
                    data_ret_reservation.append(e)

                # client
                id_osoby = data_ret_reservation[1].get()

                # query
                query = f"SELECT * FROM klient WHERE id_osoby = {id_osoby}"
                print(query)
                cursor.execute(query)
                client = cursor.fetchall()

                if str(client[0][0]) == 'None':
                    return

                data_client = []
                for i in range(nr_of_rows_client):
                    e = tk.Entry(ret_reservation, disabledforeground="black")
                    e.grid(row=13 + i, column=2)
                    e.insert(END, str(client[0][i]))
                    e.config(state='disabled')
                    data_client.append(e)

                is_show_button_clicked = True
            except Exception as ex:
                messagebox.showerror("Błąd", ex)
                return

        def ret():
            if not is_show_button_clicked:
                messagebox.showerror("Błąd", "Brak wybranej rezerwacji do zwrotu.")
                return

            # execute queries
            cursor = database.cursor()

            # check if is open
            # query 0
            query = f"SELECT COUNT(*) " \
                    f"FROM rezerwacja " \
                    f"WHERE id_rezerwacji = {data_ret_reservation[0].get()} " \
                    f"AND status = 'w trakcie'"
            print(query)
            cursor.execute(query)
            open = cursor.fetchall()

            if open[0][0] == 0:
                messagebox.showerror("Błąd", f'Nie można wykonać.'
                                             f'\nPodana rezerwacja juz była zakończona.')
                return

            # query 1
            query = f"UPDATE egzemplarz e " \
                    f"SET e.id_rezerwacji = NULL " \
                    f"WHERE e.id_rezerwacji = {data_ret_reservation[0].get()}"
            print(query)
            cursor.execute(query)
            database.commit()

            # query 2
            query = f"UPDATE rezerwacja r " \
                    f"SET r.status = 'zakonczono' " \
                    f"WHERE r.id_rezerwacji = {data_ret_reservation[0].get()}"
            print(query)
            cursor.execute(query)
            database.commit()

            if cursor.rowcount != -1:
                messagebox.showinfo("Info", f'Pomyślnie zwrócono rezerwację\n'
                                            f'id = {data_ret_reservation[0].get()}')
            else:
                messagebox.showinfo("Info", f'Nie zwrócono rezerwacji\n')

        Button(ret_reservation, text="Pokaż", fg="black", bg="#bfa7a8",
               command=show).grid(row=3, column=1, columnspan=2)
        Button(ret_reservation, text="Zwróć", fg="black", bg="#bfa7a8",
               command=ret).grid(row=18, column=1, columnspan=2)
        blank = Label(ret_reservation)
        blank.grid(row=5, column=1)

        ret_reservation.mainloop()

    def exit_function():
        top.destroy()
        root.deiconify()

        # clear cart
        products_in_cart.clear()
        products_in_cart_cntr.clear()

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
                                          command=ret_function)
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
                                        command=modify_function)
    modify_reservation_button.pack()
    blank = Label(top)
    blank.pack()

    exit_button = tk.Button(top, text="Powrót", width=15, pady=5, fg="black", bg="#bfa7a8",
                            command=exit_function)
    exit_button.pack()
    top.protocol("WM_DELETE_WINDOW", exit_function)
    top.mainloop()
