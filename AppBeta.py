import streamlit as st
import pandas as pd
import numpy as np
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import base64
from PIL import Image


### FORMATO PARA VISUALIZACIÓN DE LA PÁGINA
st.markdown("""
    <style>
    /* Fondo principal de la interfaz */
    .css-1v3fvcr {
        background-color: #3c3cb9; /* Blanco */
        color: black; /* Texto negro */
    }

    /* Botones de la barra lateral */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #1C1C1C; /* Negro */
        color: white; /* Texto blanco */
        border-radius: 5px; /* Bordes redondeados */
        border: 1px solid white; /* Borde blanco */
        font-size: 16px; /* Tamaño del texto */
        margin: 10px 0; /* Espaciado entre botones */
    }

    /* Hover de los botones */
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #4682B4; /* Azul acero claro */
        color: white; /* Texto blanco */
        border: 1px solid #1E90FF; /* Borde azul brillante */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Hover de todos los botones */
    .stButton > button:hover {
        background-color: #4682B4; /* Azul acero claro */
        color: white; /* Texto blanco */
        border: 1px solid #1E90FF; /* Borde azul brillante */
    }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(layout="wide")

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
    
def inicio():    
    st.write("# Bienvenido al Banco de Intercambiadores Digital")
    st.write("##### Un gemelo digital del banco de intercambiadores de calor del laboratorio de ingeniería quimica de la UNAL, para aprender, enseñar y entrenar la transferencia de calor.")
    st.write("## Instructivo del Gemelo Digital")
    st.video("https://youtu.be/TU8fJsVeWc0")

def informacion_general():
    st.write("# Información General")
    st.write("### Entender el calor antes de entender la máquina")
    st.markdown(
    """
    <p style='text-align: justify;'>
    Este apartado explica, en pocas palabras, qué son los intercambiadores de calor, por qué decidimos construir un gemelo digital del banco BIC-1 y cómo esta herramienta resulta útil tanto en el aula como en la industria. Está pensado para tres tipos de lector: estudiantes, profesores y empresas y para cualquiera que quiera entender el tema y valorar lo que estamos desarrollando.
    </p>
    """,
    unsafe_allow_html=True)
    
    st.image("Multimedia/Imagenes/banco.jpeg",width="stretch")
    
    if "infogen" not in st.session_state:
        st.session_state.infogen = "basico"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Lo básico", width="stretch"):
            st.session_state.infogen = "basico"

    with col2:
        if st.button("Nuestra solución", width="stretch"):
            st.session_state.infogen = "solucion"

    with col3:
        if st.button("Funcionamiento", width="stretch"):
            st.session_state.infogen = "funcionamiento"

    with col4:
        if st.button("¿Qué ganas tú?", width="stretch"):
            st.session_state.infogen = "ganas"

    # Mostrar contenido según la página seleccionada
    if st.session_state.infogen == "basico":
        st.header("¿Qué es, y para qué sirve, un intercambiador de calor?")
        st.markdown(
        """
        <p style='text-align: justify;'>
        Es un equipo que transfiere energía térmica entre dos fluidos a temperaturas distintas sin que
        lleguen a mezclarse: circulan separados por una superficie sólida y, a través de ella, el fluido 
        caliente cede calor al frío. El principio es sencillo, pero el control de la temperatura es uno de los
        factores que más pesa en cualquier proceso, y por eso estos equipos están presentes en
        prácticamente toda planta industrial.
        </p>
        """,
        unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: justify;'>
        Cuánto calor se transfiere depende de tres cosas, resumidas en la conocida relación Q̇ = U·A·ΔTm:
        el área de contacto A, la diferencia de temperaturas ΔTm que actúa como fuerza impulsora y el
        coeficiente global U, que mide la facilidad con que el calor atraviesa el equipo. Es justamente
        este coeficiente el que distingue el comportamiento de un tipo de intercambiador frente a otro.
        </p>
        """,
        unsafe_allow_html=True)
        
        st.header("Está en casi todo lo que se produce")
        st.markdown(
        """
        <p style='text-align: justify;'>
        Calentar, enfriar, condensar, evaporar o recuperar la energía de una corriente para precalentar otra
        son tareas diarias en la industria, y todas dependen de estos equipos. Como buena parte del
        consumo energético de un proceso se concentra en ellas, operarlos bien se traduce directamente en
        ahorro de energía, menores costos y una huella ambiental más baja. Los encontramos en la
        refinación, la petroquímica, la industria de alimentos y bebidas, la farmacéutica, la generación de
        energía, los sistemas de climatización y el tratamiento de aguas, entre muchos otros campos.
        </p>
        """,
        unsafe_allow_html=True)
        
        st.markdown(
        """
        <p style='text-align: justify;'>
        Existe un tipo de intercambiador para cada necesidad y, dentro de cada uno, la configuración
        interna (el arreglo de los tubos, el uso de deflectores, el número de pasos y la elección entre flujo
        en paralelo o en contracorriente) cambia por completo el resultado. Esa riqueza de
        combinaciones es justamente lo que hace exigente aprender el tema.
        </p>
        """,
        unsafe_allow_html=True)
        
        
    if st.session_state.infogen == "solucion":
        st.header("¿Por qué decidimos hacer un gemelo digital?")
        st.markdown(
        """
        <p style='text-align: justify;'>
        Un gemelo digital es una réplica virtual de un equipo real, capaz de reproducir su comportamiento
        y apoyar el análisis. Nació en el contexto de la Industria 4.0 y hoy se usa también para enseñar,
        porque permite interactuar con un modelo fiel del equipo antes de tocar la máquina
        </p>
        """,
        unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: justify;'>
        El banco BIC-1 es un equipo completo: reúne cuatro intercambiadores de coraza y tubos con
        arreglos distintos, un sistema de tubos concéntricos, un intercambiador de placas y un tanque 
        porque permite interactuar con un modelo fiel del equipo antes de tocar la máquina
        agitado, todos en acero inoxidable 304 y con la misma área de transferencia para poder
        compararlos. En conjunto habilita 38 experimentos, con vapor o agua caliente y operación en
        paralelo o en contracorriente. Es potente, pero también abrumador para quien llega por primera
        vez: la red de válvulas y configuraciones es difícil de leer en el poco tiempo de una práctica de
        laboratorio.
        </p>
        """,
        unsafe_allow_html=True)
        #st.image("Multimedia/Imagenes/21de21.png",width="stretch")
        
        st.markdown(
        """
        <p style='text-align: justify;'>
        La conclusión fue clara: el problema es real y se siente justo en el punto donde la teoría debería
        conectarse con la operación. Ahí decidimos construir la herramienta.
        </p>
        """,
        unsafe_allow_html=True)        
    
    if st.session_state.infogen == "funcionamiento":
        st.header("Un puente entre el equipo real y quien aprende")
        st.markdown(
        """
        <p style='text-align: justify;'>
        El gemelo digital del banco BIC-1 cumple tres funciones que se refuerzan entre sí:
        </p>
        """,
        unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: justify;'>
        Ver. Ofrece una representación visual y en 3D del banco, de modo que el usuario reconoce cada
        unidad, sigue el recorrido de los fluidos e identifica la función de cada válvula sin necesidad de
        estar frente a la máquina
        </p>
        """,
        unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: justify;'>
        Simular. Reproduce las distintas configuraciones (tipo de intercambiador, arreglo de flujo,
        servicio de calentamiento) y anticipa qué ocurre con las temperaturas y la transferencia de calor
        en cada escenario.
        </p>
        """,
        unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: justify;'>
        Conectar. Sirve de guía para relacionar la teoría con la operación real y con la interpretación de
        los resultados, que es donde aparecen las mayores barreras.
        </p>
        """,
        unsafe_allow_html=True)
        
    if st.session_state.infogen == "ganas":
        st.header("¿Qué gana cada quien?")

        st.markdown(
        """
        <p style='text-align: justify;'>
        El valor del gemelo digital cambia según quién lo utilice, pero en todos los casos busca reducir
        la distancia entre el conocimiento teórico y la operación real del equipo.
        </p>
        """,
        unsafe_allow_html=True)

        st.subheader("Para estudiantes")

        st.markdown(
        """
        <p style='text-align: justify;'>
        • Entender válvulas, corrientes y configuraciones antes de la práctica.<br>
        • Explorar distintos escenarios sin miedo a equivocarse.<br>
        • Relacionar la teoría con lo que se observa en los resultados.
        </p>
        """,
        unsafe_allow_html=True)

        st.subheader("Para profesores")

        st.markdown(
        """
        <p style='text-align: justify;'>
        • Preparar y estandarizar la práctica con un mismo material de apoyo.<br>
        • Evaluar la comprensión previa antes de la sesión de laboratorio.<br>
        • Dedicar el tiempo de laboratorio a lo que de verdad importa.
        </p>
        """,
        unsafe_allow_html=True)

        st.subheader("Para empresas")

        st.markdown(
        """
        <p style='text-align: justify;'>
        • Capacitar operarios y agilizar su incorporación en un entorno seguro.<br>
        • Reducir errores, desgaste y riesgo sobre el equipo real.<br>
        • Adaptar la misma lógica a otros equipos de transferencia de calor.
        </p>
        """,
        unsafe_allow_html=True)

        st.markdown(
        """
        <p style='text-align: justify;'>
        La evidencia internacional respalda esta dirección. Experiencias recientes en laboratorios de
        ingeniería de procesos muestran que los gemelos digitales mejoran la comprensión y la confianza
        de los usuarios frente a sistemas complejos (Boettcher et al., 2023).
        </p>
        """,
        unsafe_allow_html=True)

    st.write("### ¿Le interesa lo que estamos construyendo?")
    st.markdown(
        """
        <p style='text-align: justify;'>
        Lo que desarrollamos es una herramienta sencilla de usar, pero sólida en su fundamento: se apoya
        en relaciones físicas consistentes, se estructura de forma modular en Python y está pensada para
        alojarse en una página web de acceso libre. Esa arquitectura la hace fácil de distribuir y, sobre
        todo, transferible a otros equipos y operaciones.
        </p>
        """,
        unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: justify;'>
        Si su organización forma estudiantes, capacita operarios o trabaja con equipos de transferencia de
        calor, creemos que esta propuesta puede aportar. Estaremos encantados de conversar sobre cómo
        adaptarla a su contexto.
        </p>
        """,
        unsafe_allow_html=True)


    
    

## Coidgo base simluación, el contenido de paginas se programa en otro archivo
def simulacion():
    from TanqueAgitado import Tanque_Agitado
    from Horquillas import horquillas
    from TubosCoraza import TubosyCoraza
    
    st.write("# Simulación")

    if "Equipo" not in st.session_state:
        st.session_state.Equipo = "inicio"
    
    if st.session_state.Equipo == "inicio":
        st.text("Seleccione un equipo")
        col1,col2, col3 = st.columns(3)
        with col1:
            st.image(Image.open("Multimedia/Imagenes/Tanque agitado.jpeg"),width="stretch")
            if st.button("Tanque Agitado",width="stretch"):
                st.session_state.Equipo = "Tanque Agitado"
                st.rerun()
        with col2:
            st.image(Image.open("Multimedia/Imagenes/Horquillas.jpeg"),width="stretch")
            if st.button("Horquillas",width="stretch"):
                st.session_state.Equipo = "Horquillas"
                st.rerun()
        with col3:
            st.image(Image.open("Multimedia/Imagenes/Tubos y corazas.jpeg"),width="stretch")
            if st.button("Tubos y Coraza",width="stretch"):
                st.session_state.Equipo = "Tubos y Coraza"
                st.rerun()
            
    elif st.session_state.Equipo == "Tanque Agitado":
        col1,col2 = st.columns([7,1])
        with col1:
            st.markdown("### <u>Tanque Agitado</u>", unsafe_allow_html=True)
        with col2:
            if st.button("Volver",width="stretch"):
                st.session_state.Equipo = "inicio"
                st.rerun()
        Tanque_Agitado()
    
    elif st.session_state.Equipo == "Horquillas":
        col1,col2 = st.columns([7,1])
        with col1:
            st.markdown("### <u>Horquillas (Tubos Concentricos)</u>", unsafe_allow_html=True)
        with col2:
            if st.button("Volver",width="stretch"):
                st.session_state.Equipo = "inicio"
                st.rerun()
        horquillas()
    elif st.session_state.Equipo == "Tubos y Coraza":
        col1,col2 = st.columns([7,1])
        with col1:
            st.markdown("### <u>Tubos y Coraza</u>", unsafe_allow_html=True)
        with col2:
            if st.button("Volver",width="stretch"):
                st.session_state.Equipo = "inicio"
                st.rerun()
        TubosyCoraza()
            
def documentacion():
    import os
    st.write("# Documentación")
    if "pdf_actual" not in st.session_state:
        st.session_state.pdf_actual = None

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Manual de Operación", width="stretch"):
            st.session_state.pdf_actual = "MANUAL DE OPERACION.pdf"

    with col2:
        if st.button("P&ID", width="stretch"):
            st.session_state.pdf_actual = "p&d.pdf"

    with col3:
        if st.button("Diagrama de flujo", width="stretch"):
            st.session_state.pdf_actual = None
            st.write("Proximamente...")
    # Mostrar únicamente el PDF seleccionado
    if st.session_state.pdf_actual is not None:
        with open(st.session_state.pdf_actual, "rb") as f:
            pdf_bytes = f.read()

        st.pdf(pdf_bytes)
        # Botón para descargar el PDF
        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_bytes,
            file_name=os.path.basename(st.session_state.pdf_actual),
            mime="application/pdf",
            width="stretch"
        )
        
def guia_usuario():
    st.write("# Guia Usuario")
    st.write("## Caracteristicas y Guia de Operación del Equipo")
    st.video("https://youtu.be/SD0bnFhfyRk")
    st.write("## Instructivo del Gemelo Digital")
    # Videos
    # with open("Multimedia/Videos/Guia de operación.mp4", "rb") as video_file:
    #     st.video(video_file.read())
def encuesta():
    st.write("# Encuesta de Percepción")
    st.components.v1.iframe(
    "https://docs.google.com/forms/d/e/1FAIpQLScqpIZ8ArdRp8L85sKQ_SCTrPimu7G3ChCBOddT68U7GNsMmw/viewform?embedded=true",
    height=500,
    scrolling=True
    )



# MENU DE NAVEGACIÓN
img = Image.open("Multimedia/Imagenes/LogoUnal.png")
st.sidebar.image(img)

st.sidebar.write("## Menú de Navegación")
# PÁGINA PRINCIPAL
    
if st.sidebar.button("Inicio",width="stretch"):
    st.session_state.pagina = "inicio"
if st.sidebar.button("Información General",width="stretch"):
    st.session_state.pagina = "informacion_general"

if st.sidebar.button("Simulación",width="stretch"):
    st.session_state.pagina = "Simulación"
    st.session_state.Equipo = "inicio"
    
if st.sidebar.button("Documentación",width="stretch"):
    st.session_state.pagina = "Documentacion"

if st.sidebar.button("Guia de Usuario",width="stretch"):
    st.session_state.pagina = "Guia de Usuario"

if st.sidebar.button("Encuesta de Percepción",width="stretch"):
    st.session_state.pagina = "encuesta"






# PAGINAS
if st.session_state.pagina == "inicio":
    inicio()
elif st.session_state.pagina == "informacion_general":
    informacion_general()
elif st.session_state.pagina == "Simulación":
    simulacion()
elif st.session_state.pagina == "Documentacion":
    documentacion()
elif st.session_state.pagina == "Guia de Usuario":
    guia_usuario()
elif st.session_state.pagina == "encuesta":
    encuesta()
