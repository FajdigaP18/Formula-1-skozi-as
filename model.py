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


      
class Dirkac:
    
    def __init__(self, ide=None, ime=None, priimek=None, drzava = None, rojstvo = None):
        self.id = ide
        self.ime = ime
        self.priimek = priimek
        self.drzava = drzava
        self.rojstvo = rojstvo
        
    def __str__(self):
        return f'{self.ime} {self.priimek}'


    @staticmethod
    def dobi_dirkaca(did):
        with conn:
            cursor = conn.execute("""
                SELECT did, ime, priimek, drzava, rojstvo
                FROM dirkaci
                WHERE did=?
            """, [did])
            podatki = cursor.fetchone()
            return Dirkac(podatki[0], podatki[1], podatki[2], podatki[3], podatki[4])
    
    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Dirkac(*poizvedba)
            
    @staticmethod
    def vsi_dirkaci():
        '''Pridobi vse dirkace'''
        sql = '''SELECT ime,
                     priimek,
                     dirkaci.drzava,
                     dirkaci.rojstvo,
                     did
                FROM dirkaci;'''
        vsi_dirkaci = conn.execute(sql).fetchall()
        for dirkac in vsi_dirkaci:
            yield dirkac
    

    @staticmethod
    def vse_ekipe(did):
        '''Poda tabelo vseh ekip v katerih je dirkal dirkač.'''
        sql = '''SELECT DISTINCT ekipa.ime
                         FROM ekipa
                              INNER JOIN
                              rezultati ON ekipa.eid = rezultati.cid
                              INNER JOIN
                              dirkaci ON dirkaci.did = rezultati.did
                        WHERE dirkaci.did = ?'''

        ekipe = conn.execute(sql,[did]).fetchall()
#        return ekipe
        for ekipa in ekipe:
            yield ekipa

    # najboljša uvrstitev
    @staticmethod
    def najboljse_uvrstitve(ime, priimek):
        '''Poda podatke najboljše uvrstitve dirkača.'''
        sql = '''SELECT DISTINCT dirkaci.ime,
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

        podatki = (ime, priimek, ime, priimek)
        yield conn.execute(sql, podatki).fetchall()

        
    # Koliko uvrstitev na zmagovalni oder
    @staticmethod
    def zmagovalni_oder(did):
        '''Poda stevilo uvrstitev dirkaca na zmagovalni oder.'''
        sql = '''SELECT dirkaci.ime,
                               dirkaci.priimek,
                               count( * ) AS oder_za_zmagovalce,
                               dirkaci.rojstvo,
                               dirkaci.drzava
                          FROM dirkaci
                               INNER JOIN
                               rezultati ON dirkaci.did = rezultati.did
                         WHERE rezultati.pozicija < 4
                         GROUP BY dirkaci.did
                        HAVING dirkaci.did = ?'''
        yield conn.execute(sql, [did]).fetchone()

    
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
                SELECT eid, ime, drzava
                FROM ekipa
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa

    @staticmethod
    def pridobi_vse_nemce():
        sql = '''
                SELECT eid, ime FROM ekipa
                WHERE drzava = 'German'
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa
    
    @staticmethod
    def pridobi_vse_angleze():
        sql = '''
                SELECT eid, ime FROM ekipa
                WHERE drzava = 'British'
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa
    
    @staticmethod
    def pridobi_vse_italijane():
        sql = '''
                SELECT eid, ime FROM ekipa
                WHERE drzava = 'Italian'
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
    
    @staticmethod
    def pridobi_ekipo(eid):
        sql = '''SELECT eid,
                      ime,
                      drzava
                 FROM ekipa
                WHERE eid = ?;
        '''
        podatki = conn.execute(sql, [eid]).fetchone()
        return Ekipa(podatki[0], podatki[1], podatki[2])
    
    @staticmethod
    def ekipa_vsi_dirkaci(eid):
        '''Pridobi vse dirkace, ki so dirkali za to ekipo.'''
        sql = '''SELECT DISTINCT dirkaci.ime,
                               dirkaci.priimek
                 FROM dirkaci
                      INNER JOIN
                      rezultati ON dirkaci.did = rezultati.did
                      INNER JOIN
                      ekipa ON rezultati.cid = ekipa.eid
                WHERE ekipa.eid = ?;'''
        podatki = conn.execute(sql, [eid]).fetchall()
        for dirkac in podatki:
            yield dirkac
            
    @staticmethod
    def ekipa_sezone(eid):
        '''Pridobi vse sezone v katerih je sodelovala ta ekipa'''
        sql = '''select tabela.leto from (SELECT DISTINCT cid as cid,
                                strftime('%Y', dirka.datum) AS leto
                  FROM rezultati
                       INNER JOIN
                       dirka ON dirka.raceid = rezultati.rid) tabela where cid = ? ;'''
        podatki = conn.execute(sql, [eid]).fetchall()
        for leto in podatki:
            yield leto
    
            
