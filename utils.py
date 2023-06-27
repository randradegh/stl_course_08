##
# NOTAS
# Configuración básica en config.toml
# Fuente principal de esta página: https://www.geeksforgeeks.org/a-beginners-guide-to-streamlit/
# Fuente para el pie de página: https://www.youtube.com/watch?v=MeOjN5tb51U
##
##
# Utilerias del proyecto intro_stl
##

# Incluímos las bibliotecas necesarias
import streamlit as st

# Debe ser el primer comando
#st.set_page_config(page_title='Intro', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.set_page_config(
     page_title="9 Casos de Negocio con Streamlit",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="auto"
 )

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pydeck as pdk
#from scipy import stats
import numpy as np 


##
# Pie de página
##
my_footer = """
<style>
footer {
    visibility:visible;
}

footer:after {
    content:'Copyrigth © 2023, RAF.';
    display:block;
    position:relative;
    color:#2E4053;
    padding:5px
    top:3px
}
</style>
"""
 
##
# TODO
##
# - Definir una tarea para practicar lo aprendido
# - Logo
##
##
# Funciones
##

def header(text):
    BG_COLOR = "#FCF3CF"
    FONT_COLOR = "#2E4053"
    st.markdown(f'''
    <p style="font-size:34px;background-color:{BG_COLOR};color:{FONT_COLOR};border-radius:2%;text-align:center">{text}</p>
    ''', unsafe_allow_html=True)

def footer(text):
    BG_COLOR = "#E6E6E6"
    FONT_COLOR = "#2E4053"
    st.markdown(f'''
    <p style="font-size:12px;background-color:{BG_COLOR};color:{FONT_COLOR};width:200px;border-radius:2%;text-align:center">{text}</p>
    ''', unsafe_allow_html=True)

def subheader(text):
    BG_COLOR = "#E6E6E6"
    FONT_COLOR = "#6E6E6E"
    font = "sans-serif"
    st.markdown(f'''
    <p style="background-color:{BG_COLOR};color:{FONT_COLOR};font-size:26px;border-radius:2%;">{text}</p>
    ''', unsafe_allow_html=True)
##
# Layout
##
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)
#st.set_page_config(page_title='Bussines STL', page_icon = 'streamlit.png', layout = 'wide', initial_sidebar_state = 'auto')

#original_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Original image</p>'

##
# Definimos el ancho del despliegue
##

max_width=1200
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
    }}    
</style>
""",
        unsafe_allow_html=True,
    )

##
# Color para las columnas
# Fuente: https://discuss.streamlit.io/t/changing-color-of-a-column/10175/2
# No lo aplicaré por ahora,
##

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# local_css("style.css")

##
# Abrimos con un encabezado gráfico
##
st.image('images/wp3205208.jpg')
st.markdown(my_footer, unsafe_allow_html=True)

