import sqlite3

class Contact_database():
    def __init__(self):
        self.conn = sqlite3.connect('kontaky.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS kontakty(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        jmeno TEXT, 
                        prijmeni TEXT,
                        datum_narozeni TEXT DEFAULT NULL,
                        ulice TEXT,
                        cp INTEGER,
                        mesto TEXT,
                        telefon INTEGER AUTOINCREMENT)''')

        self.c.execute("""CREATE TABLE IF NOT EXISTS skupiny(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nazev TEXT,
                        id_tabulky_kontaktu INTEGER AUTOINCREMENT
                        )""")


    def add_contact(self, jmeno, prijmeni, datum_narozeni, ulice, cp, mesto, telefon):
        self.c.execute("""INSERT INTO kontakty(jmeno, prijmeni, datum_narozeni, ulice, cp, mesto) 
                        VALUES(?, ?, ?, ?, ?, ?, ?)""", (jmeno, prijmeni, datum_narozeni, ulice, cp, mesto))
        query = self.c.execute("""SELECT id FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS seznam_telefonu_{query}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        předpona_země TEXT,
                        telefon INTEGER
                        )""")
        if type(telefon) == list:
            for tel in telefon:
                self.c.execute(f"""INSERT INTO seznam_telefonu_{query}(telefon) VALUES(?)""", (tel))
        else:
            self.c.execute(f"""INSERT INTO seznam_telefonu_{query}(telefon) VALUES(?)""", (telefon))
        self.conn.commit()

    def add_number(self, jmeno, prijmeni, telefon):
        query = self.c.execute("""SELECT id FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        if type(telefon) == list:
            for tel in telefon:
                self.c.execute(f"""INSERT INTO seznam_telefonu_{query}(telefon) VALUES(?)""", (tel))
        else:
            self.c.execute(f"""INSERT INTO seznam_telefonu_{query}(telefon) VALUES(?)""", (telefon))
        self.conn.commit()

    def add_group(self, nazev, kontakty):
        self.c.execute("""INSERT INTO skupiny(nazev) VALUES(?)""", (nazev))
        query = self.c.execute("""SELECT id FROM skupiny WHERE nazev=?""", (nazev))
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS skupiny_kontaktu_{query}(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_kontaktu INTEGER,
                                id_skupiny INTEGER,
                                )""")
        if type(kontakty) == list:
            for kontakt in kontakty:
                self.c.execute("""INSERT INTO skupiny_kontaktu(id_kontaktu, id_skupiny) VALUES(?, ?)""", (kontakt, nazev))
        else:
            self.c.execute("""INSERT INTO skupiny_kontaktu(id_kontaktu, id_skupiny) VALUES(?, ?)""", (kontakty, nazev))
        self.conn.commit()

    def delete_contact(self, jmeno, prijmeni):
        query = self.c.execute("""SELECT id FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        self.c.execute(f"""DROP TABLE seznam_telefonu_{query}""")
        self.c.execute("""DELETE FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        self.conn.commit()

    def delete_number(self, jmeno, prijmeni, telefon):
        query = self.c.execute("""SELECT id FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        self.c.execute(f"""DELETE FROM seznam_telefonu_{query} WHERE telefon=?""", (telefon))
        self.conn.commit()

    def delete_group(self, nazev):
        query = self.c.execute("""SELECT id FROM skupiny WHERE nazev=?""", (nazev))
        self.c.execute(f"""DROP TABLE skupiny_kontaktu_{query}""")
        self.c.execute("""DELETE FROM skupiny WHERE nazev=?""", (nazev))
        self.conn.commit()

    def delete_contact_from_group(self, nazev, jmeno, prijmeni):
        query = self.c.execute("""SELECT id FROM skupiny WHERE nazev=?""", (nazev))
        query2 = self.c.execute("""SELECT id FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        self.c.execute(f"""DELETE FROM skupiny_kontaktu_{query} WHERE id_kontaktu=?""", (query2))
        self.conn.commit()

    def edit_contact(self, jmeno, prijmeni, datum_narozeni, ulice, cp, mesto):
        self.c.execute("""UPDATE kontakty SET datum_narozeni=?, ulice=?, cp=?, mesto=? WHERE jmeno=? AND prijmeni=?""", (datum_narozeni, ulice, cp, mesto, jmeno, prijmeni))
        self.conn.commit()

    def edit_number(self, jmeno, prijmeni, telefon, novy_telefon):
        query = self.c.execute("""SELECT id FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        self.c.execute(f"""UPDATE seznam_telefonu_{query} SET telefon=? WHERE telefon=?""", (novy_telefon, telefon))
        self.conn.commit()

    def edit_group(self, nazev, novy_nazev):
        self.c.execute("""UPDATE skupiny SET nazev=? WHERE nazev=?""", (novy_nazev, nazev))
        self.conn.commit()

    def get_all_contacts(self):
        query = self.c.execute("""SELECT * FROM kontakty""")
        return query.fetchall()

    def get_all_numbers(self):
        query = self.c.execute("""SELECT * FROM seznam_telefonu""")
        return query.fetchall()

    def get_all_groups(self):
        query = self.c.execute("""SELECT * FROM skupiny""")
        return query.fetchall()

    def get_contact(self, jmeno, prijmeni):
        query = self.c.execute("""SELECT * FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        return query.fetchall()

    def get_number(self, jmeno, prijmeni):
        query = self.c.execute("""SELECT * FROM kontakty WHERE jmeno=? AND prijmeni=?""", (jmeno, prijmeni))
        query2 = self.c.execute(f"""SELECT * FROM seznam_telefonu_{query}""")
        return query2.fetchall()

    def get_group(self, nazev):
        query = self.c.execute("""SELECT * FROM skupiny WHERE nazev=?""", (nazev))
        return query.fetchall()

    def get_contact_from_group(self, nazev):
        query = self.c.execute("""SELECT * FROM skupiny WHERE nazev=?""", (nazev))
        query2 = self.c.execute(f"""SELECT * FROM skupiny_kontaktu_{query}""")
        return query2.fetchall()

    def count_members(self, nazev):
        query = self.c.execute("""SELECT id FROM skupiny WHERE nazev=?""", (nazev))
        query2 = self.c.execute(f"""SELECT * FROM skupiny_kontaktu_{query}""")
        return len(query2.fetchall())






