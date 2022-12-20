
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
        conn.execute("""
        INSERT INTO uporabnik 
        (username, name) VALUES
        ("email@email.com", "Neko ime")
        """)

def pripravi_vse(conn):
    ustvari_tabele(conn)
    napolni_nujne_podatke(conn)