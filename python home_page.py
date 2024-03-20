import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import widgets

import einleitung
import browser
import batterie
import EV_auto  
import ladestation
import energie
import sale

# Definieren der Seiten
pages = {
    "1. Einleitung": einleitung,
    "2. Verkauf": sale,
    "3. Energie": energie,
    "4. Ladestationen": ladestation,
    "5. Elektroautos": EV_auto,  
    "6. Elektroauto-Browser": browser,
}

# Einrichten der Seitenleiste
st.sidebar.title("Ära der Elektroautos: Analyse, Trends und Zukunft der Mobilität")
select = st.sidebar.radio("Bitte wählen Sie eine Ansicht aus:", list(pages.keys()))

# Überprüfung der Auswahl der Seite 'Elektroautos' und zusätzliche Optionen
if select == "5. Elektroautos":
    additional_option = st.sidebar.radio("Weitere Optionen:", ["Elektroauto", "Batterie"])
    if additional_option == "Elektroauto":
        # Code zur Anzeige von Elektroauto
        EV_auto.app()  # Aufruf der Funktion app() aus dem Modul 'EV_auto' zur Anzeige von Elektroauto
    elif additional_option == "Batterie":
        # Code zur Anzeige von Batteriedaten
        batterie.app()  # Aufruf der Funktion app() aus dem Modul 'batterie' zur Anzeige von Batteriedaten
    else:
        pages[select].app()  # Wenn der Benutzer eine andere Option auswählt, wird die ausgewählte Seite angezeigt
else:
    pages[select].app()  # Wenn der Benutzer eine andere Seite auswählt, wird die ausgewählte Seite angezeigt
