##
# Análisis de accidentes de «listings» en la CDMX. Uso de streamlit, dataframes, pandas, mapas.
##
# Fecha inicio: 20220206
# Ref: Proyecto personal con datos de INEGI

##
# Utilerías del proyecto
##
from os import ST_WRITE
from utils import *

# Biblioteca local
import geopandas as gpd

header("9 casos de negocio con Streamlit")
st.subheader("8. Análisis de alojamientos temporales en la CDMX. Parte 1.")
st.subheader("Introducción")

st.markdown("""
    Se analizarán los alojamientos temporales tradicionales de la Ciudad de México y 
    los que ofrecen los particulares por medio de la plataforma AirBnB.

    Primero analizaremos los tradicionales y después los ofrecidos por AirBnB.

    ### Los alojamientos temporales de la Ciudad de México
    El objetivo de esta parte app es realizar un análisis sobre los inmbuebles para alojamientos temporales, 
    ya sea del tipo de hoteles u de particulares (AirBnB) en las diversas alcaldías de la 
    Ciudad de México, México.
    
    ??? Se construirá una app interactiva que permita que el usuario seleccione los 
    datos que desea analizar.
    Se mostrarán gráficos que permitan sacar algunas conclusiones acerca de las 
    diferencias en el comportamiento en cada alcaldía, además de...
""")
st.markdown("""
    
    ### Temas a analizar- ¿Qué _features_ tiene nuestros _dataset_?
    - ¿En qué alcaldias hay más alojamientos temporales, por tipo?
    - Otras preguntas.

    Alguna de las preguntas se responderán para cada alcaldía de manera 
    interactiva.

    Se usarán tres datasets:
    - Datos del DENUE para la CDMX para el tema de la sesión
    - Listings de AiBnB descargados en línea desde el sitio http://data.insideairbnb.com para la CDMX actualizados al 20211225.
        ___
    #### Carga de datos y contenido del _dataset_...
    
    Cargamos los datos usando el método read_csv() de Pandas.
    #### Carga de los datos del **Directorio Estadístico Nacional de Unidades Económicas (DENUE)**.
    Sitio oficial en INEGI: https://www.inegi.org.mx/app/mapa/denue/default.aspx

    La descarga se hace del sitio https://www.inegi.org.mx/app/descarga/?ti=6, en particular los dos 
    archivos nombrados «Servicios de alojamiento temporal y de preparación de alimentos y bebidas».

    De los registros de esos dos archivos se seleccionaron solamente los referentes a los rubros de 
    alojamientos temporales. Con ellos se construyó el _dataset_que usaremos en esta sesión.

""")
pd_hoteles = pd.read_csv('data/denue_hoteles_cdmx_2020.csv', sep='|')
#pd_hoteles = pd_hoteles.rename(columns={'municipio':'nomgeo'})
st.write(pd_hoteles.head(10))

#st.write(type(hoteles.columns))
with st.echo(code_location='above'):
    st.write(f"""
        En total son {len(pd_hoteles.columns)}. De ellas pueden ser interesantes el nombre del establecimiento, 
        la colonia y la alcaldía en donde está, el tipo de actividad, longitud y latitud.

        Vamos a generar otro _dataframe_ seleccionando solamente esas columnas.

        Además, por razones que veremos en un momento, vamos a cambiar el nombre de la columna 
        *municipio* a *alcaldia*.
    """)

    hoteles = pd_hoteles[['nom_estab','nombre_act','nomb_asent','municipio','latitud', 'longitud']]
    hoteles = hoteles.rename(columns={'municipio':'alcaldia'})
    st.write(hoteles.head(5))

'''
    ___
    ##### Valores únicos de tres columnas del _dataset_ *hoteles*

     - **Nombre de la actividad (*nombre_act*)**
'''

st.write(hoteles.nombre_act.sort_values().unique())

'''
         - **Nombre de la colonia (*nomb_asent*)**
'''

st.write(hoteles.nomb_asent.sort_values().unique())

