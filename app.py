import streamlit as st
import pandas as pd
import plotly.express as px


# Configuración de la página
st.set_page_config(
    page_title="Businness Case Dashboard",
    page_icon="💰",
    layout="wide",
)

# Título del Dashboard
st.title("Dashboard - 2023")

# Cargar el dataset
df = pd.read_csv('data/database.csv')

# Crear una nueva columna con el año y mes
df[['ANO', 'MES']] = df['ANO_MES'].str.split('-', expand=True)

# Agregar un subtitulo
st.subheader("Información General")

# Crear una sección con dos columnas y 2 filas
col_1, col_2 = st.columns(2,gap='medium')
col_3, col_4 = st.columns(2,gap='medium')


#Calcular y mostrar el total de ventas
total_sales = df['VENTAS'].sum()
col_1.metric(
    label="Total Ventas",
    value=f"{total_sales:,} COP",
    border=True
)

#Calcular y mostrar el número de transacciones
number_transaction = len(df)
col_2.metric(
    label="No. de Transacciones",
    value=f"{number_transaction:,}",
    border=True
)

# Calcular y mostrar el mejor y peor retailer
sales_by_retailer = df.groupby('RETAILER')['VENTAS'].sum().reset_index().sort_values(by='VENTAS',ascending=False) # Agrupar por retailer y sumar las ventas
best_retailer = sales_by_retailer.iloc[0] # Mejor retailer
worst_retailer = sales_by_retailer.iloc[-1] # Peor retailer


# Mostrar el mejor Retailer
col_3.metric(
    label=f"Mejor Retailer: {best_retailer['RETAILER']}",
    value=f"{best_retailer['VENTAS']:,} COP",
    border=True,
)

# Mostrar el peor Retailer
col_4.metric(
    label=f"Último Retailer: {worst_retailer['RETAILER']}",
    value=f"{worst_retailer['VENTAS']:,} COP",
    border=True,
)

st.subheader("Porcentaje de Ventas x Retailer y Categoria")

col_1, col_2 = st.columns(2,gap='medium')

with col_1:
    st.text("Se muestran los retailers que ocupan un porcentaje mayor al 2%")

    # Filtrar los retailers que ocupan un porcentaje menor al 2%
    sales_by_retailer['PERCENT'] = sales_by_retailer['VENTAS'] / sales_by_retailer['VENTAS'].sum() * 100
    filtered_sales_by_retailer = sales_by_retailer[sales_by_retailer['PERCENT'] >= 2]

    # Crear el gráfico de pastel
    fig = px.pie(filtered_sales_by_retailer, values='VENTAS', names='RETAILER')

    st.plotly_chart(fig)

with col_2:
    # Calcular y mostrar las ventas por categoría
    sales_by_category = df.groupby('CATEGORIA_3')['VENTAS'].sum().reset_index()

    fig = px.pie(sales_by_category, values='VENTAS', names='CATEGORIA_3')

    st.plotly_chart(fig)

st.subheader("Rendimiento de las Ventas por Mes")

col_1, col_2 = st.columns(2,gap='medium')

with col_1:
    # Calcular y mostrar las ventas por mes
    sales_by_month = df.groupby('MES')['VENTAS'].sum().reset_index()

    # Diccionario con los nombres de los meses
    months_dictionary = {
        '01':'Enero',
        '02':'Febrero',
        '03':'Marzo',
        '04':'Abril',
        '05':'Mayo',
        '06':'Junio',
        '07':'Julio',
        '08':'Agosto',
        '09':'Septiembre',
        '10':'Octubre',
        '11':'Noviembre',
        '12':'Diciembre'
    }

    # Cambiar el formato de los meses a texto
    sales_by_month['MES'] = sales_by_month['MES'].map(months_dictionary)

    # Creamos una figur que muestre las ventas por mes en un gráfico de barras
    fig = px.bar(sales_by_month, x='MES', y='VENTAS', title='Ventas por Mes')

    # Agregar una línea que muestre el comportamiento de las ventas
    fig.add_scatter(
        x=sales_by_month['MES'],
        y=sales_by_month['VENTAS'],
        name='Tendencia',  # Nombre de la línea
        line=dict(color='red', width=2)  
    )

    st.plotly_chart(fig)


