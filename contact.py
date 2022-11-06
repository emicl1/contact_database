"""
autor: Alex Michaud
date: 2019-10-01
decsription: This is a script for work with database and to create a database for contatcs and to add, delete, update and search contacts

"""

import sqlite3
from sqlite3 import Cursor
class Database:
    def __init__(self):
        self.connection = sqlite3.connect('contact.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS contacts ('
                            'contact_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                            'jmeno TEXT, '
                            'prijmeni TEXT,'
                            'datumnarozeni TEXT DEFAULT NULL,'
                            'ulice TEXT,'
                            'cp TEXT,'
                            'mesto TEXT);')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS seznam_telefon ('
                            'id INTEGER PRIMARY KEY,'
                            'contact_id INTEGER,' 
                            'kod_zeme INTEGER,'
                            'telefon INTEGER);')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS skupiny ('
                            'skupiny_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                            'nazev TEXT);')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS seznam_skupin ('
                            'id INTEGER PRIMARY KEY,'
                            'contact_id INTEGER,'
                            'jmeno_kontaktku TEXT,'
                            'skupiny_id INTEGER);')

    def close(self):
        self.connection.close()

    """
    Zde jsou funkce pro přidání kontaktu, skupiny, čísla, kontaktu do skupiny
    """
    def insert_contact(self, jmeno, prijmeni, datumnarozeni, ulice, cp, mesto, kod_zeme, telefon):
        self.cursor.execute('INSERT INTO contacts (jmeno, prijmeni, datumnarozeni, ulice, cp, mesto) VALUES (?, ?, ?, ?, ?, ?)', (jmeno, prijmeni, datumnarozeni, ulice, cp, mesto))
        query = self.cursor.execute('SELECT contact_id FROM contacts WHERE jmeno = ? AND prijmeni = ?',(jmeno, prijmeni))
        a = query.fetchone()
        self.cursor.execute('INSERT INTO seznam_telefon (contact_id, kod_zeme, telefon) VALUES (?, ?, ?)', (str(a[0]),  str(kod_zeme), str(telefon)))
        self.connection.commit()

    def insert_group(self, nazev):
        self.cursor.execute('INSERT INTO skupiny (nazev) VALUES (?)', (nazev))
        self.connection.commit()

    def insert_contact_to_group(self, jmeno_kontaktku, prijmeni_kontaku, nazev):
        query = self.cursor.execute('SELECT skupiny_id FROM skupiny WHERE jmeno = ?',(nazev))
        query2 = self.cursor.execute('SELECT contact_id FROM contacts WHERE jmeno = ? AND prijmeni = ?',(jmeno_kontaktku, prijmeni_kontaku))
        self.cursor.execute('INSERT INTO seznam_skupin (contact_id, skupiny_id, jmeno_kontaktku) VALUES (?, ?, ?)', (query2, query, jmeno_kontaktku))
        self.connection.commit()

    def insert_number(self, jmeno, prijmeni, kod_zeme, telefon):
        query = self.cursor.execute('SELECT contact_id FROM contacts WHERE jmeno = ? AND prijmeni = ?',(jmeno, prijmeni))
        a = query.fetchone()
        self.cursor.execute('INSERT INTO seznam_telefon (kod_zeme, telefon, contact_id) VALUES (?, ?, ?)', (str(kod_zeme), str(telefon), str(a[0])))
        self.connection.commit()

    """
    Zde jsou funkce pro výpis kontaktů, skupin, čísel jednoho kontaktu, kontaktů v skupině, specifického kontaktu
    """

    def print_contacts(self):
        query = self.cursor.execute('SELECT jmeno, prijmeni, datumnarozeni, ulice, cp, mesto FROM contacts')
        for row in query:
            print(row)

    def print_groups(self):
        query = self.cursor.execute('SELECT nazev FROM skupiny')
        for row in query:
            print(row)

    def print_numbers_of_one_person(self, jmeno, prijmeni):

        contact_id = self.cursor.execute('SELECT contact_id FROM contacts WHERE jmeno = ? AND prijmeni = ?',(jmeno, prijmeni))
        contact_id = contact_id.fetchone()
        query = self.cursor.execute('SELECT telefon FROM seznam_telefon WHERE contact_id = ?', (str(contact_id[0])))
        seznam = query.fetchall()
        for row in seznam:
            print(row)

    def print_contacts_in_group(self, nazev):
        query = self.cursor.execute('SELECT jmeno_kontaktku FROM seznam_skupin WHERE skupiny_id = (SELECT skupiny_id FROM skupiny WHERE nazev = ?)',(nazev))
        for row in query:
            print(row)

    def print_one_person(self, prijmeni, jmeno):
        if jmeno == "":
            query = self.cursor.execute(
                'SELECT jmeno, prijmeni, datumnarozeni, ulice, cp, mesto FROM contacts WHERE id = (SELECT contact_id FROM contacts WHERE prijmeni = ?)',
                (prijmeni))

        elif prijmeni == "":
            query = self.cursor.execute(
                'SELECT jmeno, prijmeni, datumnarozeni, ulice, cp, mesto FROM contacts WHERE id = (SELECT contact_id FROM contacts WHERE jmeno = ? )',
                (jmeno))
        else:
            query = self.cursor.execute(
                'SELECT jmeno, prijmeni, datumnarozeni, ulice, cp, mesto FROM contacts WHERE id = (SELECT contact_id FROM contacts WHERE jmeno = ? AND prijmeni = ?)',
                (jmeno, prijmeni))
        for row in query:
            print(row)

    """
    Zde jsou funkce pro smazání kontaktu a telefoních čísel u kontaktku  """


    def delete_contact(self, jmeno, prijmeni):
        query = self.cursor.execute('DELETE FROM contacts WHERE jmeno = ? AND prijmeni = ?', (jmeno, prijmeni))
        search = self.cursor.execute('SELECT contact_id FROM contacts WHERE jmeno = ? AND prijmeni = ?', (jmeno, prijmeni))
        search = search.fetchone()
        query2 = self.cursor.execute('DELETE FROM seznam_telefon WHERE conract_id = ?', (str(search[0]),))
        query3 = self.cursor.execute('DELETE FROM seznam_skupin WHERE contact_id = ?', (str(search[0]),))
        self.connection.commit()

    def delete_number(self, telefon):
        query = self.cursor.execute('DELETE FROM seznam_telefon WHERE  telefon = ?', (telefon, ))
        self.connection.commit()


    """ 
    Zde jsou funkce pro editaci kontaktu a telefoních čísel u kontaktku """

    def edit_contact(self,old_jmeno, old_prijmeni, jmeno, prijmeni, datumnarozeni, ulice, cp, mesto):
        query = self.cursor.execute('UPDATE contacts SET jmeno = ?, prijmeni = ?, datumnarozeni = ?, ulice = ?, cp = ?, mesto = ? WHERE jmeno = ? AND prijmeni = ?', (jmeno, prijmeni, datumnarozeni, ulice, cp, mesto, old_jmeno, old_prijmeni))
        self.connection.commit()

    def edit_number(self, telefon, kod_zeme, new_telefon):
        query = self.cursor.execute('UPDATE seznam_telefon SET kod_zeme = ?, telefon = ? WHERE telefon = ?', (kod_zeme, new_telefon, telefon))
        self.connection.commit()


    """
    Zde jsou funkce pro výpis kontaktů, specifického kontaktu a nalezení kontatku podle čísla"""

    def find_contact_by_number(self, telefon):
        query = self.cursor.execute("SELECT contact_id FROM seznam_telefon WHERE telefon = ? ", (telefon, ))
        query = query.fetchone()
        query = self.cursor.execute('SELECT jmeno, prijmeni FROM contacts WHERE contact_id = ?', (str(query[0]),))
        query = query.fetchall()
        for row in query:
            print(row)

    def find_contact_by_name(self, jmeno, prijmeni):
        if jmeno == "":
            query = self.cursor.execute('SELECT jmeno, prijmeni FROM contacts WHERE prijmeni = ?', (prijmeni, ))
        elif prijmeni == "":
            query = self.cursor.execute('SELECT jmeno, prijmeni FROM contacts WHERE jmeno = ?', (jmeno, ))
        else:
            query = self.cursor.execute('SELECT jmeno, prijmeni FROM contacts WHERE jmeno = ? AND prijmeni = ?)', (jmeno, prijmeni))
        for row in query:
            print(row)

    def print_all_contacts(self):
        query = self.cursor.execute('SELECT jmeno, prijmeni FROM contacts')
        for row in query:
            print(row)

    def print_all_numbers(self):
        query = self.cursor.execute('SELECT * FROM seznam_telefon')
        for row in query:
            print(row)