class Dirkalisce:
    def __init__(self, cid=None, ime=None, drzava=None):
        self.id = cid
        self.ime = ime
        self.drzava = drzava
    
    def __str__(self):
        return str(self.ime)
    
    @staticmethod
    def poisci_sql(sql, podatki = None):
        for poizvedba in conn.execute(sql, podatki):
            yield Dirkalisce(*poizvedba)
            
    @staticmethod
    def pridobi_dirkalisce(cid):
        sql = '''SELECT dirkalisca.cid,
                      dirkalisca.ime,
                      dirkalisca.drzava
                 FROM dirkalisca
                WHERE cid = ?;'''
        podatki = conn.execute(sql, [cid]).fetchone()
        return Dirkalisce(podatki[0], podatki[1], podatki[2])
    
    @staticmethod
    def pridobi_vsa_dirkalisca():
        sql = '''
                SELECT cid, ime, lokacija, drzava FROM dirkalisca
                ORDER BY ime;'''
        vsa_dirkalisca = conn.execute(sql).fetchall()
        for dirkalisce in vsa_dirkalisca:
            yield dirkalisce
    
    @staticmethod        
    def poisci_po_imenu(ime, limit=None):
        sql = '''
            SELECT ime FROM dirkalisca
            WHERE ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Dirkalisce.poisci_sql(sql, podatki)
    
    @staticmethod
    def najveckrat_zmagal():
        '''Poisce dirkalisce in osebo ki je najveckarat zmagala na tem dirkaliscu ter stevilo zmag.'''
        sql = '''SELECT tabela.proga,
                       tabela.ime,
                       tabela.priimek,
                       max(tabela.st) AS stevilo_zmag
                  FROM (
                           SELECT rezultati.did,
                                  dirkaci.did,
                                  dirkaci.ime AS ime,
                                  dirkaci.priimek AS priimek,
                                  dirka.dirkalisce,
                                  dirkalisca.cid,
                                  dirkalisca.ime AS proga,
                                  count( * ) AS st
                             FROM rezultati
                                  INNER JOIN
                                  dirka ON dirka.raceid = rezultati.rid
                                  INNER JOIN
                                  dirkalisca ON dirkalisca.cid = dirka.dirkalisce
                                  INNER JOIN
                                  dirkaci ON dirkaci.did = rezultati.did
                            WHERE rezultati.pozicija = 1
                            GROUP BY rezultati.did,
                                     dirka.dirkalisce
                       )
                       tabela
                 GROUP BY dirkalisce
                 order by tabela.proga;'''
        vsa_dirkalisca = conn.execute(sql).fetchall()
        for dirkalisce in vsa_dirkalisca:
            yield dirkalisce
    
    @staticmethod        
    def kdo_najveckrat_zmagal(proga_id):
        '''Pridobi podatke o tem kdo je na dirkaliscu prog_id najveckrat zmagal
        ter kolikokrat je zmagal (proga_id, ime_dirkalisca, kdo_ime, kdo_priimek, st_zmag)'''  
        sql = '''SELECT tabela1.proga_id,
                       tabela1.proga,
                       tabela1.najboljsi_ime,
                       tabela1.najboljsi_priimek,
                       tabela1.stevilo_zmag
                  FROM (
                           SELECT tabela.proga_id AS proga_id,
                                  tabela.proga AS proga,
                                  tabela.ime AS najboljsi_ime,
                                  tabela.priimek AS najboljsi_priimek,
                                  max(tabela.st) AS stevilo_zmag
                             FROM (
                                      SELECT rezultati.did,
                                             dirkaci.did,
                                             dirkaci.ime AS ime,
                                             dirkaci.priimek AS priimek,
                                             dirka.dirkalisce,
                                             dirkalisca.cid AS proga_id,
                                             dirkalisca.ime AS proga,
                                             count( * ) AS st
                                        FROM rezultati
                                             INNER JOIN
                                             dirka ON dirka.raceid = rezultati.rid
                                             INNER JOIN
                                             dirkalisca ON dirkalisca.cid = dirka.dirkalisce
                                             INNER JOIN
                                             dirkaci ON dirkaci.did = rezultati.did
                                       WHERE rezultati.pozicija = 1
                                       GROUP BY rezultati.did,
                                                dirka.dirkalisce
                                  )
                                  tabela
                            GROUP BY dirkalisce
                            ORDER BY tabela.proga
                       )
                       tabela1
                 WHERE tabela1.proga_id = ?;''' 
        podatki = conn.execute(sql, [proga_id]).fetchone()
        yield podatki  

class Sezona:
    def __init__(self, leto=None):
        self.leto = leto
        
    def __str__(self):
        return self.leto
    
    @staticmethod
    def poisci_sql(sql, podatki = None):
        for poizvedba in conn.execute(sql, podatki):
            yield Sezona(*poizvedba)
    
    @staticmethod
    def pridobi_vse_sezone():
        '''Poisce vse sezone.'''
        sql = '''
                SELECT DISTINCT strftime('%Y', dirka.datum) AS leto
                  FROM dirka
                 ORDER BY leto DESC;'''
        vse_sezone = conn.execute(sql).fetchall()
        for sezona in vse_sezone:
            yield sezona
            
    @staticmethod
    def rezultati_sezona(sezona):
        '''Pridobi koncne rezultate sezone.'''
        sql = '''SELECT rezultati.did,
                      dirkaci.ime,
                      dirkaci.priimek,
                      sum(rezultati.tocke) AS tocke
                 FROM rezultati
                      inner JOIN
                      dirkaci ON rezultati.did = dirkaci.did
                      INNER JOIN
                      dirka ON dirka.raceid = rezultati.rid
                WHERE strftime('%Y', dirka.datum) = ?
                GROUP BY rezultati.did
                ORDER BY tocke DESC;'''
        vsi_rezultati = conn.execute(sql, sezona).fetchall()
        for rezultat in vsi_rezultati:
            yield rezultat
    
    
            
    
