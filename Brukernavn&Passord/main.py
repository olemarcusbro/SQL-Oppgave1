import tkinter as tk
import sqlite3
import csv
import hashlib
import customtkinter as ctk
from PIL import ImageTk #Importerer ImageTk fra PIL biblioteket, men fikk ikke bruk for dette alivevel.
 
with sqlite3.connect("Database.db") as db: #Lager en database som heter user_database.db
    cursor = db.cursor()#Lager en cursor som heter db.cursor
 
#Lager en tabell som heter users, legger til ID som primary key og at det må være integer.
#Legger til username og passord med varchar for å begrense antall tegn.
#Bruker NOT NULL sånn at det ikke kan være mellomromm eller tomme felt.
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
password VARCHAR(100) NOT NULL);
''')#Lager en tabell som heter users, legger til ID som primary key og at det må være integer.      
 
with open('brukerdatabase.csv', 'r') as file:#Åpner en csv fil som heter brukerdatabase.csv
    # Create a CSV reader
    reader = csv.reader(file)#Lager en csv reader
    for row in reader:#For hver rad i csv filen
 
        cursor.execute('''
        INSERT INTO users(username, password)
        VALUES(?, ?)''', (row[0], hashlib.sha256(row[1].encode()).hexdigest()))
 
    db.commit()#Lagrer endringene i databasen
 
def Login():#Lager en funksjon som heter Login
    UserName = BrukerNavnEntry.get() #Denne koden bruker .get til å hente ut hva brukeren skriver i username_entry feltet og kaller det for username
    PassWord = PassordEntry.get() ##Denne koden bruker .get til å hente ut hva brukeren skriver i password_entry feltet og kaller det for password
    HashedPassword = hashlib.sha256(PassWord.encode()).hexdigest() #Krypterer password varibialen med hashlib og kaller det for hashed_password
 
# Sjekker om brukeren finnes i databasen.
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?''', (UserName, HashedPassword))#Henter ut brukernavn og passord fra databasen

    if cursor.fetchall():
        print("Du har logget inn")#Hvis brukernavn og passord stemmer overens så vil det printe ut "Login successful"

    else:#Hvis brukernavn og passord stemmer overens så vil det printe ut "Login successful"
        print("Du har ikke logget inn noe er skrevet feil")#Hvis brukernavn og passord ikke stemmer overens så vil det printe ut "Login failed"



BgColor = "black" #Setter bakgrunnsfargen til alle fg_color til svart

Root = tk.Tk()#Lager et vindu som heter Root
Root.title("Login inn i systemet")#Setter tittelen på vinduet til "Login inn i systemet"
Root.eval('tk::PlaceWindow . center')#Setter vinduet i midten av skjermen
Root.geometry("300x300",)#Setter størrelsen på vinduet til 300x300
Root.configure(bg='dark grey')#Endrer bakgrunnsfargen til grå



Brukernanlabel = ctk.CTkLabel(Root,#Lager en label som heter brukernavnlabel
                              text_color="black", #Endrer fargen på teksten til svart
                              font=("TkHeadingFont", 20),#Endrer fonten til 20
                              text="Skriv inn ditt Brukernavn:").pack()#Pakker inn brukernavnlabelo og brukernavnentry feltet

BrukerNavnEntry = ctk.CTkEntry(Root,#Lager et brukernavnentry felt
                               fg_color=BgColor,#Endrer fargen på teksten i feltet
                               font=("TkMenuFont", 15),)#Lager et brukernavnentry felt og setter fonten til 15
BrukerNavnEntry.pack()#Pakker inn brukernavnentry feltet

Passordlabel = ctk.CTkLabel(Root,#label for passord
                        text_color="black",#Endrer fargen på teksten til svart
                        font=("TkHeadingFont", 20),#Endrer fonten til 20
                        text="Skriv inn ditt Passord:"#lager en tekst som står skriv inn ditt passord
                        ).pack()#Pakker inn passordlabel

PassordEntry = ctk.CTkEntry(Root,#Lager et passordentry felt
                            fg_color=BgColor,#Endrer fargen på teksten i feltet
                            font=("TkMenuFont", 15),)#Lager et passordentry felt og setter fonten til 15
PassordEntry.pack()#Pakker inn passordentry feltet

loginButton = ctk.CTkButton(Root,#Lager en knapp som heter loginbutton
                            text="Login",#Endrer teksten på det som står i knappen
                            fg_color=BgColor,#Endrer fargen på på selve knappen
                            text_color="white",#Endrer fargen på teksten til knappen
                            hover_color="grey",#Endrer fargen til knappen når du holder over den
                            font=("TkMenuFont", 15),#Endrer fonten skriften til knappen
                            cursor="hand2",#Endrer cursor til en hånd når du holder over knappen
                            command=Login,).pack(pady=30) 

Root.mainloop()#Kjører programmet
