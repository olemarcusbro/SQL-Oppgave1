import sqlite3 #Importerer sqlite3
import csv #Importerer csv
import hashlib #Importerer hashlib
 
with sqlite3.connect("Database.db") as DB: #Lager en database som heter Database.db
    Cursor = DB.cursor()#Lager en Cursor som heter DB.cursor
 
#Lager en tabell som heter users, legger til ID som primary key og at det må være integer.
#Legger til username og passord med varchar for å begrense antall tegn.
#Bruker NOT NULL sånn at det ikke kan være mellomromm eller tomme felt.
Cursor.execute('''
CREATE TABLE IF NOT EXISTS Brukerdatabase(id INTEGER PRIMARY KEY, fname VARCHAR(25) NOT NULL, ename VARCHAR(30) NOT NULL, epost VARCHAR (50), tlf INTEGER, postnummer INTEGER)
''')#Lager en tabell som heter users, legger til ID som primary key og at det må være integer.      
 
 # Leser fra csv filen og legger til i databasen
with open('Brukerdatabase.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        Cursor.execute('''
        INSERT INTO Brukerdatabase(fname, ename, epost, tlf, postnummer)
        VALUES(?, ?, ?, ?, ?)''', row)
 
    

# Sletter rad 1 om den eksisterer fra før av
Cursor.execute('''
DELETE FROM Brukerdatabase WHERE id = ?''', (1,))

# Putter inn en fake rad som id 1
Cursor.execute('''
INSERT INTO Brukerdatabase(id, fname, ename, epost, tlf, postnummer)
VALUES(?, ?, ?, ?, ?, ?)''', (1, 'fake', 'fake', 'fake', 'fake',  'fake'))

# Sletter den fake raden
Cursor.execute('''
DELETE FROM Brukerdatabase WHERE id = ?''', (1,))

# Nå når mann setter inn en ny rad så vil den automatisk starte ifra ID 2. 
Cursor.execute('''
INSERT INTO Brukerdatabase(fname, ename, epost, tlf, postnummer)
VALUES(?, ?, ?, ?, ?)''', (row[0], row[1], row[2], row[3], row[4]))

 # Lagrer endringene som skjer i databasen sånn at de brukerne som er slettet faktisk blir slettet.
DB.commit()