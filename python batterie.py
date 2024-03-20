import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_and_prepare_data(filepath):
    data = pd.read_excel(filepath)
    data['Max_DC_Ladeleist'] = data['Ladeleist'].str.extract('DC:(\d+,\d+|\d+)').replace(',', '.', regex=True).astype(float)
    data['WLTP_komb_kWh100km'] = data['WLTP_komb'].str.replace(' kWh/100 km', '').str.replace(',', '.').astype(float)
    data['Efficiency_km_per_kWh'] = data['Reichw_E_wert'] / data['AntriebsbatterieKapazitaetNettoKwh']
    
    # Extrahiere Marke und Modell aus 'Fahrzeug'
    data['Brand'] = data['Fahrzeug'].apply(lambda x: x.split()[0])
    data['Model'] = data['Fahrzeug'].apply(lambda x: ' '.join(x.split()[1:]))
    
    return data

def visualize_data(data):
    
    # Verteilung der maximalen Ladeleistung (Gleichstrom)
    st.header("Die Verteilung der maximalen Ladeleistung (Gleichstrom)")
    st.write("""
        Die Analyse zeigt die Verteilung der maximalen Ladeleistung von Gleichstrom (DC) unter Elektrofahrzeugen. Die Ladeleistung ist ein entscheidender Faktor, 
        der die Geschwindigkeit des Aufladens der Batterie eines Elektrofahrzeugs beeinflusst.
    """)
    plot_max_dc_charging_power(data)

    # Beziehung zwischen Batteriekapazität und Fahrzeugreichweite
    st.header("Die Beziehung zwischen Batteriekapazität und Fahrzeugreichweite")
    st.write("""
        Diese Analyse zeigt, wie sich die Brutto- und Nettokapazität der Batterie auf die Reichweite von Elektrofahrzeugen auswirken. 
        Größere Batteriekapazitäten ermöglichen in der Regel eine größere Reichweite, was entscheidend für die Praktikabilität von Elektrofahrzeugen ist.
    """)
    plot_battery_capacity_vs_range(data)

    # Verteilung des Energieverbrauchs von Fahrzeugen gemäß dem WLTP-Standard
    st.header("Die Verteilung des Energieverbrauchs von Fahrzeugen gemäß dem WLTP-Standard")
    st.write("""
    Dieses Diagramm zeigt den Energieverbrauch des Fahrzeugs gemäß dem WLTP-Standard.
    Ein niedriger Energieverbrauch pro 100 km deutet auf eine höhere Energieeffizienz des Fahrzeugs hin.
    """)
    plot_energy_consumption_wltp(data)

    # Kategorisierung von Elektrofahrzeugen nach Leistung und Reichweite
    st.header("Die Kategorisierung von Elektrofahrzeugen nach Leistung und Reichweite")
    st.write("""
        Die Kategorisierung von Fahrzeugen nach ihrer Leistung und Reichweite ermöglicht die Identifizierung verschiedener Leistungssegmente je 
        nach Kombination von Leistung und Reichweite, was zur Segmentierung von Fahrzeugen entsprechend ihrer Leistung führt.
    """)
    plot_vehicle_segmentation(data)

def plot_max_dc_charging_power(data):
    plt.figure(figsize=(12, 6))
    sns.histplot(data['Max_DC_Ladeleist'].dropna(), bins=30, kde=True, color='orange')
    plt.title('Die Verteilung der maximalen Ladeleistung (Gleichstrom)')
    plt.xlabel('Die maximale Ladeleistung (kW)')
    plt.ylabel('Die Anzahl der Fahrzeuge')
    plt.grid(True)
    st.pyplot(plt)

def plot_battery_capacity_vs_range(data):
    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)
    sns.scatterplot(x='AntriebsbatterieKapazitaetBruttoKwh', y='Reichw_E_wert', data=data, color='blue', alpha=0.5)
    plt.title('Das Verhältnis zwischen der Bruttokapazität der Batterie und der Reichweite')
    plt.xlabel('Brutto-Batteriekapazität (kWh)')
    plt.ylabel('Die Reichweite des Fahrzeugs (km)')
    
    plt.subplot(1, 2, 2)
    sns.scatterplot(x='AntriebsbatterieKapazitaetNettoKwh', y='Reichw_E_wert', data=data, color='red', alpha=0.5)
    plt.title('Der Zusammenhang zwischen der Nettobatteriekapazität und der Reichweite')
    plt.xlabel('Netto Batteriekapazität (kWh)')
    plt.ylabel('Die Reichweite des Fahrzeugs (km)')
    plt.tight_layout()
    st.pyplot(plt)

def plot_energy_consumption_wltp(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['WLTP_komb_kWh100km'].dropna(), bins=30, kde=True, color='purple')
    plt.title('Die Verteilung des Energieverbrauchs von Fahrzeugen gemäß dem WLTP-Standard')
    plt.xlabel('Energieverbrauch (kWh/100 km)')
    plt.ylabel('Die Anzahl der Fahrzeuge')
    plt.grid(True)
    st.pyplot(plt)

def plot_vehicle_segmentation(data):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Reichw_E_wert', y='LeistungKW', data=data, alpha=0.6, edgecolor=None)
    plt.title('Die Kategorisierung von Elektrofahrzeugen nach Leistung und Reichweite')
    plt.xlabel('Reichweite (km)')
    plt.ylabel('Die Leistung (kW)')
    plt.grid(True)
    st.pyplot(plt)

def calculate_and_display_averages(data):
    st.subheader("Durchschnittswerte")
    avg_brutto_kapacitet = data['AntriebsbatterieKapazitaetBruttoKwh'].mean()
    avg_netto_kapacitet = data['AntriebsbatterieKapazitaetNettoKwh'].mean()
    avg_wltp_komb = data['WLTP_komb_kWh100km'].mean()

    st.write(f"Durchschnittliche Brutto-Batteriekapazität: {avg_netto_kapacitet:.2f} kWh")
    st.write(f"Durchschnittliche Nettokapazität der Batterie: {avg_brutto_kapacitet:.2f} kWh")
    st.write(f"Durchschnittlicher Energieverbrauch (WLTP kombiniert): {avg_wltp_komb:.2f} kWh/100 km

def app():
    st.sidebar.header("Die Analyse von Elektrofahrzeugen")
    filepath = "xxxxxxxx.xls"  
    data = load_and_prepare_data(filepath)
    visualize_data(data)
    calculate_and_display_averages(data)

if __name__ == "__main__":
    app()

