import streamlit as st
import pandas as pd
import plotly.express as px


# Laden der Daten
data = pd.read_excel("ElectricCarData_Norm_SortedII.xlsx")
# Umwandeln der 'Reichweite'-Spalte von String in numerischen Wert
data['Range'] = data['Range'].str.replace(' km', '').astype(int)

def app():
    st.title('Der Elektroauto-Browser')

    # Hinzufügen von Filtern
    price_filter = st.sidebar.slider('Filtern nach Preis (Euro):', int(data['PriceEuro'].min()), int(data['PriceEuro'].max()), (int(data['PriceEuro'].min()), int(data['PriceEuro'].max())))
    range_filter = st.sidebar.slider('Filtern nach Reichweite (km):', 0, int(data['Range'].max()), (0, int(data['Range'].max())))
    seats_filter = st.sidebar.slider('Filtern nach Anzahl der Sitze:', int(data['Seats'].min()), int(data['Seats'].max()), (int(data['Seats'].min()), int(data['Seats'].max())))
    body_style = st.sidebar.multiselect('Wählen Sie den Karosseriestil:', options=data['BodyStyle'].unique())
    power_train = st.sidebar.multiselect('Wählen Sie den Antrieb:', options=data['PowerTrain'].unique())
    rapid_charge = st.sidebar.checkbox('Schnellladung möglich?')

    # Filtern der Daten
    data_filtered = data[(data['PriceEuro'] >= price_filter[0]) & (data['PriceEuro'] <= price_filter[1]) &
                         (data['Range'] >= range_filter[0]) &
                         (data['Range'] <= range_filter[1]) &
                         (data['Seats'] >= seats_filter[0]) & (data['Seats'] <= seats_filter[1])]
    if body_style:
        data_filtered = data_filtered[data_filtered['BodyStyle'].isin(body_style)]
    if power_train:
        data_filtered = data_filtered[data_filtered['PowerTrain'].isin(power_train)]
    if rapid_charge:
        data_filtered = data_filtered[data_filtered['RapidCharge'] == 'Rapid charging possible']

    search_clicked = st.sidebar.button('Search')

    if search_clicked:
        # Anzeige der gefilterten Daten
        st.write(f"Gefundene Fahrzeuge: {len(data_filtered)}")
        st.dataframe(data_filtered)

    # Interaktive Visualisierung der Daten mit Plotly
    if not data_filtered.empty:
        fig = px.scatter(data_filtered, x='PriceEuro', y='Range', color='Brand', hover_data=['Model'], title="Interaktiver Scatter Plot: Preis vs. Reichweite")
        st.plotly_chart(fig)

    # Initialisierung der Variablen model_selection
    model_selection = 'Bitte wählen'
    
    # Ermöglichen der Auswahl von Marke und dann Modell für detailliertere Ansicht
    if not data_filtered.empty:
        brand_selection = st.selectbox('Wählen Sie eine Marke:', ['Bitte wählen'] + sorted(data_filtered['Brand'].unique()))
        if brand_selection != 'Bitte wählen':
            models_for_brand = sorted(data_filtered[data_filtered['Brand'] == brand_selection]['Model'].unique())
            model_selection = st.selectbox('Wählen Sie ein Modell für mehr Details:', ['Bitte wählen'] + models_for_brand)
            if model_selection != 'Bitte wählen':
                selected_model_details = data_filtered[data_filtered['Model'] == model_selection]
                st.write(selected_model_details)

    # Hinzufügen von personalisierten Empfehlungen
    if model_selection != 'Bitte wählen':
        st.subheader('Empfohlene Modelle:')
        similar_models = data[(data['Range'] <= selected_model_details['Range'].iloc[0] + 50) & 
                              (data['Range'] >= selected_model_details['Range'].iloc[0] - 50) &
                              (data['PriceEuro'] <= selected_model_details['PriceEuro'].iloc[0] + 5000) &
                              (data['PriceEuro'] >= selected_model_details['PriceEuro'].iloc[0] - 5000) &
                              (data['Model'] != model_selection)]
        if not similar_models.empty:
            for _, row in similar_models.iterrows():
                st.text(f"{row['Brand']} {row['Model']} - Reichweite: {row['Range']}km, Preis: €{row['PriceEuro']}")
        else:
            st.text("Nicht ähnliche Modelle zur Empfehlung vorhanden.")

if __name__ == "__main__":
    app()
