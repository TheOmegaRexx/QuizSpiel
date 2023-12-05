import mysql.connector
import random
import time
import threading
from tkinter import *
from tkinter import messagebox
import customtkinter



MODUS = 0

# Einstellung aus der Text Datei rauslesen
with open('DB_Einstellung.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        if key == 'USERNAME':
            USER = value
        elif key == 'PASSWORD':
            PASSWORD = value
        elif key == 'DATABASE':
            DATABASE = value
        elif key == 'HOST':
            HOST = value

# Spiel Einstellung aus der Text Datei rauslesen

with open('Spiel_Einstellung.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        if key == 'RUNDEN':
            RUNDEN = int(value)
        elif key == 'ZEITLIMIT':
            ZEITLIMIT = int(value)
        elif key == 'BEST_OF':
            BEST_OF = int(value)
        elif key == "SPIELER1":
            SPIELER_1 = value
        elif key == "SPIELER2":
            SPIELER_2 = value


# Funktion zur Fragen aus der Datenbank entnehemen
def lese_quiz_fragen_aus_db():
    fragen = []
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor()
    cursor.execute(
        "SELECT frage, antworten, richtige_antwort, id FROM quizfragen")
    for (frage, antworten, richtige_antwort, id) in cursor:
        antworten_liste = antworten.split(",")
        fragen.append(QuizFrage(frage, antworten_liste, richtige_antwort, id))
    cursor.close()
    connection.close()
    return fragen



class Haupt_fenster:

    def __init__(self):
        self.Haupt_fenster = customtkinter.CTk()
        self.Haupt_fenster.title("Startmenu")
        self.Haupt_fenster.resizable(False, False)
        self.Haupt_fenster.eval('tk::PlaceWindow . center')

        self.start_button = customtkinter.CTkButton(
            self.Haupt_fenster, text="Quiz", command=self.modus_quiz)
        self.start_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.start_button = customtkinter.CTkButton(
            self.Haupt_fenster, text="Zeit Quiz", command=self.modus_zeit_quiz)
        self.start_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.start_button = customtkinter.CTkButton(
            self.Haupt_fenster, text="2 Spieler Quiz", command=self.modus_2_quiz)
        self.start_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.start_button = customtkinter.CTkButton(
            self.Haupt_fenster, text="Wer wird Millionär?", command=self.modus_wwm_quiz)
        self.start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.start_button = customtkinter.CTkButton(
            self.Haupt_fenster, text="DB Einstellung", command=DB_Einstellung)
        self.start_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.start_button = customtkinter.CTkButton(
            self.Haupt_fenster, text="Spiel Einstellung", command=Spiel_Einstellung)
        self.start_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.verwalten = customtkinter.CTkButton(
            self.Haupt_fenster, text="Fragen verwalten", command=Fragen_einstellung)
        self.verwalten.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.Haupt_fenster.mainloop()
    # Funktionen um die einzelne Spielmoduse auszuwählen

    def modus_quiz(self):
        global MODUS
        MODUS = 1
        self.Haupt_fenster.destroy()

    def modus_zeit_quiz(self):
        global MODUS
        MODUS = 2
        self.Haupt_fenster.destroy()

    def modus_2_quiz(self):
        global MODUS
        MODUS = 3
        self.Haupt_fenster.destroy()

    def modus_wwm_quiz(self):
        global MODUS
        MODUS = 4
        self.Haupt_fenster.destroy()


class DB_Einstellung:

    def __init__(self):

        self.Einstellung = customtkinter.CTk()
        self.Einstellung.title("DB Einstellungen")
        self.Einstellung.eval('tk::PlaceWindow . center')

        self.host_label = customtkinter.CTkLabel(self.Einstellung, text="Host:")
        self.host_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.host_entry = customtkinter.CTkEntry(self.Einstellung)
        self.host_entry.insert(0, HOST)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        self.benutzer_label = customtkinter.CTkLabel(self.Einstellung, text="Benutzername:")
        self.benutzer_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.benutzer_entry = customtkinter.CTkEntry(self.Einstellung)
        self.benutzer_entry.insert(0, USER)
        self.benutzer_entry.grid(row=1, column=1, padx=5, pady=5)

        self.passwort_label = customtkinter.CTkLabel(self.Einstellung, text="Passwort:")
        self.passwort_label.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.passwort_entry = customtkinter.CTkEntry(self.Einstellung, show="*")
        self.passwort_entry.insert(0, PASSWORD)
        self.passwort_entry.grid(row=2, column=1, padx=5, pady=5)

        self.datenbank_label = customtkinter.CTkLabel(self.Einstellung, text="Datenbank:")
        self.datenbank_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.datenbank_entry = customtkinter.CTkEntry(self.Einstellung)
        self.datenbank_entry.insert(0, DATABASE)
        self.datenbank_entry.grid(row=3, column=1, padx=5, pady=5)

        self.speichern_label = customtkinter.CTkButton(
            self.Einstellung, text="Speichern", command=self.speichern)
        self.speichern_label.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5)

        self.Einstellung.mainloop()

    def speichern(self):
        global HOST, USER, PASSWORD, DATABASE, quiz_fragen
        HOST = self.host_entry.get()
        USER = self.benutzer_entry.get()
        PASSWORD = self.passwort_entry.get()
        DATABASE = self.datenbank_entry.get()
        with open('DB_Einstellung.txt', 'w') as file:
            file.write(f'USERNAME={USER}\n')
            file.write(f'PASSWORD={PASSWORD}\n')
            file.write(f'DATABASE={DATABASE}\n')
            file.write(f'HOST={HOST}\n')
        file.close()
        try:
            quiz_fragen = lese_quiz_fragen_aus_db()
            self.Einstellung.destroy()
        except Exception:
            messagebox.showerror(title="Einstellung Fehler",
                                 message="Eingegeben Daten sind nicht richtig!")


class Spiel_Einstellung:

    def __init__(self):

        self.spiel_einstellung = customtkinter.CTk()
        self.spiel_einstellung.title("Spiel Einstellung")
        self.spiel_einstellung.eval('tk::PlaceWindow . center')

        self.runden_label = customtkinter.CTkLabel(self.spiel_einstellung, text="Runden:")
        self.runden_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.runden_entry = customtkinter.CTkEntry(self.spiel_einstellung)
        self.runden_entry.insert(0, RUNDEN)
        self.runden_entry.grid(row=0, column=1, padx=5, pady=5)

        self.zeitlimit_label = customtkinter.CTkLabel(self.spiel_einstellung, text="Zeitlimit:")
        self.zeitlimit_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.zeitlimit_entry = customtkinter.CTkEntry(self.spiel_einstellung)
        self.zeitlimit_entry.insert(0, ZEITLIMIT)
        self.zeitlimit_entry.grid(row=1, column=1, padx=5, pady=5)

        self.best_of_label = customtkinter.CTkLabel(
            self.spiel_einstellung, text="2 Spieler Gewinnerpunktzahl")
        self.best_of_label.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.best_of_entry = customtkinter.CTkEntry(self.spiel_einstellung)
        self.best_of_entry.insert(0, BEST_OF)
        self.best_of_entry.grid(row=2, column=1, padx=5, pady=5)

        self.spieler_1_label = customtkinter.CTkLabel(
            self.spiel_einstellung, text="Spieler 1:")
        self.spieler_1_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.spieler_1_entry = customtkinter.CTkEntry(self.spiel_einstellung)
        self.spieler_1_entry.insert(0, SPIELER_1)
        self.spieler_1_entry.grid(row=3, column=1, padx=5, pady=5)

        self.spieler_2_label = customtkinter.CTkLabel(
            self.spiel_einstellung, text="Spieler 2:")
        self.spieler_2_label.grid(row=4, column=0, padx=5, pady=5, sticky=E)
        self.spieler_2_entry = customtkinter.CTkEntry(self.spiel_einstellung)
        self.spieler_2_entry.insert(0, SPIELER_2)
        self.spieler_2_entry.grid(row=4, column=1, padx=5, pady=5)

        self.speichern_label = customtkinter.CTkButton(
            self.spiel_einstellung, text="Speichern", command=self.speichern)
        self.speichern_label.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5)

        self.spiel_einstellung.mainloop()

    def speichern(self):
        global RUNDEN, ZEITLIMIT, BEST_OF, SPIELER_1, SPIELER_2
        RUNDEN = int(self.runden_entry.get())
        ZEITLIMIT = int(self.zeitlimit_entry.get())
        BEST_OF = int(self.best_of_entry.get())
        SPIELER_1 = self.spieler_1_entry.get()
        SPIELER_2 = self.spieler_2_entry.get()
        with open('Spiel_Einstellung.txt', 'w') as file:
            file.write(f'RUNDEN={RUNDEN}\n')
            file.write(f'ZEITLIMIT={ZEITLIMIT}\n')
            file.write(f'BEST_OF={BEST_OF}\n')
            file.write(f'SPIELER1={SPIELER_1}\n')
            file.write(f'SPIELER2={SPIELER_2}\n')
        file.close()
        self.spiel_einstellung.destroy()


