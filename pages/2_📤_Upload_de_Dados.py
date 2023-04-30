import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import openpyxl
from PIL import Image
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import tempfile
import os
from IPython.display import display
from streamlit_extras.app_logo import add_logo

# Configurações da página
st.set_page_config(
    page_title="Upload dos Dados",
    initial_sidebar_state="expanded",
    layout="wide"
)

# Define uma função que será usada para inicializar o session state
@st.cache_data
def init_session_state(allow_output_mutation=True):
    return {"df_pese": pd.DataFrame()}

# Inicializa o session state
session_state = st.session_state.setdefault("session_state", init_session_state())

add_logo("static\img\Energia_pos_RGB.png", height=100)
# cpfl_logo = Image.open('static\img\Energia_pos_RGB.png')
# st.image(cpfl_logo)
st.title("PESE SmartCalc")

upload_success = False

if not session_state["df_pese"].empty:
    st.write("Vá até a aba 'Análise da Base' e veja o que obtivemos dos dados disponibilizados: 🔍💻📊👀")
    upload_success = True
else:
    st.write("Realize o upload da Base CAPEX e relaxe 😎👨‍💻, iremos fazer algumas análises 📊💻🔍")

st.divider() 

def save_uploaded_file(uploadedfile):
    with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Arquivo salvo: {} em tempDir".format(uploadedfile.name))

tab1, tab2 = st.tabs(["Upload da Base CAPEX", "Análise da Base"])

with tab1: 
# Carrega o arquivo
    pese_file = st.file_uploader('Selecione o arquivo CAPEX', type=["xls", "xlsx", "xlsm"])
    if pese_file is not None:
        df_pese = pd.read_excel(pese_file, sheet_name="CAPEX")
        cols_fixas = df_pese.columns[:29]
        df_pese= pd.melt(df_pese, id_vars=cols_fixas, var_name='data', value_name='valor')
        df_pese['data'] = pd.to_datetime(df_pese['data'], format='%d/%m/%Y')
        df_pese['ano'] = df_pese['data'].dt.year
        df_pese = df_pese.drop('data', axis=1)
        cols_fixas = list(cols_fixas) + ['ano']
        df_pese = df_pese.groupby(cols_fixas)['valor'].sum().reset_index()
        df_pese = df_pese[(df_pese['Status da Obra'] == 'Ativa') | (df_pese['Status da Obra'] == 'Em Andamento')]
        df_pese = df_pese[(df_pese['TP'] == 28) | (df_pese['TP'] == 29)]
        session_state["df_pese"] = df_pese
    
# Acessa o dataframe df_pese armazenado no session state
    if not session_state["df_pese"].empty:
        # st.dataframe(session_state["df_pese"])
        if pese_file is not None:
            save_uploaded_file(pese_file)
            file_details = {"filename" : pese_file.name,
                        "filetype" : pese_file.type,
                        "filesize" : pese_file.size}
            session_state["file_details"] = file_details
            st.write(session_state.get("file_details", {}))
            upload_success = True
            if "file_details" not in session_state:
                session_state["file_details"] = {}

    if upload_success:
        st.success("Upload realizado com sucesso!")
        # st.write(session_state.get("file_details", {}))
        # st.dataframe(session_state["df_pese"]) 
    else:
        st.warning("Nenhum arquivo carregado ainda")   

with tab2:
    if "df_pese" in session_state:
        if not session_state["df_pese"].empty:
            # st.dataframe(session_state["df_pese"])
            # verifica se o ProfileReport já foi gerado antes
            if "pr" not in session_state:
                pr = session_state["df_pese"].profile_report()
                session_state["pr"] = pr
            else:
                pr = session_state["pr"]
                
            st_profile_report(pr)
        else:
            st.warning("Nenhum arquivo carregado ainda")
    else:
        st.warning("Nenhum arquivo carregado ainda")