st.write(f"""
    Tenemos un total de {len(hoteles.nomb_asent.sort_values().unique())} colonias.
""")

'''
         - **Nombre de las alcaldías (*alcaldia*)**
'''
st.write(hoteles.alcaldia.sort_values().unique())

'''
    ___
'''
##
# Gráficos por _features_
##

'''
    #### Gráfico de barras de tipo de actividad de los alojamientos temporales por alcaldía
'''

##
# Versión 1, sin mostrar la alcaldía
##

'''
    ___
    **Caso 1: Primera versión.**
'''
with st.echo(code_location='above'):

    # Agrupamos por actividad y alcaldía, creamos el campo de count
    df_hna_count_a= hoteles[['nomb_asent', 'alcaldia']].groupby(['nomb_asent', 'alcaldia']).size().reset_index(name='count')
    
    # Ocultamos el despliegue de los df
    with st.expander("Visualizar/Ocultar dataframe de alojamientos.", expanded=False):
        '''
            **Cantidad de alojamientos por colonia y alcaldía**
        '''
        st.write(df_hna_count_a.sort_values(by=['count'], ascending=False))

    # Gráfico de barras

    fig_a = px.bar(df_hna_count_a.sort_values(by=['count'], ascending = False).head(20), x="nomb_asent", y='count',
            title = "Alojamientos temporales en la CDMX por Colonia.<br>Se muestran solamente los 20 primeros.", 
            color="nomb_asent", 
            labels={ # Replaces default labels by column name
                "nomb_asent": "Colonia",
                "count": "Cantidad"
                },
            width = 800, 
            height = 800
    )
    
    BGCOLOR = "#A9BCF5"
    
    fig_a.update_layout({
        #'yaxis_title': 'Cantidad',
        #'xaxis_title': 'Colonia',
        'plot_bgcolor': BGCOLOR,
        'paper_bgcolor': BGCOLOR,
        'font_family':"Cantarell",
        'font_size': 14,
        'font_color' :"#0B2161",
        'title_font_family':"Cantarell",
        'title_font_color':"black",
        'legend_title_font_color':"black"    
    })

fig_a

##
# Versión 2, mostrando la alcaldía
##
'''
    ___
    **Caso 2: Concatenando colonia y alcaldía.**
'''
# Gráfico de barras 
with st.echo(code_location='above'):

    # Nuevo campo para concatenar la colonia con la alcaldía, la usaremos en un momento
    hoteles['col_alc']=hoteles['nomb_asent'].astype(str)+'/'+hoteles['alcaldia']

    # Agrupamos por actividad y alcaldía, creamos el campo de count
    df_hna_count_b= hoteles[['col_alc', 'alcaldia']].groupby(['col_alc', 'alcaldia']).size().reset_index(name='count')
    
    # Ocultamos el despliegue de los df
    with st.expander("Visualizar/Ocultar dataframe de alojamientos.", expanded=False):
        '''
            **Cantidad de alojamientos por colonia y alcaldía**
        '''
        st.write(df_hna_count_b.sort_values(by=['count'], ascending=False))
        #st.write(df_hna_count.sort_values(by=['count'], ascending=False))

    fig_b = px.bar(df_hna_count_b.sort_values(by=['count'], ascending = False).head(20), x="col_alc", y='count',
            title = "Alojamientos temporales en la CDMX por Colonia.<br>Se muestran solamente los 20 primeros.", 
            color="col_alc", 
            labels={ 
                "col_alc": "Colonia/Alcaldía",
                "count": "Cantidad"
                },
            width = 800, 
            height = 850
    )
    
BGCOLOR = "#A9BCF5"

fig_b.update_layout({
    'plot_bgcolor': BGCOLOR,
    'paper_bgcolor': BGCOLOR,
    'font_family':"Cantarell",
    'font_size': 14,
    'font_color' :"#0B2161",
    'title_font_family':"Cantarell",
    'title_font_color':"black",
    'legend_title_font_color':"black"    
})

fig_b

##
# Limpieza de datos
##

