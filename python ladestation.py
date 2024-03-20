import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Laden und Vorbereiten der Daten
@st.cache_data
def load_data():
    # Laden historischer Ladedaten
    historical_data_path = 'IEA-EV-dataEV charging pointsHistoricalEV (1).csv'
    historical_data = pd.read_csv(historical_data_path)
    
    # Laden von Prognosedaten für Ladesäulen
    projection_data_path = 'IEA-EV-dataEV charging pointsProjection-STEPSEV.csv'
    projection_data = pd.read_csv(projection_data_path)
    
    # Laden von EV-Verkaufsdaten
    sales_data_path = 'EV data history.csv'
    sales_data = pd.read_csv(sales_data_path)
    
    # Kombinieren und Filtern von historischen und prognostizierten Daten
    combined_data = pd.concat([historical_data, projection_data])
    filtered_data = combined_data[combined_data['year'] >= 2010]
    
    # Aggregieren von globalen und länderspezifischen Daten
    global_data = filtered_data.groupby(['year']).sum().reset_index()
    country_data = filtered_data.groupby(['region', 'year']).sum().reset_index()
    
    # Filtern und Aggregieren von EV-Verkaufsdaten
    sales_data_filtered = sales_data[(sales_data['parameter'] == 'EV sales') & (sales_data['year'] >= 2010)]
    sales_aggregated = sales_data_filtered.groupby(['region', 'year']).sum().reset_index()
    
    # Verknüpfen von EV-Verkäufen und Anzahl der Ladegeräte
    combined_sales_chargers = pd.merge(sales_aggregated, country_data, on=['region', 'year'], suffixes=('_sales', '_chargers'))
    
    return global_data, country_data, combined_sales_chargers

def app():
    global_data, country_data, combined_sales_chargers = load_data()

    # Visualisierungen und Interaktivität
    st.title('Analyse und Visualisierung von Elektrofahrzeug-Ladegeräten (EV) und EV-Verkäufen')

    # Globaler Trend der Ladestationen
    st.header('Globaler Trend der Anzahl von Ladestationen für Elektrofahrzeuge seit 2010.')
    fig_global = px.line(global_data, x='year', y='value', title='Globale Anzahl von Ladestationen für Elektrofahrzeuge im Laufe der Jahre')
    st.plotly_chart(fig_global)

    # Interaktive Darstellung nach Ländern für Ladestationen
    st.header('Die Anzahl von Ladestationen für Elektrofahrzeuge nach Ländern')
    selected_country = st.selectbox('Bitte wählen Sie ein Land aus:', country_data['region'].unique())
    filtered_country_data = country_data[country_data['region'] == selected_country]
    fig_country = px.line(filtered_country_data, x='year', y='value', title=f'Anzahl der Ladestationen für Elektrofahrzeuge in {selected_country} im Laufe der Jahre')
    st.plotly_chart(fig_country)

    # Analyse der Korrelation zwischen EV-Verkäufen und Ladestationen
    st.header('Die Korrelation zwischen dem Verkauf von Elektrofahrzeugen und der Anzahl der Ladestationen')
    correlation_matrix = combined_sales_chargers[['value_sales', 'value_chargers']].corr()
    correlation_value = correlation_matrix.loc['value_sales', 'value_chargers']
    fig_correlation = px.scatter(combined_sales_chargers, x='value_chargers', y='value_sales', 
                                 trendline='ols', 
                                 labels={'value_chargers': 'Die Ladegeräteanzahl', 'value_sales': 'Verkauf von EV'},
                                 title=f'Die Korrelation zwischen dem Verkauf von Elektrofahrzeugen und der Anzahl der Ladestationen (Pearson: {correlation_value:.2f})')
    st.plotly_chart(fig_correlation)

if __name__ == '__main__':
    app()