class Fragen_einstellung:

    def __init__(self):

        self.fragen_menu = customtkinter.CTk()
        self.fragen_menu.title("Fragen verwalten")
        self.fragen_menu.eval('tk::PlaceWindow . center')

        self.bs_frage = customtkinter.CTkButton(
            self.fragen_menu, text="Fragen hinzufügen", command=Fragen_hinzufügen)
        self.bs_frage.grid(row=0, column=1, padx=5, pady=5)

        self.bs_frage = customtkinter.CTkButton(
            self.fragen_menu, text="Fragen Löschen", command=Fragen_löschen)
        self.bs_frage.grid(row=1, column=1, padx=5, pady=5)

        self.bs_frage = customtkinter.CTkButton(
            self.fragen_menu, text="Bsp. Fragen", command=self.beispiel_fragen_db)
        self.bs_frage.grid(row=2, column=1, padx=5, pady=5)

    def beispiel_fragen_db(self):

        if messagebox.askyesno(title="Datenbank füllen", message="Möchtest du Beispiel Fragen zur Datenbank hinzufügen?"):
            # Verbindung zur Datenbank herstellen
            db = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD
            )

            # Cursor-Objekt erstellen
            cursor = db.cursor()

            # Datenbank erstellen
            cursor.execute("CREATE DATABASE IF NOT EXISTS quizdb")

            # Zur Datenbank wechseln
            cursor.execute("USE quizdb")

            # Tabelle erstellen
            cursor.execute("""CREATE TABLE IF NOT EXISTS quizfragen (
                            id INT NOT NULL AUTO_INCREMENT,
                            frage TEXT NOT NULL,
                            antworten TEXT NOT NULL,
                            richtige_antwort CHAR(1) NOT NULL,
                            PRIMARY KEY (id))""")

            # Beispielfragen und -antworten einfügen
            fragen = [("Was ist die Hauptstadt von Frankreich?", "A) Berlin,B) Rom,C) Paris,D) London", "C"),
                      ("Was ist die größte Insel der Welt?",
                       "A) Kuba,B) Madagaskar,C) Grönland,D) Irland", "C"),
                      ("Wer schrieb das Buch '1984'?",
                       "A) George Orwell,B) Charles Dickens,C) William Shakespeare,D) Jane Austen", "A"),
                      ("Wie heißt der höchste Berg der Welt?",
                       "A) Mount Everest,B) Kilimandscharo,C) Mount Fuji,D) Matterhorn", "A"),
                      ("Wie heißt das kleinste Land der Welt?",
                       "A) Monaco,B) Vatikanstadt,C) Andorra,D) San Marino", "B"),
                      ("Wie viele Sterne hat die amerikanische Flagge?",
                       "A) 48,B) 50,C) 52,D) 54", "B"),
                      ("Welches Tier ist das größte auf der Erde?",
                       "A) Elefant,B) Wal,C) Giraffe,D) Nashorn", "B"),
                      ("In welchem Jahr begann der Erste Weltkrieg?",
                       "A) 1905,B) 1914,C) 1923,D) 1939", "B"),
                      ("Wie heißt der längste Fluss der Welt?",
                       "A) Nil,B) Amazonas,C) Jangtse,D) Mississippi", "A"),
                      ("Wer hat die Mona Lisa gemalt?",
                       "A) Michelangelo,B) Leonardo da Vinci,C) Vincent van Gogh,D) Pablo Picasso", "B"),
                      ("Wie lautet der bekannteste Spitzname des Boxers Muhammad Ali?",
                       "A) The Great,B) Iron Mike,C) The Greatest,D) The Champ", "C"),
                      ("Wer war der erste Mensch, der auf dem Mond landete?",
                       "A) Neil Armstrong,B) Buzz Aldrin,C) Yuri Gagarin,D) Alan Shepard", "A"),
                      ("Welche Sportart wird auf einem Feld mit einem kreisförmigen Ziel gespielt?",
                       "A) Fußball,B) Hockey,C) Rugby,D) Lacrosse", "D"),
                      ("Wie heißt die Hauptfigur im Film 'Titanic'?", "A) Rose,B) Jack,C) Cal,D) Molly", "A"
                       ),
                      ("Welches Element hat das chemische Symbol Na?", "A) Natrium,B) Nickel,C) Neon,D) Stickstoff", "A"
                       ),
                      ("Wer schrieb den Roman 'Der Hobbit'?", "A) J.K. Rowling,B) George R.R. Martin,C) J.R.R. Tolkien,D) C.S. Lewis", "C"
                       ),
                      ("Wer gewann den Oscar für die beste Regie für den Film 'Schindlers Liste'?", "A) Steven Spielberg,B) Martin Scorsese,C) Francis Ford Coppola,D) Stanley Kubrick", "A"
                       ),
                      ("Welches Land hat die größte Fläche?",
                       "A) Russland,B) USA,C) China,D) Kanada", "A"),
                      ("Wie viele Planeten gibt es in unserem Sonnensystem?",
                       "A) 7, B) 8, C) 9, D) 10", "B"),
                      ("Wer gewann den Oscar für die beste Regie für den Film 'Schindlers Liste'?",
                       "A) Steven Spielberg, B) Martin Scorsese, C) Francis Ford Coppola, D) Stanley Kubrick", "A"),
                      ("Wie viele Kontinente gibt es auf der Welt?",
                       "A) 5, B) 6, C) 7, D) 8", "C"),
                      ("Wie lange dauert eine typische Schwangerschaft?",
                       "A) 6 Monate, B) 8 Monate, C) 9 Monate, D) 12 Monate", "C"),
                      ("Welches Land gewann die Fußball-Weltmeisterschaft 2018?",
                       "A) Deutschland, B) Frankreich, C) Brasilien, D) Spanien", "B"),
                      ("Wie viele Elemente gibt es im Periodensystem?",
                       "A) 118, B) 120, C) 122, D) 124", "A"),
                      ("Wie heißt die Hauptstadt von Australien?",
                       "A) Melbourne, B) Sydney, C) Perth, D) Canberra", "D"),
                      ("Welches ist das am meisten gesprochene Sprache der Welt?",
                       "A) Englisch, B) Chinesisch, C) Spanisch, D) Hindi", "B"),
                      ("Wer schrieb das Buch 'Pride and Prejudice'?",
                       "A) Jane Austen, B) Emily Bronte, C) Charlotte Bronte, D) Virginia Woolf", "A"),
                      ("Wie viele Millimeter sind in einem Zentimeter?",
                       "A) 10, B) 100, C) 1000, D) 10.000", "A"),
                      ("Welches Land hat die längste Landgrenze?",
                       "A) Russland, B) China, C) USA, D) Kanada", "A"),
                      ("Welcher Planet in unserem Sonnensystem ist der kleinste?",
                       "A) Merkur, B) Mars, C) Venus, D) Pluto", "D")

                      ]

            for frage in fragen:
                cursor.execute(
                    "INSERT INTO quizfragen (frage, antworten, richtige_antwort) VALUES (%s, %s, %s)", frage)

            # Änderungen speichern
            db.commit()

            # Verbindung schließen
            db.close()
            messagebox.showinfo(
                title="Datenbank", message="Datenbank wurde mit Beispielfragen gefüllt")


