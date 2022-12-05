import sqlite3

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

def napolni_dirkaci():
    with open("archive/drivers.csv", "r") as dirkaci:
        for vrstica in list(dirkaci)[1:]:
            id, *_, short_name, ime, priimek, date, country = vrstica.strip().split(",")
            print(id, short_name, ime, priimek, date, country)

napolni_dirkaci()