'''
    #### Limpieza de datos
    Vamos a buscar la cadena «CENTR» al inicio del nombre de la colonia:

    st.write(df_hna_count_a[df_hna_count_a.nomb_asent.str.contains('^CENTR')].head(20))

    y desplegamos el _dataframe_:
'''

with st.echo(code_location='bellow'):

    st.write(df_hna_count_a[df_hna_count_a.nomb_asent.str.contains('^CENTR')].head(20))

st.write("""
Así, encontramos lo siguiente:
- Existen varias colonias «CENTRO» y algunas fuera de la alcaldía «Cuauhtémoc»
- Debemos agrupar a todas ellas dentro de una sola categoría
- Hay un problema con la cadena «Centro» que ocurre 22 veces, debemos solucionarlo

Empecemos por limpiar los 22 registros. El problema es que el caracter final es un «cero«, no 
una «o», así que vamos a sustituir ese valor en nuestro _dataset_ usando Python.

Una solución profunda sería hacer el cambio en el archivo fuente y avisarle al INEGI ;-).

El cambio debemos hacerlo en el _dataset_ *hoteles*, antes de hacer el _groupby_.

Procedamos.
""")
with st.echo(code_location='above'):
    #Hacemos el cambio en el _dataset_ *hoteles*
    hoteles['nomb_asent'] = hoteles.nomb_asent.replace("CENTR0", "CENTRO")

    #Recreamos el agrupado
    df_hna_count_a= hoteles[['nomb_asent', 'alcaldia']].groupby(['nomb_asent', 'alcaldia']).size().reset_index(name='count')

    #Mostramos el resultado
    st.write(df_hna_count_a[df_hna_count_a.nomb_asent.str.contains('^CENTR')])
    
"""
    Observe que el registro de «CENTRO» para la alcaldía Cuauhtémoc ya tiene una 
    cuenta de 85 registros.

    **- Recuperar todos los registros que mencionen «CENTRO»**

    Lo que sigue es incorporar todos los renglones que contengan la palabra 
    «CENTRO» en cualquier posición. 

    Lo que haremos será eliminar las cadenas que no sean «CENTRO».
"""

with st.echo(code_location='above'):
    #Hacemos el cambio en el _dataset_ *hoteles*
    hoteles = hoteles.replace({'nomb_asent': r'^CENTRO.*$'}, {'nomb_asent': 'CENTRO'}, regex=True)

    # Recreamos el agrupado
    df_hna_count_a= hoteles[['nomb_asent', 'alcaldia']].groupby(['nomb_asent', 'alcaldia']).size().reset_index(name='count')

    # Mostramos lo obtenido
    st.write(df_hna_count_a[df_hna_count_a.nomb_asent.str.contains('^CENTR')].head(20))

"""
    Note que ya recuperamos todas las colonias (**116**) que contienen la palabra «CENTRO», en particular 
    las de la alcaldía Cuahtémoc.

    Ya estamos listos para construir el nuevo gráfico.
"""
fig_c = px.bar(df_hna_count_a.sort_values(by=['count'], ascending = False).head(20), x="nomb_asent", y='count',
            title = "Alojamientos temporales en la CDMX por Colonia.<br>Se muestran solamente los 20 primeros.", 
            color="nomb_asent", 
            labels={ 
                "nomb_asent": "Colonia",
                "count": "Cantidad"
                },
            width = 800, 
            height = 750
    )
    
BGCOLOR = "#A9BCF5"

fig_c.update_layout({
    'plot_bgcolor': BGCOLOR,
    'paper_bgcolor': BGCOLOR,
    'font_family':"Cantarell",
    'font_size': 14,
    'font_color' :"#0B2161",
    'title_font_family':"Cantarell",
    'title_font_color':"black",
    'legend_title_font_color':"black"    
})

fig_c


