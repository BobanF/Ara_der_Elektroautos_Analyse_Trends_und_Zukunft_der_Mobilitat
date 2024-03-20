import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def app():
    st.title("Analyse der Auswirkungen von Elektrofahrzeugen auf den Stromverbrauch")
    
    # Laden der Daten
    original_data_path = 'IEA-EV-dataElectricity demandProjection-STEPSCars.csv'
    new_data_path = 'IEA-EV-dataElectricity demandHistoricalCars (1).csv'
    
    original_data = pd.read_csv(original_data_path)
    new_data = pd.read_csv(new_data_path)

    # Einführungstext
    st.write("""
    Diese Analyse zeigt die Auswirkungen von Elektrofahrzeugen (EVs) auf den Stromverbrauch. Die Übersicht zeigt, wie das Wachstum der EV-Bestände den Energiesektor beeinflusst und wie verschiedene Regionen sich an die sich ändernden Energiebedürfnisse anpassen.
         """)

    # Filtern und Vorbereiten der Daten
    electricity_demand = original_data[original_data['parameter'] == "Electricity demand"].copy()
    ev_stock = new_data[new_data['parameter'] == "EV stock"].copy()

    electricity_demand_relevant = electricity_demand[['region', 'year', 'value']].rename(columns={'value': 'electricity_demand'})
    ev_stock_relevant = ev_stock[['region', 'year', 'value']].rename(columns={'value': 'ev_stock'})

    # Zusammenführen und Aggregieren der Daten
    merged_data = pd.merge(electricity_demand_relevant, ev_stock_relevant, on=['region', 'year'], how='inner')
    merged_data_aggregated = merged_data.groupby(['region', 'year']).agg({'electricity_demand': 'mean', 'ev_stock': 'sum'}).reset_index()

    # Visualisierung der Korrelation mit Plotly
    fig = px.scatter(merged_data_aggregated, x='ev_stock', y='electricity_demand',
                     trendline="ols",
                     title="Die Korrelation zwischen dem Anstieg des EV-Verkaufs und dem Verbrauch von elektrischer Energie")
    fig.update_layout(xaxis_title="Verkauf von Elektrofahrzeugen", yaxis_title="Der Stromverbrauch (GWh)")
    st.plotly_chart(fig)

    # Vorbereiten der Daten für weitere Visualisierungen
    electricity_demand = original_data[original_data['parameter'] == "Electricity demand"].copy()
    electricity_demand['value'] = pd.to_numeric(electricity_demand['value'], errors='coerce')
    electricity_demand_trends = electricity_demand.pivot_table(index='year', columns='region', values='value', aggfunc='sum').reset_index()

    # Visualisierung der Stromnachfrage-Trends mit Plotly
    st.write("## Jährliches Wachstum der Nachfrage nach elektrischer Energie nach Regionen.")
    fig = px.line(electricity_demand_trends, x='year', y=electricity_demand_trends.columns[1:], 
                  title="Jährliches Wachstum der Nachfrage nach elektrischer Energie nach Regionen",
                  labels={'value': 'Der Stromverbrauch (GWh)', 'year': 'Jahr'})
    fig.update_layout(xaxis_title="Jahr", yaxis_title="Der Stromverbrauch (GWh)", legend_title="Region")
    st.plotly_chart(fig)

    # Fazit und Implikationen
    st.write("""
    Abschließend hat das Wachstum des EV-Verkaufs einen signifikanten Einfluss auf den Stromverbrauch. Energienetze müssen sich weiterentwickeln, um diesen Trend zu unterstützen. 
    Es besteht ein klarer Bedarf an nachhaltigen Lösungen und Politiken, die die Integration von EV in unsere Gesellschaft fördern.
    """)

if __name__ == "__main__":
    app()
