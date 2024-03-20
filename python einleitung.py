import streamlit as st

st.title("Ära der Elektroautos: Analyse, Trends und Zukunft der Mobilität")

@st.cache_data
def app():


    st.image("EV.jpg", use_column_width=True)

    st.write(""" 
    Willkommen zur Präsentation über die aktuellen Trends im Bereich Elektrofahrzeuge.        
    Heute werden wir uns eingehend mit der Dynamik des Verkaufs von Elektrofahrzeugen, dem Energieverbrauch,
    der fortschreitenden Entwicklung der Ladeinfrastruktur und den neuesten Modellen auf dem Markt befassen.         
    Elektrofahrzeuge erleben dank eines zunehmenden Umweltbewusstseins einen signifikanten Anstieg der Verkaufszahlen. 
    Parallel dazu ist die Entwicklung einer zuverlässigen Ladeinfrastruktur zu einem wesentlichen Faktor für das Wachstum des Elektrofahrzeugmarktes geworden, 
    indem ein umfassendes Netzwerk von Ladestationen weltweit bereitgestellt wird. Automobilhersteller investieren intensiv in die Entwicklung innovativer Elektrofahrzeugmodelle,     
    um den diversen Anforderungen und Wünschen der Konsumenten gerecht zu werden. Diese Präsentation wird Ihnen tiefergehende Einblicke in die treibenden Kräfte hinter dem aktuellen 
    Markt für Elektrofahrzeuge und ihre Bedeutung für die Zukunft der Mobilität bieten.        
             
    Im Rahmen unserer Diskussion über Elektrofahrzeuge unterscheiden wir zwei Haupttypen: BEV (Battery Electric Vehicles) und PHEV (Plug-in Hybrid Electric Vehicles).
    BEV-Fahrzeuge, auch bekannt als reine Elektrofahrzeuge, werden ausschließlich mit elektrischer Energie betrieben, die in Batterien gespeichert ist, 
    und kommen ohne einen Verbrennungsmotor aus. Diese Fahrzeuge bieten Vorteile in Bezug auf Effizienz und die Reduzierung von Emissionen, 
    da sie elektrische Energie als einzige Antriebsquelle nutzen.
                     
    Auf der anderen Seite kombinieren PHEV-Fahrzeuge den elektrischen Antrieb mit einem traditionellen Verbrennungsmotor. Diese Fahrzeuge können über eine externe Stromquelle aufgeladen werden, 
    was es ihnen ermöglicht, bestimmte Strecken ausschließlich mit elektrischer Energie zu fahren, 
    bevor der Verbrennungsmotor aktiv wird. Dies ermöglicht ihnen eine größere Reichweite und Flexibilität im Vergleich zu BEV-Fahrzeugen.    
             
             
             """)
