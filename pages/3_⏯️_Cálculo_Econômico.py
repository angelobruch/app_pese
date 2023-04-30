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
from streamlit_extras.stateful_button import button
from streamlit_extras.let_it_rain import rain


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

if not session_state["df_pese"].empty:
   st.write("👉 Selecione a obra do PESE para que possamos calcular os indicadores econômicos pra você 😉")
   upload_success = True
else:
   st.write("👋 Primeiramente, precisamos que você faça o upload da base CAPEX na aba 'Upload de Dados' 📁")

st.divider() 

import streamlit as st
import pandas as pd

if not session_state["df_pese"].empty:
   filtro_empresa = session_state["df_pese"]['Empresa'] == st.selectbox('Selecione a Empresa', session_state["df_pese"]['Empresa'].unique())

   if filtro_empresa.any():
      df_filtered_empresa = session_state["df_pese"][filtro_empresa]
      obras_selecionadas = st.multiselect('Selecione a obra', df_filtered_empresa['Nome da Obra'].unique(), key="obras")
      if len(obras_selecionadas) > 0:
   # O usuário selecionou uma obra
         obra_selecionada = df_filtered_empresa[df_filtered_empresa['Nome da Obra'] == obras_selecionadas[0]].iloc[0]

      if not obras_selecionadas:
         st.warning("Selecione pelo menos uma obra")
      else:
         filtro_obra = df_filtered_empresa['Nome da Obra'].isin(obras_selecionadas)
         df_filtered = df_filtered_empresa[filtro_obra]
         obra_selecionada = df_filtered.iloc[0]
         with st.expander("Detalhes da obra"):
            st.subheader("Informações gerais")
            st.write(f"Nome da obra: {obra_selecionada['Nome da Obra']}")
            st.write(f"Ano PO: {obra_selecionada['Ano PO']}")
            st.write(f"Status da obra: {obra_selecionada['Status da Obra']}")
            st.write(f"Descrição: {obra_selecionada['Descrição']}")
            st.write(f"Responsável Planejamento: {obra_selecionada['Responsável Planejamento']}")
            orcamento_medio = df_filtered['Orçamento Total'].mean()
            orcamento_formatado = f"R${orcamento_medio:,.2f}"
            st.write(f"Orçamento Total Médio: {orcamento_formatado}")
            
      st.divider() 
      if obras_selecionadas:
         st.write("👇 Insira os inputs abaixo para realizarmos o cálculo econômico: 💰💸💹")
         # Configura as colunas
         col1, col2, col3 = st.columns(3)

         # Taxa de Desconto para o Cálculo Econômico
         taxa_desconto = col1.number_input(
            "Taxa de Desconto (WACC)",
            value=session_state.get("taxa_desconto", 0.0),
            format="%.2f",
            step=0.01,
            help="Insira a taxa de desconto para o cálculo econômico em decimal",
         )
         session_state["taxa_desconto"] = taxa_desconto

         # Perdas Técnicas
         perdas_tecnicas = col2.number_input(
            "Perdas Técnicas (MWh)",
            value=session_state.get("perdas_tecnicas", 0),
            format="%d",
            step=1,
            help="Insira as perdas técnicas em porcentagem",
         )
         session_state["perdas_tecnicas"] = perdas_tecnicas

         # Energia Não-Circulante
         energia_nao_circulante = col3.number_input(
            "Energia Não-Circulante (MWh)",
            value=session_state.get("energia_nao_circulante", 0),
            format="%d",
            step=1,
            help="Insira a energia não-circulante em porcentagem",
         )
         session_state["energia_nao_circulante"] = energia_nao_circulante

         # Verifica se o botão foi pressionado
         if button("Confirmar Inputs", key="button1"):
            st.divider()
            with st.expander("Entradas do Usuário"):
               st.subheader("Informações que serão utilizadas no cálculo:")
               st.write(f"Taxa de Desconto: {energia_nao_circulante}")
               st.write(f"Perdas técnicas: {perdas_tecnicas}")
               st.write(f"Energia Não-Circulante: {energia_nao_circulante}")
               rain(
                  emoji="🎈",
                  font_size=54,
                  falling_speed=5,
                  animation_length="infinite",
               )

            
   else:
      st.warning("Nenhuma obra encontrada para essa empresa")
else:
   st.warning("Nenhum arquivo carregado ainda")