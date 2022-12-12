
def ustvari_tabele(conn):
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS
            uporabnik(
                uid INTEGER PRIMARY KEY,
                username TEXT,
                name TEXT
            )
            """
        )

folk = [
    ("1bc1@gmail.com", "ime1"),
    ("1bcdef@gmail.com", "ime2"),
    ("dogola@gmail.com", "ime3")
]


def napolni_nujne_podatke(conn):
    with conn:
        for (email, name) in folk:
                (f"""
                INSERT INTO uporabnik (email, name)
                VALUES (?, ?)
                """, (email, name))

def pripravi_vse(conn):
    ustvari_tabele(conn)
    napolni_nujne_podatke(conn)