class Fragen_löschen:

    def __init__(self):
        global fragenn
        self.fragen_ansehen = customtkinter.CTk()
        self.fragen_ansehen.title("Alle Fragen")

        self.fragen_ansehen_label = customtkinter.CTkLabel(
            self.fragen_ansehen, text="Alle Fragen")
        self.fragen_ansehen_label.pack()

        self.fragen_ansehen_listbox = Listbox(self.fragen_ansehen, width=60)
        self.fragen_ansehen_listbox.pack()

        for i, frage in enumerate(quiz_fragen):
            question_string = f"{i+1}. {frage.frage}"
            self.fragen_ansehen_listbox.insert(END, question_string)

        self.delete_button = customtkinter.CTkButton(
            self.fragen_ansehen, text="Frage löschen", command=self.delete_question)
        self.delete_button.pack()
        fragenn = frage

        self.fragen_ansehen.mainloop()

    def delete_question(self):
        selected_index = self.fragen_ansehen_listbox.curselection()
        if len(selected_index) == 0:
            messagebox.showerror(
                title="Fehler", message="Bitte wählen Sie eine Frage aus.")
            return
        question_id = selected_index[0] + 1
        quiz_fragen.pop(question_id - 1)
        self.fragen_ansehen_listbox.delete(selected_index)
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM quizfragen WHERE id={fragenn.id}")
        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo(
            title="Erfolg", message="Frage wurde erfolgreich gelöscht.")


