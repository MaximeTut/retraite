import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import numpy as np
import scipy.stats as stats
from numbers import Number
import plotly.graph_objects as go
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

def economie(plafond: int, pareto_df) -> Number:

    pareto_df["salaire_plafonne"] = np.where(pareto_df['salaire'] > plafond, plafond, pareto_df['salaire'])
    pareto_df["depense_plafonnee_annuel"] = pareto_df["salaire_plafonne"] * pareto_df["nbre_personne"] *12
    pareto_df["economie"] = pareto_df["depense_annuel"]  - pareto_df["depense_plafonnee_annuel"]
    economie = pareto_df.economie.sum()
    return "{:,.0f}".format(economie)

set_background("background2.png")


df = pd.read_csv("csvForStreamlit.csv")
df_brut = pd.read_csv("retraite_brut.csv", delimiter = ";")

titre_html = """
<link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'>

<div style="text-align: center; font-family: 'Montserrat';">
<h1 style="font-size: 70px; font-weight: 600; letter-spacing: 2rem; ">
  RETRAITE
</h1>
<h2 style="margin: 10px 0; font-size: 40px; letter-spacing: 0.1rem; font-family: 'Montserrat'; font-weight: 400;">Et si on plafonnait les pensions ?</h2>
</div>
"""

st.markdown(titre_html, unsafe_allow_html = True)



plafond = st.slider('', min_value=4000, max_value=15000, step=500)

economie_html = f"""<p style="text-align:center; font-weight: 600; 
font-size:34px; font-family: 'Montserrat'; letter-spacing: 0.1rem;">Economie réalisée par an en plafonnant les retraites à {plafond} € :</p>
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
pareto_df["depense_annuel"] = pareto_df["nbre_personne"] * pareto_df["salaire"] *12

economie_realisee = economie(plafond, pareto_df)

chiffre_economie = f"""
<p style="margin-top: 15px; text-align:center; font-size:45px; letter-spacing: 0.1rem; color: #FF4B4B; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.35); font-weight: 700; padding: 0.7rem; box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
background: linear-gradient(90deg, rgba(1,34,144,0.75) 0%, rgba(247,247,247,0.75) 50%, rgba(230,39,55,0.75) 100%); font-family: 'Montserrat';">{economie_realisee} €</p>

"""
st.markdown(chiffre_economie, unsafe_allow_html = True)

st.markdown("#")
st.markdown("#")
st.markdown("#")

#############################################THE PLOT#######################################################""
df["pension_moyenne"] = df["pension_moyenne"].astype(str)

fig, ax = plt.subplots(figsize = (12,4))
ax.bar(df["pension_moyenne"], df["depense"])
ax.set_title("Distribution des pensions")
ax.annotate("Un plafonnement n'impactera que cette catégorie", xy=(45, 6000000000), xytext=(10, 17000000000),
            arrowprops=dict(facecolor='red', arrowstyle='->', shrinkA=0))
plt.xticks(rotation=90, fontsize=8)
ax.set_ylabel("Budget de l'état (en milliards d'€)")
ax.set_xlabel("Pensions mensuelles (en €)")
st.pyplot(fig)








######################### DATA UTILISEES #################################"

with st.expander("Explications"):

    
    html_tableau = """
    <p>
    Les données utilisées proviennent du site du gouvernement. J'utilise ce tableau pour la distribution des pensions :
    (Distribution de la pension mensuelle brute de droit direct) <p>"""


    
    html_explanation = """
    <p>La distribution des retraites supérieures à 4500 euros est incertaine car non communiquée.
    En effet, on sait seulement qu'elle représente 1.44% de la population de retraités.
    Le plus probable est que ces pensions suivent une distribution de Pareto.
    En prenant en compte le budget total de l'état (294,9 milliards) et ce que coûtent exactement les pensions "pauvres",
    calculées grâce aux chiffres de ce tableau (environ 266,7 milliards), j'en conclu que l'état dépense 28,1 milliard pour
    1.44% de la population, les pensions "riches". Ce qui nous donne une pension moyenne de 9649 euros/mois pour cette catégorie
    de la population.
    J'utilise ensuite cette moyenne pour calculer le paramètre alpha de la distribution de paréto
    à 0.5.
    En résumé, les chiffres que j'utilise:</p>
        <ul>
        <li>Budget de l'état pour les pensions de droit direct : 294,9 milliards d'euros par an </li>
        <li>Nombre total de retraités : 16,9 millions</li>
        <li>Pension "pauvres" : 266,7 milliards d'euros par an</li>
        <li>Pourcentage de retraités touchant plus de 4500 euros/mois brut : 1,44%</li>
        </ul>
    <p>Ces données sont disponibles dans l'onglet "source"</p>
    
    """
    st.markdown(html_tableau, unsafe_allow_html=True)
    st.dataframe(df_brut)
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
    """
    st.markdown(Donnee_distribution, unsafe_allow_html=True)
    

with st.expander("Notebook"):
    github = """
    <p>Lien Github avec le notebook :
    <a href="https://github.com/MaximeTut/retraite">Github</a>.</p>
    """
    st.markdown(github, unsafe_allow_html=True)







