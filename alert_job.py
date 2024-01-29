from tkinter import ttk
import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, Listbox, END, Toplevel, IntVar, Checkbutton
from datetime import datetime
#from tabulate import tabulate

titres = ["ID", "Date de Candidature", "Nom Société", "Téléphone", "Réponse Société", "+"]

# Fonction pour ajouter une recherche de stage
def ajouter_recherche():
    date_candidature = datetime.now().strftime('%d-%m-%Y %H:%M')
    cv_envoyes = cv_var.get()
    lettre_envoyes = lettre_var.get()
    nom_societe = entry_nom_societe.get()
    telephone = entry_telephone.get()
    lien_recrutement = entry_lien_recrutement.get()

    # Ajouter la recherche dans la base de données
    cursor.execute('''
        INSERT INTO recherches_stages (date_candidature, nom_societe, telephone,  reponse_societe, lien_recrutement, cv_envoyes, lettre_envoyes,)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date_candidature,nom_societe, telephone, lien_recrutement,  cv_envoyes, lettre_envoyes, None))
    conn.commit()
    messagebox.showinfo("Succès", "Recherche de stage ajoutée avec succès")
    mettre_a_jour_listbox()  # Mettre à jour la liste après l'ajout

def mettre_a_jour_treeview():
    treeview_recherches.delete(*treeview_recherches.get_children())
    try:
        cursor.execute('SELECT * FROM recherches_stages')
        resultats = cursor.fetchall()

        treeview_recherches['columns'] = titres[:-1]  # Enlève le "+" de la dernière colonne
        for titre in titres:
            if titre == "+":
                continue  # Ne configure pas de colonne pour le bouton "+"
            treeview_recherches.heading(titre, text=titre, anchor='center')
            treeview_recherches.column(titre, anchor='center', width=150)  # Ajustez la largeur selon vos besoins

        for resultat in resultats:
            treeview_recherches.insert('', 'end', values=resultat)  # Ajoute une cellule vide pour le bouton "+"

        # Configure le bouton "+" pour chaque élément
        for item_id in treeview_recherches.get_children():
            treeview_recherches.item(item_id, tags=(item_id,))  # Associe l'identifiant de l'élément comme tag
            treeview_recherches.tag_bind(item_id, '<ButtonRelease-1>', lambda event, item_id=item_id: afficher_infos_completes(item_id))

    except sqlite3.OperationalError as e:
        print(f"Erreur SQL: {e}")

fenetre_info = None


# Fonction pour afficher les informations complètes lors du clic sur le bouton "+"
def afficher_infos_completes(item_id):
    global fenetre_info
    global nouvelles_valeurs_globale

    nouvelles_valeurs_globale = None

    if item_id not in treeview_recherches.get_children():
        return

    item_values = treeview_recherches.item(item_id, 'values')

    # Affiche les informations complètes dans une nouvelle fenêtre
    fenetre_info = Toplevel(fenetre)
    fenetre_info.title("Informations Complètes")
    nouvelles_valeurs = []

    # Labels et Entry pour afficher et modifier les informations
    for i, titre in enumerate(titres[:-1]):
        label = Label(fenetre_info, text=f"{titre}:", anchor='w')
        label.grid(row=i, column=0, sticky='w')

        # Champ Entry pour modification
        valeur_actuelle = item_values[i]
        entry_modification = Entry(fenetre_info)
        entry_modification.insert(END, valeur_actuelle)
        entry_modification.grid(row=i, column=1, sticky='w')

        nouvelles_valeurs.append(entry_modification)

    # Bouton "Modifier"
    Button(fenetre_info, text="Modifier", command=lambda item_id=item_id, valeurs=nouvelles_valeurs: modifier_recherche(item_id)).grid(row=len(titres)-1, column=0, sticky='w')


    nouvelles_valeurs_globale = nouvelles_valeurs

# Fonction pour gérer la modification des informations
def modifier_recherche(item_id):
    global nouvelles_valeurs_globale 

    item_id = int(item_id[1:])

# Vérifier si l'élément existe dans la liste des enfants
    if item_id not in [int(treeview_recherches.item(child)['text'][1:]) for child in treeview_recherches.get_children()]:
        messagebox.showerror("Erreur", "L'élément n'existe pas.")
        return

    try:
        cursor.execute('''
            UPDATE recherches_stages
            SET date_candidature=?, nom_societe=?, telephone=?, reponse_societe=?, lien_recrutement=?, cv_envoyes=?, lettre_envoyes=?
            WHERE id=?
        ''', (
            nouvelles_valeurs_globale[0].get(),
            nouvelles_valeurs_globale[1].get(), 
            nouvelles_valeurs_globale[2].get(), 
            nouvelles_valeurs_globale[3].get(), 
            nouvelles_valeurs_globale[4].get(), 
            nouvelles_valeurs_globale[5].get(), 
            nouvelles_valeurs_globale[6].get() if len(nouvelles_valeurs_globale) > 5 else '',
            item_id
            ))
        conn.commit()
        messagebox.showinfo("Succès", "Informations modifiées avec succès !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")

    # Configure le bouton "+" pour chaque élément
    for item_id in treeview_recherches.get_children():
        treeview_recherches.item(item_id, tags=(item_id,))  # Associe l'identifiant de l'élément comme tag
        treeview_recherches.tag_bind(item_id, '<ButtonRelease-1>', lambda event, item_id=item_id: afficher_infos_completes(item_id, originales_valeurs_globale))

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

    Label(fenetre_ajout, text="Téléphone:").grid(row=3, column=0)
    entry_telephone = Entry(fenetre_ajout)
    entry_telephone.grid(row=3, column=1)

    Label(fenetre_ajout, text="Nom de la Société:").grid(row=4, column=0)
    entry_nom_societe_ajout = Entry(fenetre_ajout)
    entry_nom_societe_ajout.grid(row=4, column=1)

    Label(fenetre_ajout, text="Lien de Recrutement:").grid(row=5, column=0)
    entry_lien_recrutement_ajout = Entry(fenetre_ajout)
    entry_lien_recrutement_ajout.grid(row=5, column=1)

    Label(fenetre_ajout, text="CV envoyés:").grid(row=1, column=0)
    cv_var = IntVar()
    Checkbutton(fenetre_ajout, variable=cv_var, text="Oui").grid(row=1, column=1)

    Label(fenetre_ajout, text="Lettre envoyés:").grid(row=2, column=0)
    lettre_var = IntVar()
    Checkbutton(fenetre_ajout, variable=lettre_var, text="Oui").grid(row=2, column=1)

    # Bouton pour ajouter la recherche depuis la fenêtre d'ajout
    Button(fenetre_ajout, text="Enregistrer", command=lambda: ajouter_recherche_from_window(
        fenetre_ajout,
        entry_nom_societe_ajout.get(),
        entry_telephone.get(),
        entry_lien_recrutement_ajout.get(),
        cv_var,
        lettre_var
    )).grid(row=7, column=0, columnspan=2)

# Fonction pour ajouter une recherche depuis la fenêtre d'ajout
def ajouter_recherche_from_window(fenetre_ajout, nom_societe, telephone, lien_recrutement,  cv_var, lettre_var):
    date_candidature = datetime.now().strftime('%d-%m-%Y %H:%M')

    cv = "Oui" if cv_var.get() == 1 else "Non"
    lettre = "Oui" if lettre_var.get() == 1 else "Non"

    cursor.execute('''
        INSERT INTO recherches_stages (date_candidature, nom_societe, telephone, reponse_societe, lien_recrutement, cv_envoyes, lettre_envoyes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date_candidature, nom_societe, telephone, None, cv, lettre, lien_recrutement))
    conn.commit()
    messagebox.showinfo("Succès", "Recherche de stage ajoutée avec succès")
    mettre_a_jour_treeview()  # Mettre à jour la Treeview après l'ajout
    fenetre_ajout.destroy()  # Fermer la fenêtre d'ajout