class Fragen_hinzufügen:

    def __init__(self):
        self.frage_hinzufügen = customtkinter.CTk()
        self.frage_hinzufügen.title("Fragen hinzugügen")

        self.frage_hinzufügen_label = customtkinter.CTkLabel(self.frage_hinzufügen, text="Frage:")
        self.frage_hinzufügen_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.frage_hinzufügen_entry = customtkinter.CTkEntry(self.frage_hinzufügen,)
        self.frage_hinzufügen_entry.grid(row=0, column=1, padx=5, pady=5)

        self.antwort_a_label = customtkinter.CTkLabel(self.frage_hinzufügen, text="Antwort A):")
        self.antwort_a_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.antwort_a_entry = customtkinter.CTkEntry(self.frage_hinzufügen,)
        self.antwort_a_entry.grid(row=1, column=1, padx=5, pady=5)

        self.antwort_b_label = customtkinter.CTkLabel(self.frage_hinzufügen, text="Antwort B):")
        self.antwort_b_label.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.antwort_b_entry = customtkinter.CTkEntry(self.frage_hinzufügen)
        self.antwort_b_entry.grid(row=2, column=1, padx=5, pady=5)

        self.antwort_c_label = customtkinter.CTkLabel(self.frage_hinzufügen, text="Antwort C):")
        self.antwort_c_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.antwort_c_entry = customtkinter.CTkEntry(self.frage_hinzufügen,)
        self.antwort_c_entry.grid(row=3, column=1, padx=5, pady=5)

        self.antwort_d_label = customtkinter.CTkLabel(self.frage_hinzufügen, text="Antwort D):")
        self.antwort_d_label.grid(row=4, column=0, padx=5, pady=5, sticky=E)
        self.antwort_d_entry = customtkinter.CTkEntry(self.frage_hinzufügen,)
        self.antwort_d_entry.grid(row=4, column=1, padx=5, pady=5)

        self.richtig = customtkinter.CTkLabel(
            self.frage_hinzufügen, text="Wähle die Richtige antwort:")
        self.richtig.grid(row=5, column=0,)

        global auswahl_antwort
        auswahl_antwort = IntVar(self.frage_hinzufügen)

        self.antwort_a_button = customtkinter.CTkRadioButton(self.frage_hinzufügen, text="A", value=1, variable=auswahl_antwort)
        self.antwort_a_button.grid(row=6, column=0)

        self.antwort_b_button = customtkinter.CTkRadioButton(self.frage_hinzufügen, text="B", value=2, variable=auswahl_antwort)
        self.antwort_b_button.grid(row=6, column=1)

        self.antwort_c_button = customtkinter.CTkRadioButton(self.frage_hinzufügen, text="C", value=3, variable=auswahl_antwort)
        self.antwort_c_button.grid(row=6, column=2)

        self.antwort_d_button = customtkinter.CTkRadioButton(self.frage_hinzufügen, text="D", value=4, variable=auswahl_antwort)
        self.antwort_d_button.grid(row=6, column=3)

        self.frage_hinzufügen_button = customtkinter.CTkButton(
            self.frage_hinzufügen, text="Frage hinzufügen", command=self.fragen_hinzufügen_db)
        self.frage_hinzufügen_button.grid(row=7, column=0)

        self.frage_hinzufügen.mainloop()

    def fragen_hinzufügen_db(self):
        if auswahl_antwort.get() == 1:
            richtige_antwort = "A"
        elif auswahl_antwort.get() == 2:
            richtige_antwort = "B"
        elif auswahl_antwort.get() == 3:
            richtige_antwort = "C"
        elif auswahl_antwort.get() == 4:
            richtige_antwort = "D"
        else:
            messagebox.showerror("Antwort auswahl", "Wähle eine Antwort aus")
            return

        db_frage = (self.frage_hinzufügen_entry.get(), self.antwort_a_entry.get(
        ) + "," + self.antwort_b_entry.get() + "," + self.antwort_c_entry.get() + "," + self.antwort_d_entry.get(), richtige_antwort)

        # Verbindung zur Datenbank herstellen
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        # Cursor-Objekt erstellen
        cursor = db.cursor()

        # Datenbank erstellen
        cursor.execute("CREATE DATABASE IF NOT EXISTS quizdb")

        # Zur Datenbank wechseln
        cursor.execute("USE quizdb")

        # Tabelle erstellen
        cursor.execute("""CREATE TABLE IF NOT EXISTS quizfragen (
                            id INT NOT NULL AUTO_INCREMENT,
                            frage TEXT NOT NULL,
                            antworten TEXT NOT NULL,
                            richtige_antwort CHAR(1) NOT NULL,
                            PRIMARY KEY (id))""")
        fragen = [db_frage]

        for frage in fragen:
            cursor.execute(
                "INSERT INTO quizfragen (frage, antworten, richtige_antwort) VALUES (%s, %s, %s)", frage)

        # Änderungen speichern
        db.commit()

        # Verbindung schließen
        db.close()
        messagebox.showinfo(
            title="Frage", message="Frage wurde der Datenbank hinzugefügt")


