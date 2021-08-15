#!/usr/bin/env python
# coding: utf-8

# In[ ]:
'''
# Dashboard Streamlit

Dipendenze: 
 - Python
 - Streamlit

'''
# Importo le librerie
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go #per modificare la legenda
import numpy as np


def plot_lines (sensibilita, specificita, incidenza):
    """
    Funzione di plotting 
    """
         
    numero_di_positivi = incidenza
    numero_di_negativi = 100-incidenza
    veri_positivi = 100*((sensibilita/100)*numero_di_positivi)/numero_di_positivi
    falsi_positivi = 100-100*((specificita/100)*numero_di_negativi)/numero_di_negativi
    

    fig = go.Figure(
        go.Scatter(
              x=[incidenza,incidenza],
              y=[0,100],
              mode='lines',
              name='incidenza positivi',
              line=go.scatter.Line(color="red")
              )
      )
        

    fig.add_trace(
         go.Scatter(
            x=[0,0,100, 100], 
            y=[0,100,100,0], 
            name='Veri negativi',
            fill="toself", fillcolor="orange", opacity=0.2)
        )

  
    fig.add_trace(
        go.Scatter(
            x=[0,0,numero_di_positivi, numero_di_positivi], 
            y=[0,100,100,0], 
            name='Falsi negativi',
            fill="toself", fillcolor="red", opacity=0.2)
        )


    fig.add_trace(
        go.Scatter(
            x=[0,0,numero_di_positivi,numero_di_positivi], 
            y=[0,veri_positivi,veri_positivi,0], 
            name='Veri positivi',
            fill="toself", fillcolor="blue", opacity=0.2)
        )

    

    fig.add_trace(
        go.Scatter(
            x=[incidenza,incidenza,100,100], 
            y=[0,falsi_positivi,falsi_positivi,0], 
            name='Falsi positivi',
            fill="toself", fillcolor="green", opacity=0.2)
            
        )
    
   
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    fig.update_layout(
        height=550,
        #title_text='Visualizzazione legge di Bayes',
        xaxis_title="Percentuale popolazione ",
        yaxis_title="Percentuale popolazione ",
    )
    return fig



# Titolo
st.title('Dashboard dinamica per la visualizzazione della probabilità condizionata su un test statistico')

# Slider sidebar
st.sidebar.write('Regola i parametri di accuratezza del test diagnostico')

sensibilita = st.sidebar.slider("Valore di sensibilità in %", 1, 100, 90)
#st.sidebar.write('Il valore di sensibilità è: ', sensibilita, " %")

specificita = st.sidebar.slider("Valore di specificità in %", 1, 100, 95)
#st.sidebar.write('Il valore di specificità è: ', specificita, " %")

incidenza = st.sidebar.slider("Valore di incidenza in %", 0, 100, 10)
#st.sidebar.write('Il valore di incidenza è: ', incidenza, " %")

dimensione_popolazione = st.sidebar.slider("Dimensione della popolazione ", 0, 1000000, 500000)
#st.sidebar.write('La dimensione della popolazione è: ', dimensione_popolazione)


# calcoli con parametri della sidebar
numero_di_positivi = incidenza*dimensione_popolazione/100
numero_di_negativi = (100-incidenza)*dimensione_popolazione/100
veri_positivi = sensibilita*numero_di_positivi/100
veri_negativi = specificita*numero_di_negativi/100
falsi_positivi = numero_di_negativi - veri_negativi
falsi_negativi = numero_di_positivi - veri_positivi 

probabilita_pos_dato_positivo = veri_positivi/(veri_positivi+falsi_positivi)
st.write('Probabilità di essere positivo avendo ricevuto un test con esito positivo:', np.round(100*probabilita_pos_dato_positivo,2), "%")

probabilita_neg_dato_negativo = veri_negativi/(veri_negativi+falsi_negativi)
st.write('Probabilità di essere negativo avendo ricevuto un test con esito negativo:', np.round(100*probabilita_neg_dato_negativo,2), "%")

fig = plot_lines (sensibilita, specificita, incidenza)
st.plotly_chart(fig)

# Descrizione della distribuzione nella popolazione rispetto ai dati inseriti 
st.sidebar.write('Tot positivi nella popolazione:', int(numero_di_positivi))
st.sidebar.write('Tot negativi nella popolazione:', int(numero_di_negativi))
st.sidebar.write('Veri positivi:', int(veri_positivi))
st.sidebar.write('Veri negativi:', int(veri_negativi))
st.sidebar.write('Falsi positivi:', int(falsi_positivi))
st.sidebar.write('Falsi negativi:', int(falsi_negativi))


st.markdown(
"""
# Guida
\n
Questa applicazione serve a visualizzare facilmente gli effetti di un test diagnostico 
su una popolazione usando la legge di Bayes. 

Dati due eventi indipendenti $A$ e $B$ la legge di Bayes ci dice che la probabilità condizionata 
della verificazione dell'evento $A$, dato che l'evento $B$ si è verificato, è calcolabile come: 

$P(A|B) = P(B|A) * P(A) / P(B)$

Dove: 
- $P(A)$ è la probabilità di verificazione dell'evento $A$
- $P(B)$ è la probabilità di verificazione dell'evento $B$
- $P(B|A)$ è la probabilità di verificazione dell'evento $B$ dato l'evento $A$ verificato

Supponiamo quindi di avere una popolazione di N soggetti i quali devono eseguire un test 
di positività ad una patologia (es. Maurite). La maurite ha una incidenza sulla popolazione 
regolabile usando l'indicatore -incidenza- che rappresenta la percentuale di popolazione che 
effettivamente ha la maurite (valore di default 10%). 

Gli scienziati hanno sviluppato un test diagnostico che riesce a rilevare la maurite. 
La probabilità di risultare positivo al test diagnostico per un soggetto avente la maurite 
è pari al valore di sensibilità del test (valore di default 90%). 
La probabilità di risultare negativo al test diagnostico per un soggetto sano è pari al 
valore di specificità del test (valore di default pari al 95%).

Siamo interessati a sapere qual è la probabilità per un soggetto che ha ricevuto un test 
positivo di essere effettivamente positivo. 

Il risultato non è affatto banale e fortemente controintuitivo. 
Questa dashboard calcola le probabilità condizionate di essere positivo avendo avuto ricevuto 
un test con esito positivo e la probabilità di essere negativo avendo ricevuto un test con esito negativo. 


"""
)
