from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import openpyxl
from PIL import Image
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.app_logo import add_logo

# Configurações da página
st.set_page_config(
    page_title="Home",
    initial_sidebar_state="expanded",
    layout="wide"
)

# Define uma função que será usada para inicializar o session state
@st.cache_data
def init_session_state():
    return {"df_pese": pd.DataFrame()}

# Inicializa o session state
session_state = st.session_state.setdefault(
    "session_state", init_session_state())

# # Acessa o dataframe df_pese armazenado no session state
# if not session_state["df_pese"].empty:
#     st.dataframe(session_state["df_pese"])

add_logo("static\img\Energia_pos_RGB.png", height=100)
# cpfl_logo = Image.open('static\img\Energia_pos_RGB.png')
# st.image(cpfl_logo)
st.title("PESE SmartCalc", anchor=None, help=None)
st.write("App para cálculo de viabilidade financeira das obras do PESE")

st.divider() 

st.markdown(
    """
    Este APP foi feito em Python por **Angelo T. Bruch de Oliveira e Stanley E. Tokuno** e ainda está em fase de desenvolvimento. 👈
    ### Gostaria de saber mais?
    - Visite a página [streamlit.io](https://streamlit.io)
    - Vá até [documentation](https://docs.streamlit.io)
    - Tenha calma, estamos fazendo o nosso melhor para entregar um APP funcional 🧘‍♀️🧘‍♂️💻💪🚀
"""
)
# %%