class QuizFrage:
    def __init__(self, frage, antworten, richtige_antwort, id):
        self.frage = frage
        self.antworten = antworten
        self.richtige_antwort = richtige_antwort
        self.id = id


class QuizStatistik:
    def __init__(self):
        self.gesamtzahl_fragen = 0
        self.gesamtzahl_richtige_antworten = 0

    def frage_beantwortet(self, ist_richtig):
        self.gesamtzahl_fragen += 1
        if ist_richtig:
            self.gesamtzahl_richtige_antworten += 1

    def prozent_richtig(self):
        if self.gesamtzahl_fragen == 0:
            return 0
        return self.gesamtzahl_richtige_antworten / self.gesamtzahl_fragen * 100


class Quiz:

    def __init__(self):
        self.master = customtkinter.CTk()
        self.master.resizable(False, False)
        self.master.geometry("720x480")
        self.master.title("Quiz")

        self.frage_label = customtkinter.CTkLabel(self.master, text='', font=("arial", 20))
        self.frage_label.pack()

        self.box = customtkinter.CTkFrame(self.master)
        self.antwort_button_1 = customtkinter.CTkButton(
            self.box, text='', width=100, height=100, command=lambda: self.check_antwort(0))
        self.antwort_button_1.grid(column=1, row=1)

        self.antwort_button_2 = customtkinter.CTkButton(
            self.box, text='', width=100, height=100, command=lambda: self.check_antwort(1))
        self.antwort_button_2.grid(column=0, row=1)

        self.antwort_button_3 = customtkinter.CTkButton(
            self.box, text='', width=100, height=100, command=lambda: self.check_antwort(2))
        self.antwort_button_3.grid(column=1, row=0)

        self.antwort_button_4 = customtkinter.CTkButton(
            self.box, text='', width=100, height=100, command=lambda: self.check_antwort(3))
        self.antwort_button_4.grid(column=0, row=0)

        self.box.pack()

        self.auswahl = ["D", "C", "B", "A"]
        self.question_index = 0
        self.fragen_update()

    def fragen_update(self):
        frage = quiz_fragen[self.question_index]
        label_frage = frage.frage
        antworten = frage.antworten
        self.frage_label.configure(text=label_frage)

        for i in range(4):
            self.box.grid_slaves()[i].configure(text=antworten[i])

    def check_antwort(self, index):
        frage = quiz_fragen[self.question_index]
        if self.auswahl[index] == frage.richtige_antwort:
            quiz_statistik.frage_beantwortet(True)
        else:
            quiz_statistik.frage_beantwortet(False)

        self.question_index += 1
        if self.question_index < RUNDEN:
            self.fragen_update()
        else:
            self.master.destroy()
            Stats()


