import streamlit as st
import pandas as pd
import plotly.express as px

# Laden und Vorbereiten der Daten
file_path = 'ElectricCarData_Norm_Sorted.xlsx'
data = pd.read_excel(file_path)

# Konvertierung von Strings in numerische Werte
data['Range_km'] = data['Range'].str.replace(' km', '').astype(int)
data['TopSpeed_kmh'] = data['TopSpeed'].str.replace(' km/h', '').astype(int)
data['Accel_sec'] = data['Accel'].str.replace(' sec', '').astype(float)
data['Efficiency_Wh_km'] = data['Efficiency'].str.replace(' Wh/km', '').astype(float)
data['FastCharge_km/h'] = pd.to_numeric(data['FastCharge'].str.extract('(\d+)')[0], downcast='float', errors='coerce').fillna(0)

# Hinzufügen von Funktionen für die Visualisierung
def plot_powertrain_distribution(data):
    st.write("""
    Visualisierung der Verteilung von Fahrzeugantrieben.
    Diese Grafik zeigt die Anzahl der Fahrzeuge pro Antriebstyp, was dabei helfen kann, die Beliebtheit verschiedener Antriebstechnologien zu verstehen.
    """)
    # Anpassung für korrekte Benennung der Spalten
    powertrain_count = data['PowerTrain'].value_counts().reset_index(name='count')
    powertrain_count.columns = ['Antriebssysteme', 'Anzahl der Fahrzeuge']  # Umbenennung der Spalten für Klarheit

    fig = px.bar(powertrain_count, x='Antriebssysteme', y='Anzahl der Fahrzeuge', title='Verteilung der Antriebssysteme')
    st.plotly_chart(fig)

def plot_body_style_pricing(data):
    st.write("""
    Visualisierung der durchschnittlichen Fahrzeugpreise nach Karosseriestil.
    Diese Grafik gibt Einblicke in die bevorzugten Karosseriestile von Herstellern in verschiedenen Preiskategorien, was Verbrauchern bei Kaufentscheidungen helfen kann.
    """)
    fig = px.bar(data.groupby('BodyStyle')['PriceEuro'].mean().reset_index(), x='BodyStyle', y='PriceEuro', title='Durchschnittspreise nach Karosseriestil')
    st.plotly_chart(fig)

def plot_price_vs_performance(data):
    st.write("""
    Der Graph zeigt, wie der Preis, die Beschleunigung, die Höchstgeschwindigkeit und die Reichweite in Fahrzeugen miteinander verbunden sind. 
    Dies gibt uns eine Vorstellung davon, welche Leistung Kunden für ihr investiertes Geld erwarten können.
    """)
    # Anzeige der Korrelationsmatrix mit unterschiedlichen Farben
    fig = px.imshow(data[['PriceEuro', 'Accel_sec', 'TopSpeed_kmh', 'Range_km']].corr(), 
                    text_auto=True, title='Verbindung zwischen Preis, Leistung, Höchstgeschwindigkeit, Reichweite',
                    color_continuous_scale=['red', 'green'])  # Rot für negative Korrelation, Grün für positive
    st.plotly_chart(fig)

def plot_fast_charging_capabilities(data):
    st.write("""
    Analyse der Schnellladekapazität in Bezug auf die Reichweite des Fahrzeugs.
    Dieser Streudiagramm zeigt Fahrzeuge mit ihrer Reichweite und Ladekapazität und hebt Modelle hervor, 
    die schnelles Laden mit großer Reichweite bieten, was für die Langzeitpraktikabilität von Elektrofahrzeugen entscheidend ist.
    """)
    fig = px.scatter(data, x='Range_km', y='FastCharge_km/h', color='Brand', hover_data=['Model'], title='Lademöglichkeiten im Vergleich zur Reichweite')
    st.plotly_chart(fig)

def plot_top_models_by_feature(data, feature, top_n=10):
    st.write(f"Top {top_n} Modelle nach {feature}")
    # Für Beschleunigung möchten wir die niedrigsten Werte oben haben, für andere Merkmale die höchsten
    ascending = True if feature == 'Accel_sec' else False
    sorted_data = data.sort_values(by=feature, ascending=ascending).head(top_n)
    fig = px.bar(sorted_data, x='Model', y=feature, color='Brand', text=feature,
                 title=f"Top {top_n} Modelle nach {feature}")
    st.plotly_chart(fig)

# Haupt-Streamlit-Anwendung
def app():
    st.title('Analyse der verfügbaren Elektrofahrzeuge auf dem Markt')

    # Hinzufügen einer Auswahl für Analysen
    analysis_options = {
        'Verteilung der Antriebssysteme': plot_powertrain_distribution,
        'Durchschnittspreise pro Karosseriestil': plot_body_style_pricing,
        'Verbindung zwischen Preis und Leistung': plot_price_vs_performance,
        'Lademöglichkeiten im Vergleich zur Reichweite': plot_fast_charging_capabilities
    }

    option = st.selectbox('Wählen Sie eine Analyse aus:', list(analysis_options.keys()))

    # Aufrufen der ausgewählten Analyse
    analysis_function = analysis_options[option]
    analysis_function(data)

    st.title('Top-Modelle Elektrofahrzeuge nach Schlüsselfunktionen')

    feature_selection = st.selectbox('Wählen Sie eine Funktion aus:',
                                     ['Range_km', 'FastCharge_km/h', 'PriceEuro', 'Efficiency_Wh_km', 'Accel_sec'])
    
    top_n_selection = st.slider('Bitte wählen Sie die Anzahl der Top-Modelle zur Anzeige aus:', min_value=3, max_value=20, value=10)

    # Anpassung des Titels für verschiedene Funktionen
    if feature_selection == 'Accel_sec':
        st.write("Analyse von Modellen mit der besten Beschleunigung (je niedriger, desto besser)")
    else:
        st.write(f"Analyse führender Modelle basierend auf {feature_selection}")

    plot_top_models_by_feature(data, feature_selection, top_n=top_n_selection)


if __name__ == '__main__':
    app()