with col_2:
    # Mostrar las métricas de las ventas por mes
    st.metric(
        value=f"{sales_by_month['VENTAS'].mean():,.2f} COP",
        label="Promedio de Ventas",
        border=True
    )
    st.metric(
        value=f"{sales_by_month['VENTAS'].max():,.2f} COP",
        label=f"Mejor Mes: {sales_by_month['MES'][sales_by_month['VENTAS'].idxmax()]}",
        border=True
    )
    st.metric(
        value=f"{sales_by_month['VENTAS'].min():,.2f} COP",
        label=f"Mes con menos Ventas: {sales_by_month['MES'][sales_by_month['VENTAS'].idxmin()]}",
        border=True
    )

# Agregar un selector para elegir un retailer
retailer = st.selectbox(
    options=df['RETAILER'].unique(), # Opciones del selector
    label='Selecciona un Retailer'
)

# Filtrar las ventas por retailer
retailer_sales_by_month = df[df['RETAILER'] == retailer].groupby('MES')['VENTAS'].sum().reset_index()

col_1, col_2 = st.columns(2,gap='medium')

with col_1:

    # Cambiar el formato de los meses a texto
    retailer_sales_by_month['MES'] = retailer_sales_by_month['MES'].map(months_dictionary)
    
    # Crear un gráfico de barras con las ventas por mes del retailer seleccionado
    fig = px.bar(retailer_sales_by_month,x='MES', y='VENTAS', title=f"Ventas x Mes {retailer}")

    fig.add_scatter(
        x=retailer_sales_by_month['MES'],
        y=retailer_sales_by_month['VENTAS'],
        name='Tendencia',  # Nombre de la línea
        line=dict(color='red', width=2)  
    )

    st.plotly_chart(fig)

with col_2:
    # Mostrar las métricas de las ventas por mes del retailer seleccionado
    st.metric(
        value=f"{retailer_sales_by_month['VENTAS'].mean():,.2f} COP",
        label="Promedio de Ventas",
        border=True
    )
    st.metric(
        value=f"{retailer_sales_by_month['VENTAS'].max():,.2f} COP",
        label=f"Mejor Mes: {retailer_sales_by_month['MES'][retailer_sales_by_month['VENTAS'].idxmax()]}",
        border=True
    )
    st.metric(
        value=f"{retailer_sales_by_month['VENTAS'].min():,.2f} COP",
        label=f"Mes con menos Ventas: {retailer_sales_by_month['MES'][retailer_sales_by_month['VENTAS'].idxmin()]}",
        border=True
    )

st.subheader("Ventas x Días de la Semana")

col_1, col_2 = st.columns(2,gap='medium')

# Calcular y mostrar las ventas por día de la semana
sales_by_day = df.groupby('DAY_NAME')['VENTAS'].sum().reset_index()

with col_1:
    fig = px.bar(sales_by_day, x='DAY_NAME', y='VENTAS', title='Ventas por Día de la Semana')

    # Agregar una línea que muestre el comportamiento de las ventas
    fig.add_scatter(
    x=sales_by_day['DAY_NAME'],
    y=sales_by_day['VENTAS'],
    name='Tendencia',  
    line=dict(color='red', width=2)  
    )

    st.plotly_chart(fig)

with col_2:
    # Mostrar las métricas de las ventas por día de la semana
    st.metric(
        value=f"{sales_by_day['VENTAS'].mean():,.2f} COP",
        label="Promedio de Ventas",
        border=True
    )
    st.metric(
        value=f"{sales_by_day['VENTAS'].max():,.2f} COP",
        label=f"Mejor Día: {sales_by_day['DAY_NAME'][sales_by_day['VENTAS'].idxmax()]}",
        border=True
    )
    st.metric(
        value=f"{sales_by_day['VENTAS'].min():,.2f} COP",
        label=f"Día con menos Ventas: {sales_by_day['DAY_NAME'][sales_by_day['VENTAS'].idxmin()]}",
        border=True
    )