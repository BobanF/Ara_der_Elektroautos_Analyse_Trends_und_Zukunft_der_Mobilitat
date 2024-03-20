import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor  
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    data = pd.read_csv("EV data history.csv")
    #data_wo_pop = pd.read_csv("world_population.csv")
    return data

def prepare_data(data):
    global_sales_data = data[(data['parameter'] == 'EV sales') & (data['region'] == 'World')]
    X = global_sales_data['year'].values.reshape(-1, 1)
    y = global_sales_data['value'].values
    return X, y

def train_linear_model_and_predict(X, y):
    model = LinearRegression()
    model.fit(X, y)
    future_years = np.array(range(int(X.min()), 2031)).reshape(-1, 1)
    predictions = model.predict(future_years)
    return future_years.flatten(), predictions

def train_random_forest_and_predict(X, y):  # Neue Funktion für Random Forest
    rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
    rf_model.fit(X, y)
    future_years = np.array(range(int(X.min()), 2031)).reshape(-1, 1)
    predictions_rf = rf_model.predict(future_years)
    return future_years.flatten(), predictions_rf

def plot_global_forecast(years, predictions_linear, predictions_rf):
    fig = go.Figure()
    
    # Füge Linien für Vorhersagen beider Modelle hinzu
    fig.add_trace(go.Scatter(x=years, y=predictions_linear, mode='lines + markers', name='Lineare Regression', marker=dict(color='red')))
    fig.add_trace(go.Scatter(x=years, y=predictions_rf, mode='lines + markers', name='Random Forest'))

    # Setze grundlegende Grafikelemente
    fig.update_layout(title='Die globale Prognose für den Verkauf von Elektrofahrzeugen bis 2030.',
                      xaxis_title='Jahr',
                      yaxis_title='Der Verkauf von Elektrofahrzeugen.',
                      legend_title='Modell')

    # Füge Bereichsschieberegler hinzu
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1J", step="year", stepmode="backward"),
                    dict(count=5, label="5J", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="linear"
        )
    )

    return fig


def plot_interactive_forecast_by_powertrain(data):
    # Filterung der Daten nur für 'EV sales'
    filtered_data = data[data['parameter'] == 'EV sales']

    # Initialisierung der Grafik
    fig = go.Figure()

    # Ermögliche Benutzern die Auswahl des Antriebstyps
    powertrains = ['BEV', 'PHEV']  # Annahme basierend auf verfügbaren Antriebstypen
    selected_powertrain = st.selectbox("Bitte wählen Sie den Antriebstyp aus:", ['Alle'] + powertrains)

    # Füge eine Linie für globale Daten hinzu, wenn 'Alle' ausgewählt ist
    if selected_powertrain == 'Alle':
        for powertrain in powertrains:
            pt_data = filtered_data[(filtered_data['region'] == 'World') & (filtered_data['powertrain'] == powertrain)]
            fig.add_trace(go.Scatter(x=pt_data['year'], y=pt_data['value'], name=powertrain,
                                     mode='lines+markers', line=dict(width=2)))

    # Füge Linien für ausgewählte Regionen und Antriebstypen hinzu
    else:
        filtered_data = filtered_data[filtered_data['powertrain'] == selected_powertrain]
        regions = filtered_data['region'].unique()
        for region in regions:
            region_data = filtered_data[filtered_data['region'] == region]
            fig.add_trace(go.Scatter(x=region_data['year'], y=region_data['value'], name=f"{region} - {selected_powertrain}",
                                     mode='lines+markers', line=dict(width=2), visible='legendonly'))

    # Aktualisiere das Layout des Diagramms
    fig.update_layout(
        title=f'Verkauf von Fahrzeugen nach Regionen und Antriebsart: {selected_powertrain}',
        xaxis_title='Jahr',
        yaxis_title='Verkauf von Fahrzeugen',
        legend_title='Die Region / Art des Antriebs',
        hovermode='x unified',
        template="plotly_white"
    )

    return fig