if __name__ == "__main__":
    options = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c"]
    db = Database()
    db.print_all_numbers()
    while True:
        print("Zadejte jednu z následujících možností:")
        print("a) Přidat kontakt")
        print("s) editovat kontakt")
        print("d) smazání kontaktu")
        print("f) Vyhledat kontakt podle jména")
        print("g) Přidání telefonního čísla")
        print("h) editování telefoního čísla")
        print("j) smazání telefoního čísla")
        print("k) vyhledání kontaktu podle telefoního čísla")

        print("l) Ukončení programu")
        print("z) čísla jedné osoby")
        print("x) všechny kontakty")
        print("c) všechna čísla")
        option = input("Zadejte volbu: ")
        if option not in options:
            print("Zadal jste špatnou volbu, zkuste to znovu")
        else:
            if option == "a":
                jmeno = input("Zadejte jméno: ")
                prijmeni = input("Zadejte příjmení: ")
                datumnarozeni = input("Zadejte datum narození: ")
                ulice = input("Zadejte ulici: ")
                cp = input("Zadejte číslo popisné: ")
                mesto = input("Zadejte město: ")
                kod_zeme = input("Zadejte kód země: ")
                telefon = input("Zadejte telefon: ")
                db = Database()
                db.insert_contact(jmeno, prijmeni, datumnarozeni, ulice, cp, mesto, kod_zeme, telefon)
                db.close()
            elif option == "s":
                old_jmeno = input("Zadejte staré jméno: ")
                old_prijmeni = input("Zadejte staré příjmení: ")
                jmeno = input("Zadejte nové jméno: ")
                prijmeni = input("Zadejte nové příjmení: ")
                datumnarozeni = input("Zadejte datum narození: ")
                ulice = input("Zadejte ulici: ")
                cp = input("Zadejte číslo popisné: ")
                mesto = input("Zadejte město: ")
                db = Database()
                db.edit_contact(old_jmeno, old_prijmeni, jmeno, prijmeni, datumnarozeni, ulice, cp, mesto)
                db.close()
            elif option == "d":
                jmeno = input("Zadejte jméno: ")
                prijmeni = input("Zadejte příjmení: ")
                db = Database()
                db.delete_contact(jmeno, prijmeni)
                db.close()
            elif option == "f":
                print("Zadejte jméno a příjmení kontaktu, kterého chcete najít, nebo nechte pole prázdné")
                jmeno = input("Zadejte jméno: ")
                prijmeni = input("Zadejte příjmení: ")
                db = Database()
                db.find_contact_by_name(jmeno, prijmeni)
                db.close()
            elif option == "g":
                jmeno = input("Zadejte jméno: ")
                prijmeni = input("Zadejte příjmení: ")
                telefon = input("Zadejte telefon: ")
                kod_zeme = input("Zadejte kód země: ")
                db = Database()
                db.insert_number(jmeno, prijmeni, telefon, kod_zeme)
                db.close()

            elif option == "h":
                telefon = input("Zadejte telefon: ")
                kod_zeme = input("Zadejte kód země: ")
                new_telefon = input("Zadejte nový telefon: ")
                db = Database()
                db.edit_number(telefon, kod_zeme, new_telefon)
                db.close()

            elif option == "j":
                telefon = input("Zadejte telefon: ")
                db = Database()
                db.delete_number(telefon)
                db.close()

            elif option == "k":
                telefon = input("Zadejte telefon: ")
                db = Database()
                db.find_contact_by_number(telefon)
                db.close()

            elif option == "l":
                break

            elif option == "z":
                jmeno = input("Zadejte jméno: ")
                prijmeni = input("Zadejte příjmení: ")
                db = Database()
                db.print_numbers_of_one_person(jmeno, prijmeni)
                db.close()

            elif option == "x":
                db = Database()
                db.print_all_contacts()
                db.close()

            elif option == "c":
                db = Database()
                db.print_all_numbers()
                db.close()























