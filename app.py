import streamlit as st
import json
from datetime import datetime

# File to store patient data
PATIENTS_FILE = "patients.json"

# Load or initialize patient data
def load_patients():
    try:
        with open(PATIENTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_patients(data):
    with open(PATIENTS_FILE, "w") as f:
        json.dump(data, f, default=str)

# Initialize patient data
patients = load_patients()

# Sidebar menu
menu = ["Accueil", "Créer un patient", "Dossier Patient"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Accueil":
    st.title("Gestion des Patients")
    search = st.text_input("Rechercher un patient (Nom, Prénom, Date de Naissance)")
    results = []
    if search:
        for patient_id, patient in patients.items():
            if (
                search.lower() in patient["nom"].lower()
                or search.lower() in patient["prenom"].lower()
                or search in patient["date_naissance"]
            ):
                results.append((patient_id, patient))
        if results:
            for patient_id, patient in results:
                st.write(f"ID: {patient_id} - {patient['nom']} {patient['prenom']} (Né(e) le {patient['date_naissance']})")
        else:
            st.write("Aucun patient correspondant trouvé.")
    else:
        st.write("Entrez un critère pour rechercher un patient.")

elif choice == "Créer un patient":
    st.title("Créer un nouveau patient")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_naissance = st.date_input("Date de Naissance")
    statut = st.selectbox("Statut ménopausique", ["Non", "Oui"])
    antecedents = st.text_area("Antécédents médicaux")
    if st.button("Enregistrer"):
        patient_id = str(len(patients) + 1)
        patients[patient_id] = {
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance.isoformat(),
            "statut": statut,
            "antecedents": antecedents,
            "consultations": [],
        }
        save_patients(patients)
        st.success(f"Patient {nom} {prenom} ajouté avec succès !")

elif choice == "Dossier Patient":
    st.title("Dossier Patient")
    patient_id = st.text_input("ID du patient")
    if st.button("Afficher Dossier"):
        if patient_id in patients:
            patient = patients[patient_id]
            st.write(f"Nom : {patient['nom']}")
            st.write(f"Prénom : {patient['prenom']}")
            st.write(f"Date de naissance : {patient['date_naissance']}")
            st.write(f"Statut ménopausique : {patient['statut']}")
            st.write(f"Antécédents médicaux : {patient['antecedents']}")
            st.write("Consultations :")
            if patient["consultations"]:
                for consultation in patient["consultations"]:
                    st.write(f"- {consultation['date']} : {consultation['text']}")
            else:
                st.write("Aucune consultation enregistrée.")
            
            # Add a new consultation
            st.subheader("Ajouter une nouvelle consultation")
            new_consultation = st.text_area("Détails de la consultation")
            if st.button("Valider Consultation"):
                if new_consultation.strip():
                    # Add consultation and save immediately
                    patients[patient_id]["consultations"].append({
                        "date": datetime.now().strftime("%d %B %Y"),
                        "text": new_consultation
                    })
                    save_patients(patients)
                    st.success("Consultation ajoutée avec succès !")
                    # Refresh the page to show the updated consultations
                    st.experimental_rerun()
                else:
                    st.error("Le champ de consultation ne peut pas être vide.")
        else:
            st.error("ID du patient non trouvé.")
