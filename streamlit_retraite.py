import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import numpy as np
import scipy.stats as stats
from numbers import Number
import matplotlib.pyplot as plt

st.set_page_config(page_title="My App", page_icon=":shark:")

@st.experimental_singleton
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.experimental_singleton
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-color:rgba(0,0,0,0.1)

    }
    </style>
    ''' % bin_str
    return st.markdown(page_bg_img, unsafe_allow_html=True)

def economie(plafond: int) -> Number:
    economie = sum(pareto_df[pareto_df.salaire>plafond]["salaire"] * pareto_df[pareto_df.salaire>plafond]["nbre_personne"]*12)
    return "{:,.0f}".format(economie)

set_background("background2.png")


df = pd.read_csv("csvForStreamlit.csv")


titre_html = """
<p style="text-align: center; font-family: Arial, sans-serif;">
  <span style="color: blue; font-size: 70px;">RET</span>
  <span style="color: black; font-size: 70px;">RAI</span>
  <span style="color: red; font-size: 70px;">TE</span>
  <br>
  <span style="font-size: 45px;">Et si on plafonnait les pensions ?</span>
</p>


"""
st.markdown(titre_html, unsafe_allow_html = True)



plafond = st.slider('', min_value=4000, max_value=15000, step=500)

economie_html = f"""<h1 style="color:#8B0000; text-align:center;
font-size:35px;">Economie réalisée par an en plafonnant les retraites à {plafond} euros :</h1>
"""

st.markdown(economie_html, unsafe_allow_html = True)

df_streamlit = pd.read_csv("csvForStreamlit.csv")
alpha = 0.5
min_salary = 4500
max_salary = 22000
num_people = df_streamlit.tail(1).nombre_personnes.sum()


x = np.arange(min_salary, max_salary, 500)
pareto = stats.pareto(alpha, scale=min_salary)
pdf = pareto.pdf(x)
pdf_normalized = pdf * (1 / np.sum(pdf))

pareto_df = pd.DataFrame()
pareto_df["proba"] = pdf_normalized
pareto_df["nbre_personne"] = pareto_df["proba"]*num_people
pareto_df["nbre_personne"] = round(pareto_df.nbre_personne).astype(int)
pareto_df["salaire"] = x

economie_realisee = economie(plafond)

chiffre_economie = f"""
<h1 style="color:red; text-align:center; font-size:45px; 
background-color:rgba(255, 255, 255, 0.5);">{economie_realisee} Euros</h1>

"""
st.markdown(chiffre_economie, unsafe_allow_html = True)

st.markdown("#")
st.markdown("#")
st.markdown("#")






######################### DATA UTILISEES #################################"

with st.expander("Explications"):

    
    html_explanation = """
    <p>La distribution des retraites supérieures à 4500 euros est incertaine car non communiquée.
    Le plus probable est que ces pensions suivent une distribution de Pareto.
    J'estime le paramètre alpha de cette distribution à 0.5 en utilisant la moyenne des pensions
    de la catégorie "pensions >4500 euros" à 9600 euros mensuels. Pour cela j'utilise ces chiffres :</p>
        <ul>
        <li>Budget de l'état pour les pensions de droit direct des régimes obligatoires : 294,9 milliards d'euros par an </li>
        <li>Nombre total de retraités = 16,9 millions</li>
        <li>Pourcentage de retraités touchant plus de 4500 euros/mois brut : 1,44%</li>
        </ul>
    <p>Ces données sont disponibles dans l'onglet "source"</p>
    <p>Ces données sont disponibles dans l'onglet "source"</p>

    
    """

    st.markdown(html_explanation, unsafe_allow_html=True)


with st.expander("Sources"):
    budget = """
     <p>Budget de l'état pour les pensions de droit direct :
    <a href="https://www.vie-publique.fr/fiches/37945-quel-est-le-budget-consacre-aux-retraites#:~:text=Le%20budget%20consacr%C3%A9%20aux%20pensions,produit%20int%C3%A9rieur%20brut%20(PIB).">www.vie-publique.fr</a>.</p>

    """
    st.markdown(budget, unsafe_allow_html=True)


    nombre_retraite = """
     <p>Nombre de retraités:
    <a href="https://www.insee.fr/fr/statistiques/2415121#:~:text=Lecture%20%3A%20en%202020%2C%20le%20nombre,31%20d%C3%A9cembre%20de%20l%27ann%C3%A9e.">www.insee.fr</a>.</p>

    """
    st.markdown(nombre_retraite, unsafe_allow_html=True)

    Donnee_distribution = """
    <p>Distribution des pensions:
    <a href="https://data.drees.solidarites-sante.gouv.fr/explore/dataset/4178_distribution-des-pensions-mensuelles/information/">data.drees.solidarites-sante.gouv.fr</a>.</p>
    <p>Du jeu de données fournis, j'utilise ce tableau (Distribution de la pension mensuelle brute de droit direct):
    """
    st.markdown(Donnee_distribution, unsafe_allow_html=True)
    df_brut = pd.read_csv("retraite_brut.csv", delimiter = ";")
    st.dataframe(df_brut)
    