'''
    ___
    ####  Análisis de tipos de actividades por alcaldía, usando gráficos de barras con facetas
'''
# Gráfico de barras con varias facetas
with st.echo(code_location='above'):
    # Agrupamos por actividad y alcaldía, creamos el campo de count
    df_hna_count= hoteles[['nombre_act','alcaldia']].groupby(['alcaldia','nombre_act']).size().reset_index(name='count')

    fig = px.bar(df_hna_count, x="alcaldia", y='count',
            title = "Actividad de los alojamientos temporales en la CDMX", facet_col = 'nombre_act',
            facet_col_wrap= 2,
            color="alcaldia",
            labels={ 
                "alcaldia": "Alcaldía",
                "count": "Cantidad",
                "nombre_act": "Actividad"
                },
            width = 1000, 
            height = 1000
    )
    
    BGCOLOR = "#A9BCF5"
    
    fig.update_layout({
        'plot_bgcolor': BGCOLOR,
        'paper_bgcolor': BGCOLOR,
        'font_family':"Cantarell",
        'font_size': 14,
        'font_color' :"#0B2161",
        'title_font_family':"Cantarell",
        'title_font_color':"black",
        'legend_title_font_color':"black"    
    })

fig

st.error('Incluir comentarios (insights)')
##
# Análisis de los alojamientos temporales de AirBnB
##

"""
    ___
   ### B) Los alojamientos temporales de AirBnB
"""

##
# Análisis de tipos de actividades por alcaldía, usando gráficos de barras con facetas.
##

url = "http://data.insideairbnb.com/mexico/df/mexico-city/2021-12-25/visualisations/listings.csv"
#@st.cache_data(allow_output_mutation=True)
@st.cache_data()
def get_data():
    return pd.read_csv(url)

df_abb = get_data()

st.write(df_abb.head(5))
##
# Limpieza de datos (RAF).
##
# ???
# df_abb['price'] = df_abb['price'].replace(regex=['^.'],value='')
# # Quitamos las comas
# df_abb['price'] = df_abb['price'].replace(regex=[','],value='')
# # Lo hacemos flotante
# df_abb["price"] = pd.to_numeric(df_abb["price"], downcast="float")

##
# Introducción
##
st.title("Análisis de Datos de AirBnB en la CDMX")
"""
    En esta app se hace un análisis de datos de los *listings* de AirBnBn en la CDMX
    El propósito del análisis es encontrar las mejores opciones para decidir en que zona es más redituable contar con una propiedad que va a ser parte del servicio de AirBnB.
    Debemos responder a las siguientes cuestiones:
    - ¿Cuál es el precio promedio por noche?  
    - ¿Que zona de la CDMX tiene la mayor cantidad de habitaciones disponibles?
    - ¿En cuál alcaldía es más elevado el precio?
    - ¿Qué tipo de habitación es más redituable?
"""

st.markdown("El *dataset* se obtuvo del URL http://data.insideairbnb.com/mexico/df/mexico-city/2021-12-25/visualisations/listings.csv")

st.markdown("## Análisis preliminar de los datos")

# Construímos la lista de features
str_cols = '<ul>'
for col in df_abb.columns:
    str_cols += '<li>' + col

str_cols = str_cols + '</ul>'

st.markdown("Columnas del *dataset*:")
st.markdown('<p>' + str_cols + '</p>', unsafe_allow_html=True)

#st.dataframe(df_abb.head(5))
st.code("""
import missingno as msno 
p = msno.matrix(df_abb)
st.pyplot(p.figure)
""")

# Análisis de nulos
"""
### Análisis de nulos usando missingno
"""
import missingno as msno 
p = msno.matrix(df_abb)
st.pyplot(p.figure)
# Limpieza del dataset
st.markdown("Eliminamos algunas columnas que no son útiles para aligerar el análisis: `id`, `host_id` y `neighbourhood_group` y otras más.")

st.code("df_abb = df_abb.drop(['id', 'host_id', 'neighbourhood_group', 'last_review', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365', 'number_of_reviews_ltm','license'], axis='columns', inplace=False)")