class ZeitQuiz(Quiz):

    def __init__(self):
        super().__init__()
        self.remaining_time = ZEITLIMIT
        self.countdown_label = customtkinter.CTkLabel(self.master, text='', font=("arial", 20))
        self.countdown_label.pack()
        self.start_countdown()

    def start_countdown(self):
        # Starte den Countdown in einem separaten Thread, damit die GUI nicht blockiert wird
        threading.Thread(target=self.countdown, args=(
            self.remaining_time,)).start()

    def countdown(self, t):
        while t:
            # Aktualisiere die Countdown-Anzeige
            self.countdown_label.configure(text=f"Verbleibende Zeit: {t}")
            time.sleep(1)
            t -= 1
        # Wenn die Zeit abgelaufen ist, werte die restlichen Fragen als falsch und das Spiel wird beendet
        for i in range(self.question_index, RUNDEN):
            quiz_statistik.frage_beantwortet(False)
        Stats()
        self.master.destroy()


class Quiz2(Quiz):

    def __init__(self):
        super().__init__()
        self.spieler1 = SPIELER_1
        self.spieler2 = SPIELER_2
        self.rundenanzahl = RUNDEN
        self.spieler1_punktzahl = 0
        self.spieler2_punktzahl = 0
        self.spieler_reinfolge = True
        self.spieler_label = customtkinter.CTkLabel(
            self.master, text=f"Runde {self.question_index + 1} - Spieler {self.spieler1} ist dran!", font=("arial", 20))
        self.spieler_label.pack()
        self.spieler_punkte1_label = customtkinter.CTkLabel(
            self.master, text=f"{self.spieler1}: {self.spieler1_punktzahl}", font=("arial", 20))
        self.spieler_punkte1_label.pack(side=LEFT, padx=20, pady=20)
        self.spieler_punkte2_label = customtkinter.CTkLabel(
            self.master, text=f"{self.spieler2}: {self.spieler2_punktzahl}", font=("arial", 20))
        self.spieler_punkte2_label.pack(side=RIGHT, padx=20, pady=20)

    def check_antwort(self, index):
        frage = quiz_fragen[self.question_index]
        if self.auswahl[index] == frage.richtige_antwort:
            if self.spieler_reinfolge:
                self.spieler1_punktzahl += 1
            else:
                self.spieler2_punktzahl += 1

        self.question_index += 1

        if self.spieler1_punktzahl == BEST_OF:
            self.master.destroy()
            Ergebnis(f"Spiel beendet! Gewinner: {self.spieler1}")

        elif self.spieler2_punktzahl == BEST_OF:
            self.master.destroy()
            Ergebnis(f"Spiel beendet! Gewinner: {self.spieler2}")

        elif self.question_index < RUNDEN:
            self.fragen_update()
        else:
            self.master.destroy()
            Ergebnis("Spiel beendet! Unendschieden")

        if self.question_index % 2 == 0:
            self.spieler_reinfolge = TRUE
        else:
            self.spieler_reinfolge = FALSE

        if self.spieler_reinfolge:
            aktueller_spieler = self.spieler1
        else:
            aktueller_spieler = self.spieler2

        if self.question_index <= self.rundenanzahl:
            self.spieler_label.configure(
                text=f"Runde {self.question_index + 1} - Spieler {aktueller_spieler} ist dran!")
            self.spieler_punkte1_label.configure(
                text=f"{self.spieler1}: {self.spieler1_punktzahl}")
            self.spieler_punkte2_label.configure(
                text=f"{self.spieler2}: {self.spieler2_punktzahl}")


