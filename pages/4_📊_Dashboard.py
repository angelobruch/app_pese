import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import openpyxl
from PIL import Image
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


session_state = st.session_state.get(df_pese=pd.DataFrame())
session_state.df_pese