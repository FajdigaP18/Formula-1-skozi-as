import sqlite3

conn = sqlite3.connect("f1database.sqlite3")


# moram se dokoncati povezave med starimi in novimi ekipami
# vir : https://wtf1.com/post/these-are-all-the-f1-team-changes-in-the-last-decade/
# vir : https://www.topgear.com/car-news/formula-one/formula-one-here-are-family-trees-every-team
stare_v_novo = {'Tyrrell':'Mercedes', 'BAR':'Mercedes', 'Honda':'Mercedes', 'Brawn':'Mercedes',
                'Jaguar':'Red Bull', 'Stewart':'Red Bull',
                'Minardi':'AlphaTauri','Toro Rosso':'AlphaTauri',
                'Toleman' : 'Alpine','Benetton':'Alpine', 'Renault':'Alpine', 'Lotus':'Alpine', 'Lotus F1':'Alpine',
                'Jordan' : 'Aston Martin', 'Spyker' : 'Aston Martin', 'Spyker MF1' : 'Aston Martin', 'Force India' : 'Aston Martin', 'Racing Point' : 'Aston Martin',
                'Sauber' : 'Alfa Romeo', #LDS-Alfa Romeo,March-Alfa Romeo, Caterham
                'Marussia': 'Haas F1 Team', 'Manor Marussia' : 'Haas F1 Team', 'Virgin' 'Haas F1 Team'
                'Wolf' : 'Williams'}


# TODO: Tukaj ustvarimo bazo če je še ni

class Model:

    def dobi_vse_uporabnike(self):
        with conn:
            cur = conn.execute("""
            SELECT * FROM uporabnik
            """)

            return cur.fetchall()
        

class Dirkac:
    
    def __init__(self, ide = None, ime = None, priimek = None):
        self.id = ide
        self.ime = ime
        self.priimek = priimek
        
    def __str__(self):
        return f'{self.ime} {self.priimek}'
    
    # vse ekipe, za katere je dirkal 
    # NISM SE PREVERILA CE DELUJE !!!!!!!!!!!
    def vse_ekipe(self, conn):
        '''Poda tabelo vseh ekip v katerih je dirkal dirkač.'''
        curr = conn.cursor()
        poizvedba = '''SELECT DISTINCT ime
                         FROM ekipa
                              INNER JOIN
                              rezultati ON ekipa.eid = rezultati.cid
                              INNER JOIN
                              dirkaci ON dirkaci.did = rezultati.did
                        WHERE dirkaci.did IN (
                                  SELECT d.did
                                    FROM dirkaci d
                                   WHERE d.ime = ? AND 
                                         d.priimek = ?);'''
        curr.excecute(poizvedba,(self.ime, self.priimek))
        podatki = curr.fetchall()
        return podatki

    # najboljša uvrstitev
    def najboljsa_uvrstitev(self, conn):
        '''Poda podatke najboljše uvrstitve dirkača.'''
        curr = conn.cursor()
        poizvedba = '''SELECT dirkaci.ime,
                              dirkaci.priimek,
                              rezultati.pozicija,
                              ekipa.ime,
                              dirkalisca.ime,
                              dirka.datum
                         FROM dirkaci
                              INNER JOIN
                              rezultati ON dirkaci.did = rezultati.did
                              INNER JOIN
                              ekipa ON ekipa.eid = rezultati.cid
                              INNER JOIN
                              dirka ON dirka.raceid = rezultati.rid
                              INNER JOIN
                              dirkalisca ON dirka.dirkalisce = dirkalisca.cid
                        WHERE dirkaci.ime = ? AND 
                              dirkaci.priimek = ? AND 
                              rezultati.pozicija = (
                                                       SELECT min(rezultati.pozicija) 
                                                         FROM rezultati
                                                        GROUP BY rezultati.did
                                                       HAVING rezultati.did = (
                                                                                  SELECT dirkaci.did
                                                                                    FROM dirkaci
                                                                                   WHERE dirkaci.ime = ? AND 
                                                                                         dirkaci.priimek = ?
                                                                              )
                                                   )
                        ORDER BY dirka.datum DESC;'''
        curr.excecute(poizvedba, (self.ime, self.priimek, self.ime, self.priimek))
        podatki = curr.fetchall()
        return podatki
    
    
    # Koliko uvrstitev na zmagovalni oder
    def zmagovalni_oder(self, conn):
        '''Poda stevilo uvrstitev dirkaca na zmagovalni oder.'''
        curr = conn.cursor()
        poizvedba = '''SELECT dirkaci.ime,
                               dirkaci.priimek,
                               count( * ) AS oder_za_zmagovalce
                          FROM dirkaci
                               INNER JOIN
                               rezultati ON dirkaci.did = rezultati.did
                         WHERE rezultati.pozicija < 4
                         GROUP BY dirkaci.did
                        HAVING dirkaci.ime = ? AND 
                               dirkaci.priimek = '?'''
        curr.execute(poizvedba, (self.ime, self.priimek))
        podatki = curr.fetchall()
        return podatki
    
class Ekipa:

    def __init__(self, eid=None, ime=None, nationality=None):
        self.eid = eid
        self.ime = ime
        self.nationality = nationality

    def __str__(self) -> str:
        return str(self.ime)
    
    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Ekipa(*poizvedba)


    @staticmethod
    def pridobi_vse_ekipe():
        sql = '''
                SELECT eid, ime, nationality FROM ekipa
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa

    @staticmethod
    def poisci_po_imenu(ime, limit=None):
        sql = '''
            SELECT ime FROM ekipa
            WHERE ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Ekipa.poisci_sql(sql, podatki)

    @staticmethod
    def poisci_po_nacionalnosti(nacija, limit=None):
        sql = '''
            SELECT drzava FROM ekipa
            WHERE drzava LIKE ?'''
        podatki = ['%' + nacija + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Ekipa.poisci_sql(sql, podatki)


