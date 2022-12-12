import sqlite3
import baza

conn = sqlite3.connect("f1database.sqlite3")

baza.pripravi_vse(conn)

# TODO: Tukaj ustvarimo bazo če je še ni

class Model:

    def dobi_vse_uporabnike(self):
        with conn:
            cur = conn.execute("""
            SELECT * FROM uporabnik
            """)

            return cur.fetchall()