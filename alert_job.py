import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, Listbox, END, Toplevel
from datetime import datetime, timedelta
from tabulate import tabulate
from sqlite3 import OperationalError

# Fonction pour ajouter une recherche de stage
def ajouter_recherche():
    date_candidature = datetime.now().strftime('%d-%m-%Y %H:%M')

    cv_envoyes = entry_cv_envoyes.get()
    lettre_envoyes = entry_lettre_envoyes.get()
    nom_societe = entry_nom_societe.get()
    Téléphone = entry_Téléphone.get()
    lien_recrutment = entry_lien_recrutment.get()

    # Ajouter la recherche dans la base de données
    cursor.execute('''
        INSERT INTO recherches_stages (date_candidature, cv_envoyes, lettre_envoyes, nom_societe, lien_recrutment, reponse_societe)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date_candidature, cv_envoyes, lettre_envoyes, nom_societe, lien_recruitment, None))
    conn.commit()
    messagebox.showinfo("Succès", "Recherche de stage ajoutée avec succès")
    mettre_a_jour_listbox()  # Mettre à jour la liste après l'ajout

# Fonction pour mettre à jour la Listbox avec les recherches sauvegardées
def mettre_a_jour_listbox():
    listbox_recherches.delete(0, END)
    try:
        cursor.execute('SELECT id, date_candidature, nom_societe, telephone, reponse_societe FROM recherches_stages')
        resultats = cursor.fetchall()

        titres = ["ID", "Date de Candidature", "Nom Société", "Téléphone", "Réponse Société"]
        listbox_recherches.insert(END, " | ".join(titres))

        for resultat in resultats:
            colalign = ["center"] * len(resultat)
            listbox_recherches.insert(END, tabulate([resultat], headers=titres, tablefmt='plain').split('\n')[1])
    except OperationalError as e:
        print(f"Erreur SQL: {e}")

# Fonction pour mettre à jour l'heure sur l'interface principale
def mettre_a_jour_heure():
    heure_actuelle = datetime.now().strftime('%d-%m-%Y %H:%M')
    label_heure.config(text=f"{heure_actuelle}")
    fenetre.after(1000, mettre_a_jour_heure)  # Mettre à jour l'heure chaque seconde

# Fonction pour afficher la fenêtre d'ajout de recherche
def afficher_fenetre_ajout_recherche():
    fenetre_ajout = Toplevel(fenetre)
    fenetre_ajout.title("Ajouter une recherche")

    # Labels et Entry pour saisir les informations

    Label(fenetre_ajout, text="CV envoyés:").grid(row=1, column=0)
    cv_var = IntVar()
    Checkbutton(fenetre_ajout, variable=cv_var, text="Oui").grid(row=1, column=1)

    Label(fenetre_ajout, text="Lettre envoyés:").grid(row=2, column=0)
    entry_lettre_envoyes_ajout = Entry(fenetre_ajout)
    entry_lettre_envoyes_ajout.grid(row=2, column=1)

    Label(fenetre_ajout, text="Téléphone:").grid(row=3, column=0)
    entry_nom_societe_ajout = Entry(fenetre_ajout)
    entry_nom_societe_ajout.grid(row=3, column=1)

    Label(fenetre_ajout, text="Nom de la Société:").grid(row=3, column=0)
    entry_nom_societe_ajout = Entry(fenetre_ajout)
    entry_nom_societe_ajout.grid(row=4, column=1)

    Label(fenetre_ajout, text="Lien de Recrutement:").grid(row=4, column=0)
    entry_lien_recrutment_ajout = Entry(fenetre_ajout)
    entry_lien_recrutment_ajout.grid(row=5, column=1)

    # Bouton pour ajouter la recherche depuis la fenêtre d'ajout
    Button(fenetre_ajout, text="Ajouter Recherche", command=lambda: ajouter_recherche_from_window(
        fenetre_ajout,
        entry_cv_envoyes_ajout.get(),
        entry_lettre_envoyes_ajout.get(),
        entry_nom_societe_ajout.get(),
        entry_lien_recrutment_ajout.get()
    )).grid(row=5, column=0, columnspan=2)

# Fonction pour ajouter une recherche depuis la fenêtre d'ajout
def ajouter_recherche_from_window(fenetre_ajout, cv, lettre, nom_societe, lien_recrutment):
    date_candidature = datetime.now().strftime('%d-%m-%Y %H:%M')

    cv = "Oui" if cv_var.get() == 1 else "Non"
    lettre = "Oui" if lettre_var.get() == 1 else "Non"

    cursor.execute('''
        INSERT INTO recherches_stages (date_candidature, cv_envoyes, lettre_envoyes, nom_societe, Téléphone, lien_recrutment, reponse_societe)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date_candidature, cv, lettre, nom_societe, Telephone, lien_recrutment, None))
    conn.commit()
    messagebox.showinfo("Succès", "Recherche de stage ajoutée avec succès")
    mettre_a_jour_listbox()  # Mettre à jour la liste après l'ajout
    fenetre_ajout.destroy()  # Fermer la fenêtre d'ajout

# Création d'une base de données SQLite
conn = sqlite3.connect('recherches_stages.db')
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recherches_stages (
        id INTEGER PRIMARY KEY,
        date_candidature TEXT,
        cv_envoyes TEXT,
        lettre_envoyes TEXT,
        nom_societe TEXT,
        Telephone TEXT,
        lien_recrutment TEXT,
        reponse_societe TEXT
    )
''')
conn.commit()

# Interface utilisateur avec Tkinter
fenetre = Tk()
fenetre.title("Gestion des Recherches de Stages")

# Label pour afficher l'heure actuelle
label_heure = Label(fenetre, text="", font=("Helvetica", 12))
label_heure.grid(row=7, column=0, columnspan=2)
mettre_a_jour_heure()  # Appeler la fonction pour mettre à jour l'heure

# Labels et Entry pour saisir les informations
#Label(fenetre, text="Date de Candidature (DD-MM-YYYY):").grid(row=0, column=0)
#entry_date_candidature = Entry(fenetre)
#entry_date_candidature.grid(row=0, column=1)

# ... (Le reste du code reste inchangé)

# Listbox pour afficher les recherches sauvegardées
listbox_recherches = Listbox(fenetre, height=10, width=60)
listbox_recherches.grid(row=8, column=0, columnspan=2)
mettre_a_jour_listbox()

# Bouton pour ajouter une recherche
Button(fenetre, text="Ajouter une recherche", command=afficher_fenetre_ajout_recherche).grid(row=6, column=0, columnspan=2)

# ... (Le reste du code reste inchangé)

fenetre.mainloop()

# Fermer la connexion à la base de données
conn.close()
