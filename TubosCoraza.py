import streamlit as st
import pandas as pd
from CoolProp.CoolProp import PropsSI
import numpy as np


def TubosyCoraza():
    def M(t):
        return 25/1000*PropsSI('D','T',t+273.15,'P',560/760*101325,'Water')
    def Cp(t):
        return PropsSI('C','T',t+273.15,'P',560/760*101325,'Water')
    def k(t):
        return PropsSI('L','T',t+273.15,'P',560/760*101325,'Water')
    def rho(t):
        return PropsSI('D','T',t+273.15,'P',560/760*101325,'Water')
    def mu(t):
        return PropsSI('V','T',t+273.15,'P',560/760*101325,'Water') 
    Cp_prom = (Cp(17)+Cp(91))/2
    
    # ======================================================
    # PROPIEDADES GEOMÉTRICAS TUBOS Y CORAZA
    # ======================================================

    L = 0.60  # m

    # Coraza
    Di_coraza = 0.1615

    # Tubos
    Di_tubo = 0.01708
    Do_tubo = 0.02130

    # Número de tubos
    Ntubos = 16

    Ai = Ntubos*np.pi*Di_tubo*L
    Ao = Ntubos*np.pi*Do_tubo*L

    Ap = Ao/L

    Cp_prom = (Cp(20)+Cp(80))/2
    rho_prom = (rho(20)+rho(80))/2

    if "Configuracion_TC" not in st.session_state:
        st.session_state.Configuracion_TC = None

    
    # Pantalla de selección
    if st.session_state.Configuracion_TC is None:
        st.title("Intercambiadores de Tubos y Coraza")

        # TABLA 1: Datos comunes
        st.subheader("Especificaciones Generales")

        datos_tc = pd.DataFrame({
            "Parámetro": [
                "Material de la coraza",
                "Longitud de la coraza",
                "Diámetro interno de la coraza",
                "Diámetro externo de la coraza",
                "Material de los tubos",
                "Longitud de los tubos",
                "Diámetro interno de los tubos",
                "Diámetro externo de los tubos",
                "Diámetro conexiones",
                "Material de construcción"
            ],
            "Valor": [
                "Acero inoxidable 304",
                "60 cm",
                "16.15 cm",
                "16.83 cm",
                "Acero inoxidable 304",
                "60 cm",
                "1.708 cm",
                "2.13 cm",
                '1/2" Sch 10',
                "Acero inoxidable 304"            ]
            })
        
        st.table(datos_tc)
        
        # TABLA 2: Diferencias
        st.subheader("Configuraciones Disponibles")
        
        comparacion_tc = pd.DataFrame({
            "Configuración": [
                "Triangular 1 Paso",
                "Triangular 2 Pasos",
                "Triangular Sin Bafles",
                "Cuadrado 1 Paso"
            ],
            "Arreglo": [
                "Triangular",
                "Triangular",
                "Triangular",
                "Cuadrado"
            ],
            "Pasos": [1, 2, 1, 1],
            "Tubos": [16, 8, 16, 16],
            "Bafles": [9, 9, 0, 9]
        })
        
        st.table(comparacion_tc)
        
        st.divider()
        
        st.text("Seleccione la configuración")
    
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.image("Multimedia/Imagenes/trianbafles.png", width="stretch")

            if st.button("Pitch Triangular - 1 Paso", width="stretch"):
                st.session_state.Configuracion_TC = "Pitch Triangular - 1 Paso"
                st.rerun()

        with col2:
            st.image("Multimedia/Imagenes/trianbafles2.png", width="stretch")

            if st.button("Pitch Triangular - 2 Paso", width="stretch"):
                st.session_state.Configuracion_TC = "Pitch Triangular - 2 Paso"
                st.rerun()

        with col3:
            st.image("Multimedia/Imagenes/trianSINbafles.png", width="stretch")

            if st.button("Pitch Triangular - Sin Bafles", width="stretch"):
                st.session_state.Configuracion_TC = "Pitch Triangular - Sin Bafles"
                st.rerun()

        with col4:
            st.image("Multimedia/Imagenes/cuadbafles.png", width="stretch")

            if st.button("Pitch Cuadrado - 1 Paso", width="stretch"):
                st.session_state.Configuracion_TC = "Pitch Cuadrado - 1 Paso"
                st.rerun()
    
    else:

        if st.button("Cambiar configuración", width="stretch"):
            st.session_state.Configuracion_TC = None
            st.rerun()

        # ==========================================
        # CONFIGURACIÓN SELECCIONADA
        # ==========================================

        if st.session_state.Configuracion_TC == "Pitch Triangular - 1 Paso":

            ho_vapor = 1200
            hi_agua = 900
            ho_agua = 700
    
            Nt = 16
            Np = 1
            Nb = 9

        elif st.session_state.Configuracion_TC == "Pitch Triangular - 2 Paso":

            ho_vapor = 1400
            hi_agua = 1100
            ho_agua = 850
    
            Nt = 8
            Np = 2
            Nb = 9
    
        elif st.session_state.Configuracion_TC == "Pitch Triangular - Sin Bafles":
    
            ho_vapor = 700
            hi_agua = 600
            ho_agua = 350
    
            Nt = 16
            Np = 1
            Nb = 0
    
        elif st.session_state.Configuracion_TC == "Pitch Cuadrado - 1 Paso":
    
            ho_vapor = 1000
            hi_agua = 850
            ho_agua = 600
    
            Nt = 16
            Np = 1
            Nb = 9
    
        # ==========================================
        # DATOS DE OPERACIÓN
        # ==========================================
    
        st.subheader(st.session_state.Configuracion_TC)
    
        col1, col2 = st.columns(2)
    
        with col1:
            QAF = st.number_input(
                "Especifique el caudal del fluido frío (mL/s)",
                min_value=1,
                max_value=1000,
                step=1
            )
    
        with col2:
            TAF = st.slider(
                "Especifique la temperatura de ingreso del fluido frío (°C)",
                min_value=15,
                max_value=30,
                value=20,
                step=1
            )
    
        MetCal = st.selectbox(
            "Seleccione el fluido de calentamiento",
            ["Agua Caliente", "Vapor"]
        )
    
        if MetCal == "Agua Caliente":
    
            ConfigFlow = st.selectbox(
                "Seleccione la configuración de flujo",
                ["Paralelo", "Contraflujo"]
            )
    
            col1, col2 = st.columns(2)
    
            with col1:
                QAC = st.number_input(
                    "Especifique el caudal del fluido caliente (mL/s)",
                    min_value=1,
                    max_value=1000,
                    step=1
                )
    
            with col2:
                TAC = st.slider(
                    "Especifique la temperatura de ingreso del fluido caliente (°C)",
                    min_value=TAF + 1,
                    max_value=80,
                    value=max(TAF + 5, 40),
                    step=1
                )
    
        else:
    
            T_sat = st.slider(
                "Especifique la temperatura de ingreso del vapor (°C)",
                min_value=93,
                max_value=150,
                value=120,
                step=1
            )
    
        # ==========================================
        # BOTÓN DE SIMULACIÓN
        # ==========================================
    
        
    if st.button("Correr Simulación"):

        st.success(
            "Esta simulación predice datos reales."
        )

        # =====================================================
        # VAPOR POR LOS TUBOS
        # =====================================================

        if MetCal == "Vapor":

            # Fluido frío por coraza
            w = QAF/1e6 * rho_prom

            # Para vapor se desprecia la resistencia interna
            U = ho_vapor

            t1 = TAF

            # Temperatura de ebullición a presión de operación
            T_eb = PropsSI(
                'T',
                'P',
                560*101325/760,
                'Q',
                0,
                'Water'
            ) - 273.15
    
            def f(t):
    
                return (
                    U*Ap/(w*Cp_prom)
                )*(
                    T_sat - t
                )
    
            h = 0.001
    
            x = 0
            t = t1
    
            Longitud = [0]
            temp = [t]
    
            evaporacion = False
            L_evap = None
    
            while x < L:
    
                k1 = f(t)
                k2 = f(t + 0.5*h*k1)
                k3 = f(t + 0.5*h*k2)
                k4 = f(t + h*k3)
    
                t = t + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    
                x += h
    
                if t >= T_eb:
    
                    t = T_eb
    
                    temp.append(t)
                    Longitud.append(x)
    
                    evaporacion = True
                    L_evap = x
    
                    break
    
                temp.append(t)
                Longitud.append(x)
    
            # Vapor a temperatura constante
    
            Temp = [T_sat for _ in Longitud]
    
            # ==========================================
            # GRÁFICA
            # ==========================================
    
            n_puntos = 50
            paso = max(1, len(Longitud)//n_puntos)
    
            Longitud_plot = Longitud[::paso]
            temp_plot = temp[::paso]
            Temp_plot = Temp[::paso]
    
            placeholder = st.empty()
    
            for i in range(2, len(Longitud_plot)+1):
    
                df = pd.DataFrame({
                    "Longitud (m)": Longitud_plot[:i],
                    "Fluido frío (°C)": temp_plot[:i],
                    "Vapor (°C)": Temp_plot[:i]
                })
    
                placeholder.line_chart(
                    df,
                    x="Longitud (m)",
                    y=[
                        "Fluido frío (°C)",
                        "Vapor (°C)"
                    ]
                )
    
            # ==========================================
            # RESULTADOS
            # ==========================================
    
            if evaporacion:
    
                st.warning(
                    f"El fluido frío alcanzó la temperatura de ebullición "
                    f"({T_eb:.1f} °C) a una longitud aproximada de "
                    f"{L_evap:.3f} m."
                )
    
                st.warning(
                    "La simulación se detuvo en ese punto ya que, a partir de allí, "
                    "comenzaría el cambio de fase."
                )
    
                st.warning(
                    "Se recomienda no operar el equipo bajo las condiciones "
                    "especificadas. La generación de vapor en el lado originalmente "
                    "destinado al agua líquida puede afectar el desempeño térmico "
                    "y acelerar fenómenos de corrosión."
                )
    
            else:
    
                col1, col2 = st.columns(2)
    
                with col1:
    
                    st.info(
                        f"Fluido frío: "
                        f"t₁ = {t1:.1f} °C , "
                        f"t₂ = {temp[-1]:.1f} °C"
                    )
    
                with col2:
    
                    st.info(
                        f"Vapor: "
                        f"T = {T_sat:.1f} °C"
                    )
            st.info("El perfil de temperatura se obtiene a partir de datos teóricos, las unicas temperaturas representativas son las temperaturas de entrada y salida del equipo. ")
    
        # =====================================================
        # AGUA CALIENTE
        # =====================================================
    
        elif MetCal == "Agua Caliente":
    
            pass
    
        
                