# Création d'une base de données SQLite
conn = sqlite3.connect('recherches_stages.db')
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recherches_stages (
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        date_candidature TEXT,
        nom_societe TEXT,
        telephone TEXT,
        reponse_societe TEXT,
        lien_recrutement TEXT,
        cv_envoyes TEXT,
        lettre_envoyes TEXT

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


# Listbox pour afficher les recherches sauvegardées
listbox_recherches = Listbox(fenetre, height=10, width=60)
listbox_recherches.grid(row=8, column=0, columnspan=2)

# Bouton pour ajouter une recherche
Button(fenetre, text="Ajouter une recherche", command=afficher_fenetre_ajout_recherche).grid(row=6, column=0, columnspan=2)

# Treeview pour afficher les recherches sauvegardées
treeview_recherches = ttk.Treeview(fenetre, height=10, columns=titres, show='headings')
treeview_recherches.grid(row=8, column=0, columnspan=2, sticky='nsew')

# Configuration de l'ascenseur vertical
scrollbar_vertical = ttk.Scrollbar(fenetre, orient="vertical", command=treeview_recherches.yview)
scrollbar_vertical.grid(row=8, column=2, sticky="ns")
treeview_recherches.configure(yscrollcommand=scrollbar_vertical.set)

# Configuration de l'ascenseur horizontal
scrollbar_horizontal = ttk.Scrollbar(fenetre, orient="horizontal", command=treeview_recherches.xview)
scrollbar_horizontal.grid(row=9, column=0, columnspan=2, sticky="ew")
treeview_recherches.configure(xscrollcommand=scrollbar_horizontal.set)

# Ajustement dynamique de la largeur des colonnes
for i, titre in enumerate(titres):
    treeview_recherches.heading(titre, text=titre, anchor='center')
    treeview_recherches.column(titre, anchor='center', width=150)  # Ajustez la largeur selon vos besoins

mettre_a_jour_treeview()

if fenetre_info:
    fenetre_info.destroy()

fenetre.mainloop()

# Fermer la connexion à la base de données
conn.close()