class QuizWwd(Quiz):

    def __init__(self):
        super().__init__()

        self.gewinnstufen = ["500 €", "1.000 €", "2.000 €", "5.000 €", "10.000 €",
                             "20.000 €", "50.000 €", "125.000 €", "500.000 €",
                             "1.000.000 €"]
        self.gewinnstufe_index = 0

        self.gewinn_label = customtkinter.CTkLabel(self.master, text="Gewinnstufe: ",
                                  font=("arial", 20))
        self.gewinn_label.pack(side=BOTTOM, pady=20)
        self.show_gewinnstufe()

        self.publikumsjoker_button = customtkinter.CTkButton(self.master, text="Publikumsjoker",
                                            width=15, command=self.publikumsjoker)
        self.publikumsjoker_button.pack(side=LEFT, padx=20, pady=20)

        self.telefonjoker_button = customtkinter.CTkButton(self.master, text="Telefonjoker",
                                          width=15, command=self.telefonjoker)
        self.telefonjoker_button.pack(side=RIGHT, padx=20, pady=20)

        self.fiftyfifty_button = customtkinter.CTkButton(self.master, text="FiftyFifty",
                                        width=15, command=self.fiftyfifty)
        self.fiftyfifty_button.pack(side=RIGHT, padx=20, pady=20)

    def show_gewinnstufe(self):
        gewinnstufe = self.gewinnstufen[self.gewinnstufe_index]
        self.gewinn_label.configure(text="Gewinnstufe: " + gewinnstufe)

    def publikumsjoker(self):
        richtige_antwort = quiz_fragen[self.question_index].richtige_antwort
        if richtige_antwort == "A":
            antwort = "A"
        elif richtige_antwort == "B":
            antwort = "B"
        elif richtige_antwort == "C":
            antwort = "C"
        else:
            antwort = "D"

        messagebox.showinfo(
            "Publikumsjoker", f"Das Publikum ist sich zu 100% sicher, dass die richtige Antwort {antwort} ist.")
        self.publikumsjoker_button.configure(state=DISABLED)

    def telefonjoker(self):
        Telefon_kontakte = ["Marvin", "Issar", "Tom", "Marco",
                            "Vincent", "Cedrik", "Kamil", "Seyid", "Yunnis"]
        i = random.randint(0, 9)

        richtige_antwort = quiz_fragen[self.question_index].richtige_antwort
        if richtige_antwort == "A":
            antwort = "Ich denke, es ist Antwort A."
        elif richtige_antwort == "B":
            antwort = "Ich denke, es ist Antwort B."
        elif richtige_antwort == "C":
            antwort = "Ich denke, es ist Antwort C."
        else:
            antwort = "Ich denke, es ist Antwort D."
        messagebox.showinfo(
            "Telefonjoker", f"{Telefon_kontakte[i]} sagt: " + antwort)
        self.telefonjoker_button.configure(state=DISABLED)

    def fiftyfifty(self):
        richtige_antwort = quiz_fragen[self.question_index].richtige_antwort
        if richtige_antwort == "A":
            antwort_richtig = "Antwort A"
        elif richtige_antwort == "B":
            antwort_richtig = "Antwort B"
        elif richtige_antwort == "C":
            antwort_richtig = "Antwort C"
        else:
            antwort_richtig = "Antwort D"

        if richtige_antwort != "A":
            antwort_falsch = "Antwort A"
        elif richtige_antwort != "B":
            antwort_falsch = "Antwort B"
        elif richtige_antwort != "C":
            antwort_falsch = "Antwort C"
        else:
            antwort_falsch = "Antwort D"

        zufall = random.randint(0, 1)
        if zufall == 1:
            messagebox.showinfo(
                "FiftyFifty", f"Es ist {antwort_richtig} oder {antwort_falsch}.")
        else:
            messagebox.showinfo(
                "FiftyFifty", f"Es ist {antwort_falsch} oder {antwort_richtig}.")
        self.fiftyfifty_button.configure(state=DISABLED)

    def check_antwort(self, index):
        frage = quiz_fragen[self.question_index]
        if self.auswahl[index] == frage.richtige_antwort:
            self.gewinnstufe_index += 1
            if self.gewinnstufe_index < len(self.gewinnstufen):
                self.show_gewinnstufe()
                self.question_index += 1

                self.fragen_update()
            else:
                self.master.destroy()
                Ergebnis(
                    "Herzlichen Glückwunsch!\n Sie haben 1.000.000$ gewonnen!")

        else:
            self.master.destroy()

            Ergebnis(
                "Verloren!!! \nDie Antwort war leider Falsch das heißt es gibt kein Preis für sie :(")


