import sqlite3
import csv

def napolni_dirkaci():
    with open("archive/drivers.csv", "r") as dirkaci:
        csv_reader = csv.reader(dirkaci, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        caunt = 0
        for vrstica in csv_reader:
            if caunt == 5: break
            caunt += 1
            tupl = tuple([vrstica[0]] + vrstica[4:-1])
            seznam.append(tupl)
        sql = "INSERT INTO dirkaci (did, priimek, short_name, dateofbrith, nationality) VALUES (?, ?, ?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()


def napolni_dirkalisca():
    with open("archive/circuits.csv", 'r') as dirkalisca:
        csv_reader = csv.reader(dirkalisca, delimiter=',')
        naslovi_st = next(csv_reader)
        seznam = []
        caunt = 0
        for vrstica in csv_reader:
            if caunt == 3:
                break
            caunt+=1
            tupl = tuple([vrstica[0]] + vrstica[2:5])
            seznam.append(tupl)
        sql = "INSERT INTO dirkalisca (cid, name, location, country) VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()
        
def napolni_dirka():
    with open("archive/races.csv", "r") as dirka:
        csv_reader = csv.reader(dirka, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        caunt = 0
        for vrstica in csv_reader:
            if caunt == 5: break
            caunt += 1
            tupl = tuple([vrstica[0], vrstica[3] ,vrstica[5]])
            seznam.append(tupl)
        sql = "INSERT INTO dirka (raceid, dirkalisce, date) VALUES (?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()

def napolni_ekipa():
    with open("archive/constructors.csv", "r") as ekipa:
        csv_reader = csv.reader(ekipa, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        caunt = 0
        for vrstica in csv_reader:
            if caunt == 5: break
            caunt += 1
            tupl = tuple([vrstica[0], vrstica[2], vrstica[3]])
            seznam.append(tupl)
        sql = "INSERT INTO ekipa (eid, team_name, nationality) VALUES (?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()

dirkaci = "CREATE TABLE IF NOT EXISTS dirkaci (did INTEGER PRIMARY KEY, priimek TEXT, short_name TEXT, dateofbrith DATE, nationality TEXT)"
dirkalisca = "CREATE TABLE IF NOT EXISTS dirkalisca (cid INTEGER PRIMARY KEY, name TEXT, location TEXT, country TEXT)"

dirka = "CREATE TABLE IF NOT EXISTS dirka (raceid INTEGER PRIMARY KEY, dirkalisce INTEGER, date DATE, FOREIGN KEY(dirkalisce) REFERENCES dirkalisce(cid))"

ekipa = "CREATE TABLE IF NOT EXISTS ekipa (eid INTEGER PRIMARY KEY, team_name TEXT, nationality TEXT)"

db = sqlite3.connect("f1database.sqlite3")

with db as cursor:
    cursor.execute(dirkaci)
    cursor.execute(dirkalisca)
    cursor.execute(dirka)
    cursor.execute(ekipa)
    napolni_dirkaci()
    napolni_dirkalisca()
    napolni_dirka()
    napolni_ekipa()

