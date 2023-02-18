import sqlite3
import baza

conn = sqlite3.connect("f1database.sqlite3")

baza.pripravi_vse(conn)

# moram se dokoncati povezave med starimi in novimi ekipami
# vir : https://wtf1.com/post/these-are-all-the-f1-team-changes-in-the-last-decade/
# vir : https://www.topgear.com/car-news/formula-one/formula-one-here-are-family-trees-every-team
# stare_v_novo = {?: ['Mercedes', 'Tyrrell', 'BAR', 'Honda', 'Brawn'],
#                 ?: ['Red Bull','Jaguar', 'Stewart'],
#                 ?: ['AlphaTauri','Minardi ','Toro Rosso'],
#                 ?: ['Alpine', 'Toleman','Benetton', 'Renault', 'Lotus', 'Lotus F1', '...'],
#                 ?: ['Aston Martin', 'Jordan', 'MF1', 'Spyker', 'Spyker MF1', 'Force India', 'Racing Point'],
#                 ?: ['Alfa Romeo', 'Sauber'], #LDS-Alfa Romeo,March-Alfa Romeo, Caterham
#                 ?: ['Haas F1 Team','Marussia', 'Manor Marussia', 'Virgin'];
#                 ?: ['Williams','Wolf'],
#                 }
# TODO: Tukaj ustvarimo bazo če je še ni

class Model:

    def dobi_vse_uporabnike(self):
        with conn:
            cur = conn.execute("""
            SELECT * FROM uporabnik
            """)

            return cur.fetchall()

class Dirkac:
    
    def __init__(self, ide, ime, priimek):
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
        curr.excecute(poizvedba,[self.ime, self.priimek])
        podatki = curr.fetchall()
        return podatki

    # def najboljse_uvrstitve(self, conn):
    
    # Koliko uvrstitev na zmagovalni oder
    
    