class Stats:

    def __init__(self):
        self.Stats = customtkinter.CTk()
        self.Stats.title("Statistiken")
        self.Stats_label = customtkinter.CTkLabel(
            self.Stats, text=f"Quiz beendet!\nSie haben {quiz_statistik.gesamtzahl_richtige_antworten} von {quiz_statistik.gesamtzahl_fragen} Fragen richtig beantwortet.\nIhre Erfolgsquote beträgt {quiz_statistik.prozent_richtig():.2f}%.")
        self.Stats.eval('tk::PlaceWindow . center')
        self.Stats_nochmal = customtkinter.CTkButton(
            self.Stats, text="Nochmal", command=self.nochmal)
        self.Stats_beenden = customtkinter.CTkButton(
            self.Stats, text="Beenden", command=self.beenden)
        self.Stats_label.pack()
        self.Stats_nochmal.pack()
        self.Stats_beenden.pack()
        self.Stats.resizable(False, False)
        self.Stats.mainloop()

    def nochmal(self):
        self.Stats.destroy()
        main()

    def beenden(self):
        self.Stats.destroy()


class Ergebnis:

    def __init__(self, text):
        self.Stats = customtkinter.CTk()
        self.Stats.title("Ergebnis")
        self.Stats_label = customtkinter.CTkLabel(
            self.Stats, text=text)
        self.Stats.eval('tk::PlaceWindow . center')
        self.Stats_nochmal = customtkinter.CTkButton(
            self.Stats, text="Nochmal", command=self.nochmal)
        self.Stats_beenden = customtkinter.CTkButton(
            self.Stats, text="Beenden", command=self.beenden)
        self.Stats_label.pack()
        self.Stats_nochmal.pack()
        self.Stats_beenden.pack()
        self.Stats.resizable(False, False)
        self.Stats.mainloop()

    def nochmal(self):
        self.Stats.destroy()
        main()

    def beenden(self):
        self.Stats.destroy()


# Funktion um das Spiel zu starten


def main():
    global quiz_fragen, quiz_statistik, frage

    quiz_fragen = lese_quiz_fragen_aus_db()

    quiz_statistik = QuizStatistik()
    Haupt_fenster()

    frage = quiz_fragen
    frage = random.shuffle(frage)

    if MODUS == 1:
        Spiel_Quiz = Quiz()
        Spiel_Quiz.master.mainloop()
    elif MODUS == 2:
        Spiel_Quiz = ZeitQuiz()
        Spiel_Quiz.master.mainloop()
    elif MODUS == 3:
        Spiel_Quiz = Quiz2()
        Spiel_Quiz.master.mainloop()
    elif MODUS == 4:
        Spiel_Quiz = QuizWwd()
        Spiel_Quiz.master.mainloop()
    else:
        pass


# Startet das Spiel
if __name__ == "__main__":
    main()