def plot_market_shares(data):
    # Definition von Interessensregionen
    regions_of_interest = ['World', 'China', 'USA', 'Europe', 'Germany']
    
    # Filterung von Daten für EV-Verkaufsanteil und EV-Bestandsanteil
    ev_sales_share = data[(data['parameter'] == 'EV sales share') & data['region'].isin(regions_of_interest)]
    ev_stock_share = data[(data['parameter'] == 'EV stock share') & data['region'].isin(regions_of_interest)]
    
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    # Festlegen von Farben/Regionen für bessere Visualisierung
    colors = {'World': 'black', 'China': 'red', 'USA': 'blue', 'Europe': 'green', 'Germany': 'orange'}
    
    # Diagramm für den EV-Verkaufsanteil
    for region in regions_of_interest:
        region_data = ev_sales_share[ev_sales_share['region'] == region]
        ax[0].plot(region_data['year'], region_data['value'], marker='o', linestyle='-', color=colors[region], label=region)
    ax[0].set_title('Prozentsatz der Verkäufe von EV')
    ax[0].set_xlabel('Jahr')
    ax[0].set_ylabel('Anteil (%)')
    ax[0].grid(True)
    ax[0].legend(title='Region')

    # Diagramm für den EV-Bestandsanteil
    for region in regions_of_interest:
        region_data = ev_stock_share[ev_stock_share['region'] == region]
        ax[1].plot(region_data['year'], region_data['value'], marker='o', linestyle='-', color=colors[region], label=region)
    ax[1].set_title('Anteil von EV am Gesamtverkauf')
    ax[1].set_xlabel('Jahr')
    ax[1].set_ylabel('Anteil (%)')
    ax[1].grid(True)
    ax[1].legend(title='Region')
    
    return fig


def app():
    data = load_data()
    X, y = prepare_data(data)
    
    st.write("## Marktanalyse für Elektrofahrzeuge")

    # Diagramme für Marktanteile
    fig1 = plot_market_shares(data)
    st.pyplot(fig1)
    
    # Interaktive Grafik des jährlichen Verkaufs von Elektrofahrzeugen nach Regionen
    st.write("## Der interaktive Graph der jährlichen Verkaufszahlen von Elektrofahrzeugen nach Regionen.")
    fig_interactive = plot_interactive_forecast_by_powertrain(data)
    st.plotly_chart(fig_interactive)
    st.write("""
    Das interaktive Diagramm erlaubt den Benutzern, den jährlichen Verkauf von Elektroautos genauer zu untersuchen, indem sie einen bestimmten Antriebstyp (BEV oder PHEV) wählen und die Verkaufstrends in verschiedenen Regionen vergleichen. Eine solche Analyse kann dabei helfen, wichtige Märkte für die Erweiterung und Entwicklung neuer Antriebstechnologien zu identifizieren.

    Asien führt den Weg: Asien, besonders China, dominiert derzeit den Elektromobilitätsmarkt mit einem Wert von 137,5 Milliarden USD im Jahr 2021, was etwa 49% des Gesamtmarktanteils entspricht. China allein verkaufte 2021 mehr Elektroautos (3,3 Millionen) als weltweit im Jahr 2020.

    Europa und die USA erleben starkes Wachstum: Auch Europa und die USA zeigen eine deutliche Zunahme bei der Akzeptanz und dem Verkauf von Elektroautos. Europa hat das Ziel, bis 2050 klimaneutral zu werden, und unterstützt Elektroautos stark auf politischer Ebene. Die USA schreiten dank technologischer Innovationen und politischer Unterstützung schnell voran.           
              
      """)
    
    
    # Lineares Modell und globale Vorhersage
    years_linear, predictions_linear = train_linear_model_and_predict(X, y)
    years_rf, predictions_rf = train_random_forest_and_predict(X, y)

    # Visualisierung der Vorhersagen
    fig_global = plot_global_forecast(years_linear, predictions_linear, predictions_rf)
    st.plotly_chart(fig_global)

    st.write("""
    Basierend auf historischen Verkaufsdaten zeigt diese Grafik die weltweite Prognose für den Verkauf von Elektrofahrzeugen bis zum Jahr 2030 mit Hilfe eines linearen Modells. Diese Prognosen helfen den Akteuren in der Elektrofahrzeugindustrie, das potenzielle Marktwachstum zu verstehen und ihre Produktionskapazitäten sowie Forschungs- und Entwicklungskapazitäten und Marketingstrategien entsprechend der erwarteten Nachfragesteigerung zu planen.

    Prognosen bis 2030: Der Elektrofahrzeugmarkt wird voraussichtlich bis zum Jahr 2030 einen Wert von 2,3 Billionen USD erreichen, was ein enormes Potenzial für Wachstum und Innovationen in der EV-Industrie darstellt. Diese Daten deuten auf Optimismus seitens der Experten und Marktanalysten hinsichtlich der Zukunft von Elektrofahrzeugen hin.
             

""")


if __name__ == "__main__":
    app()
