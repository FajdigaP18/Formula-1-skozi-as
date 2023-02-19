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
    
    def __init__(self, ide=None, ime=None, priimek=None):
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
                                         d.priimek = ?)'''
        curr.excecute(poizvedba,(self.ime, self.priimek))
        podatki = curr.fetchall()
        return podatki

    # najboljša uvrstitev
    def najboljse_uvrstitve(self, conn):
        '''Poda podatke najboljše uvrstitve dirkača.'''
        curr = conn.cursor()
        poizvedba = ''''''
        curr.excecute(poizvedba, (self.ime, self.priimek))
        podatki = curr.fetchall()
        return podatki
    
    
    # Koliko uvrstitev na zmagovalni oder
    def zmagovalni_oder(self, conn):
        '''Poda stevilo uvrstitev dirkaca na zmagovalni oder.'''
        curr = conn.cursor()
        poizvedba = ''''''
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
                SELECT eid, team_name, nationality FROM ekipa
                ORDER BY team_name;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa

    @staticmethod
    def pridobi_vse_nemce():
        sql = '''
                SELECT eid, team_name FROM ekipa
                WHERE nationality = 'German'
                ORDER BY team_name;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa
    
    @staticmethod
    def pridobi_vse_angleze():
        sql = '''
                SELECT eid, team_name FROM ekipa
                WHERE nationality = 'British'
                ORDER BY team_name;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa
    
    @staticmethod
    def pridobi_vse_italijane():
        sql = '''
                SELECT eid, team_name FROM ekipa
                WHERE nationality = 'Italian'
                ORDER BY team_name;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa

    @staticmethod
    def poisci_po_imenu(ime, limit=None):
        sql = '''
            SELECT team_name FROM ekipa
            WHERE team_name LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Ekipa.poisci_sql(sql, podatki)

    @staticmethod
    def poisci_po_nacionalnosti(nacija, limit=None):
        sql = '''
            SELECT nationality FROM ekipa
            WHERE nationality LIKE ?'''
        podatki = ['%' + nacija + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Ekipa.poisci_sql(sql, podatki)