df_abb = df_abb.drop(['id', 'host_id', 'neighbourhood_group', 'last_review', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365', 'number_of_reviews_ltm','license'], axis='columns', inplace=False)

# Construímos la lista de features
str_cols = '<ul>'
for col in df_abb.columns:
    str_cols += '<li>' + col

str_cols = str_cols + '</ul>'

st.markdown("Nos quedamos con las siguientes columnas del *dataset*:")
st.markdown('<p>' + str_cols + '</p>', unsafe_allow_html=True)

st.markdown("Los primeros cinco registros del *dataset* son:")
st.dataframe(df_abb.head(5))

st.markdown('## Análisis estadístico')
st.markdown("""
Haremos un somero análisis estadístico del *dataset* con la función _describe()_ de Python. 

La función _describe()_ se utiliza para calcular algunos datos estadísticos como percentiles, media y desviacion 
estándar de los valores numéricos de nuestros datos.
""")
# calling describe method
desc = df_abb.describe()
# display
st.dataframe(desc)

st.markdown(f"""
    Podemos observar que el precio promedio de los _listings_ es de \$**{np.trunc(df_abb.price.mean())}**, y 
    que el precio máximo es de \$**{np.trunc(df_abb.price.max())}**. Probablemente es un error, pero si dejamos ese 
    valor nuestros cálculos se verán afectados por ser un _outlier_.
""")

# Eliminamos outliers
MAX = 20000
st.markdown(f"""
    Después de eliminar los valores atípicos (*outliers*), en nuestro caso  valores mayores a ${MAX} volvemos a _describir_ nuestros datos.
    (_Un valor atípico es una observación que se encuentra a una distancia anormal de otros valores en una muestra aleatoria de una población. En cierto sentido, esta definición deja en manos del analista (o de un proceso de consenso) decidir qué se considerará anormal. Antes de poder distinguir las observaciones anormales, es necesario caracterizar las observaciones normales_.)
""")

with st.echo(code_location='above'):
    MAX = 20000
    df_abb = df_abb[df_abb['price'] <= MAX]
    st.write(df_abb.describe())

"""
    Observemos que los valores de media y valore máximo para el precio(_price_) ha disminuido al 
    eliminar los _outliers_.

    De esta manera el análisis será más representativo de la población.
"""

##
# KPI con go para describe
##

st.title("Dashboard para toda la CDMX")

st.markdown('#### ¿Que es un tablero (*dashboard*)')
st.markdown("""
Un tablero es una muestra visual de datos importantes. Si bien se puede utilizar de diferentes formas, su principal intención es proporcionar información de un vistazo, como los KPI.

Un tablero generalmente se ubica en su propia página y recibe información de una base de datos vinculada. En muchos casos, es configurable, 
lo que le permite elegir qué datos desea ver y si desea incluir tablas o gráficos para visualizar los números.
""")

# st.markdown('## Algunos valores')
# st.write(df_abb['price'].iloc[0])
# Máximo de precios
max_price = df_abb['price'].max()
# #max_price = "{:,}".format(max_price)
# st.write(max_price)

#Cantidad de registros
qrows_0= df_abb.shape[0]
qrows = "{:,}".format(qrows_0)

font_color_text = '#7FB3D5'
font_color_number = '#82E0AA'
BGCOLOR = "#042f47"


# Precio promedio
price_avg_0 = df_abb['price'].mean()
price_avg = f"{price_avg_0:,.2f}"

# Cantidad promedio de reviews
rev_avg_0 = df_abb['number_of_reviews'].mean()
rev_avg = f"{rev_avg_0:,.2f}"
col01, col02, col03 = st.columns(3)
#col1 = st.columns(3)

fig_ind = go.Figure()

with col01:
    ref = 5
    fig_ind.add_trace(go.Indicator(
        mode = "number",
        number = {'prefix': "$",'font.size' : 55, 'font.color': font_color_number, 'valueformat':','},
        value = max_price,
        title = {'text': 'Precio<br>Máximo', 'font.size': 25, 'font.color':font_color_text},
        domain = {'row': 0, 'column': 0}))

with col02:
    fig_ind.add_trace(go.Indicator(
        mode = "number",
        number = {'prefix': "$", 'font.size' : 55, 'font.color': font_color_number},
        value = price_avg_0,
        title = {'text':'Precios<br>Promedio (MX)', 'font.size': 25, 'font.color':font_color_text},
        domain = {'row': 0, 'column': 1}))

with col03:
    ref = 5
    fig_ind.add_trace(go.Indicator(
        mode = "number",
        number = {'font.size' : 55, 'font.color': font_color_number},
        value = rev_avg_0,
        title = {'text':'Promedio de<br><i>Reviews</i>', 'font.size': 25, 'font.color':font_color_text},
        domain = {'row': 0, 'column': 2})
    )

fig_ind.update_layout(
    paper_bgcolor = BGCOLOR, 
    width=1050,
    height = 250,
    margin=dict(l=20, r=20, t=40, b=5),
    grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
)

##
# Mostramos los KPI
##
st.markdown('### *Dasboard* General de AirBnB en la Ciudad de México')
fig_ind
st.markdown("### Cantidad de *listings* por alcaldía")
st.markdown("""
    En el cuadro siguiente podemos ver cuantos _listings_ tiene cada alcaldía. ¿Cuál de ellas tiene más, cuál menos? ¿Habrá alguna razón que lo explique?

    Una lista es una de las varias maneras de presentar los datos, si están ordenados por alguna columna es más fácil su comparación.

    A continuación mostramos las alcaldías ordenadas de forma ascendente por la cantidad de _listings_ que poseen.

    ### Listado de alcaldías y _listings_, ordenados por cantidad de _listings_. 
""")

a_array = df_abb.groupby(['neighbourhood'])['neighbourhood'].count()
#st.write(a_array)
df_a = a_array.to_frame()
df_a = df_a.rename(columns={'neighbourhood': 'Cant. Listings'}) 
df_a.reset_index(inplace=True)

# Mostramos del df
st.write(df_a.sort_values(by=['Cant. Listings']))

st.markdown('### Revelaciones (*insights*)')
#str_01 = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Observe que en Milpa alta solo existen 19 _listings_.</p>'
st.write('<p style="background-color:#b4acc9;color:#7a066b;">Observe que en Milpa Alta solo existen 19 <i>listings</i>.</p>', unsafe_allow_html=True)

##
# Análisis de Milpa Alta
##

ama_max_listings = df_a['Cant. Listings'].max()
ama_avg_listings = df_a['Cant. Listings'].mean()
ama_min_listings = df_a['Cant. Listings'].min()

col_ama01, col_ama02, col_ama03 = st.columns(3)

st.markdown("## Datos sobre cantidades de _listings_ por alcaldía")

##
# Caso Milpa Alta
##
#Análisis de min, max, mean de listings
fig_agl = go.Figure()

# Análisis de precios de listings Milpa Alta
fig_aama = go.Figure()

with col_ama01:
    str1 = """Cantidad <br>
    <span style='color:#d38c27'>Máxima de </span><i>listings</i><br><span style='color:white'>      (Cuauhtémoc)</span>
    """
    fig_agl.add_trace(go.Indicator(
        mode = "number",
        number = {'font.size' : 55, 'font.color': font_color_number},
        value = int(ama_max_listings),
        delta = {'reference': 30, 'relative': True},
        title = {'text': str1, 'font.size': 18, 'font.color':font_color_text},
        domain = {'row': 0, 'column': 0}))

with col_ama02:
    str2 = """Cantidad <br>
    <span style='color:#d38c27'>Promedio </span><i>de listings</i>
    """
    fig_agl.add_trace(go.Indicator(
        mode = "number",
        number = {'font.size' : 55, 'font.color': font_color_number},
        value = int(ama_avg_listings),
        delta = {'reference': 30, 'relative': True},
        title = {'text': str2, 'font.size': 18, 'font.color':font_color_text},
        domain = {'row': 0, 'column': 1}))

with col_ama03:
    str3 = """Cantidad <br>
    <span style='color:#d38c27'>Mínima </span><i>de listings</i><br><span style='color:white'>    (Milpa Alta)</span>
    """
    fig_agl.add_trace(go.Indicator(
        mode = "number",
        number = {'font.size' : 55, 'font.color': font_color_number},
        value = int(ama_min_listings),
        delta = {'reference': 30, 'relative': True},
        title = {'text': str3, 'font.size': 18, 'font.color':font_color_text},
        domain = {'row': 0, 'column': 2}))

fig_agl.update_layout(
    paper_bgcolor = "#042f47", 
    width=1050,
    height = 300,
    margin=dict(l=20, r=20, t=20, b=20),
    grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
)

# Mostramos las tres columnas
fig_agl

st.markdown("### Cantidad de listings y precios promedios por alcaldías")

st.markdown("""
    ¿En cuál alcaldía se encuentra el precio promedio de _listings_ más alto? ¿Es lo esperado?

    ¿Por qué razones podría darse ese comportamiento?
""")

st.info("""
    Ejercicio: ¿Qué sugieren hacer para conocer las razones de que en la alcaldía Milpa Alta 
    se encuentre el mayor precio promedio de la CDMX?
""")

col11, col12 = st.columns(2)

with col11:
    fig1 = px.bar(df_a, x='neighbourhood', y='Cant. Listings', 
    color = 'neighbourhood',
    title = 'Cantidad de Listings por Alcaldía de la CDMX')
    fig1.update_layout(width=600,height=600)
    fig1.update_yaxes(title_text='Cantidad de Listings')
    fig1.update_xaxes(title_text='Alcaldías')
    fig1.update_layout({
        #'plot_bgcolor': 'red',
        'paper_bgcolor': BGCOLOR,
    })
    st.plotly_chart(fig1, use_container_width=True)

# Promedio de precios por alcaldía
ap_array = df_abb.groupby(['neighbourhood'])['price'].mean()

df_ap = ap_array.to_frame()
df_ap.reset_index(inplace=True)

df_ap = df_ap.sort_values(by=['price'], ascending = False)

# Sectores
with col12:
    # fig1 = px.pie(df_a, names='neighbourhood', values='Cant. Listings', title = 'Listings por Alcaldía de la CDMX')
    # fig1.update_layout(width=600,height=600)
    # fig1.update_layout({
    #     #'plot_bgcolor': 'red',
    #     'paper_bgcolor': BGCOLOR,
    # })
    # st.plotly_chart(fig1, use_container_width=True)

    fig1 = px.bar(df_ap, x='neighbourhood', y='price', 
    color_discrete_sequence=px.colors.qualitative.Pastel, 
    color='price', 
    title = 'Precios Promedio por Alcaldía')
    fig1.update_layout(width=600,height=600)
    fig1.update_yaxes(title_text='Precio Promedio')
    fig1.update_xaxes(title_text='Alcaldías')
    fig1.update_layout({
        #'plot_bgcolor': 'red',
        'paper_bgcolor': BGCOLOR,
    })
    
    st.plotly_chart(fig1, use_container_width=True)

"""
    ___
"""

#Box_plot para precios de Milpa Alta
#df_db = df_abb.drop(['id', 'host_id', 'neighbourhood_group'], axis='columns', inplace=False)
df_ma = df_abb[df_abb['neighbourhood']=='Milpa Alta']
fig_bp = px.box(df_ma, y="price", title='Box Plot para los precios de listings en Milpa Alta')

fig_bp.update_layout(width=600,height=500)
fig_bp.update_yaxes(title_text='Precio')
fig_bp.update_xaxes(title_text='Alcaldía Milpa Alta')

fig_bp.update_layout({
        #'plot_bgcolor': 'red',
        'paper_bgcolor': BGCOLOR,
    })

if st.checkbox("Mostrar/Ocultar una de las soluciones"):
    fig_bp

"""
    En la siguiente parte de este ejercicio usaremos un mapa para continuar investigando que 
    tiene de especial Milpa Alta.
"""