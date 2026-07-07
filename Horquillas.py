import streamlit as st
from CoolProp.CoolProp import PropsSI
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go


def horquillas():
    hi_Tub_Conc= 200
    ho_Tub_Conc= 300
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
    k_prom = (k(17)+k(91))/2
    rho_prom = (rho(17)+rho(91))/2
    mu_prom = (mu(20)+mu(91))/2
    
    #Datos de los tubos 
    #Tubo externo
    di_tuex = 4.276 /100 #m
    do_tuex = 4.830 /100 #m
    #Tubo interno
    di_tuin = 2.130 /100 #m
    do_tuin = 2.708 /100 #m
    #Áreas transversales de los espacios
    At_tuin = np.pi*(di_tuin/2)**2 #m^2
    At_anulo = np.pi*(di_tuex/2)**2 - np.pi*(do_tuin/2)**2 #m^2 de anulo
    
    # Area de 8 secciones de 1 metro cada una
    L = 8 #m etros
    Ai = L*np.pi*di_tuin
    Ao = L*np.pi*do_tuin
    
    #Area de transferencia por unidad de longitud
    Ap = np.pi*do_tuin
    
    col1, col2 = st.columns(2)
    with col1:
        FAF = st.number_input("Ingrese el flujo de Agua fria (mL/s)", min_value=1 ,max_value=5000,step=1)
        w = FAF/1e6 * rho_prom

        TAF = st.slider("Especifique la temperatura de ingreso del agua fria (°C)",
                            min_value= 15,
                            max_value= 30,
                            value = 20,
                            step = 1
                        )
    with col2:
        df = pd.DataFrame({
            "Especificación": [
                "Diámetro externo tubo interno",
                "Diámetro interno tubo externo",
                "Número de secciones",
                "Longitud total"
                ],
            "Valor": [
                "2.708 cm",
                "4.276 cm",
                "8",
                "8 m"
            ]
        })
        st.table(df) ## Visualizaicón especificaciones    
    
    FS = st.selectbox("Seleccione la utilidad térmica", ["Vapor","Agua Caliente"],key="uter") # //// Especificar el fluido térmico
    
    if st.session_state.uter == "Agua Caliente": 
        col1, col2 = st.columns(2)
        with col1:    
            FAC = st.number_input("Ingrese el flujo de Agua caliente (mL/s)",min_value=1,max_value=5000,step=1)

        with col2:
            TAC = st.slider("Ingrese la temperatura del Agua Caliente (°C): ",min_value=TAF+1,max_value=80,step=1)
        Configflow = st.selectbox("Especifique la configuración de flujo",["Contraflujo","Paralelo"])
        ##Conversion de flujo volumetrico a flujo másico
        W = FAC/1e6 * rho_prom
        ### Código para estimar los coeficientes convecticos en función del flujo
        U = ((hi_Tub_Conc*Ai/Ao)**-1 + ho_Tub_Conc**-1)**-1
        
        if st.button("Correr simulación") == True:
            st.warning("Esta simulación se basa en datos teóricos, sube tus datos experimentales para predecir el comportamiento real.")
            if Configflow == "Contraflujo":
                t1 = TAF
            
                # Limites T2 para bisección
                T2_min = t1
                T2_max = TAC
            
                h_paso = 0.01 #Tamaño de paso
                tol = 1e-03 #toleración error
                error = 1
            
                while error > tol:
                    T2 = 0.5*(T2_min+T2_max)
                
                    def f(t):
                        return (U*Ap/(w*Cp_prom))*(T2 + w/W*(t-t1)-t)
            
                    #Condiciones iniciales RK4
                    h = 0.01
                    theta = 0
                    t = t1
                    Longitud = [0]
                    temp = [t]

                    while theta < L:
                        k1 = f(t)
                        k2 = f(t + 0.5*h*k1)
                        k3 = f(t + 0.5*h*k2)
                        k4 = f(t + h*k3)

                        t = t + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
                        theta += h

                        temp.append(t)
                        Longitud.append(theta)
                    t2 = temp[-1]
                    T1_calc = T2 + w/W*(t2-t1)
                    error = abs(T1_calc - TAC)
                # ajuste bisección
                    if T1_calc > TAC:
                        T2_max = T2
                    else:
                        T2_min = T2
            
                Temp = [T2 + (w/W)*(t - t1) for t in temp]
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
                        "Fluido caliente (°C)": Temp_plot[:i]
                    })

                    placeholder.line_chart(
                        df,
                        x="Longitud (m)",
                        y=["Fluido frío (°C)", "Fluido caliente (°C)"]
                    )

                    #time.sleep(0.05)  # opcional para visualizar la animación
                col1 , col2 =st.columns(2)
                with col1:                
                    st.info(f"Fluido frio: t1= {t1:.1f} °C , t2= {temp[-1]:.1f} °C")
                with col2:    
                    st.info(f"Fluido Térmico: T1= {Temp[-1]:.1f} °C , T2= {Temp[0]:.1f} °C")
            elif Configflow == "Paralelo":
                t1 = TAF
                T1 = TAC

                # límites para bisección de t2
                t2_min = t1
                t2_max = T1

                h = 0.01
                tol = 1e-3
                error = 1
            
                U = ((hi_Tub_Conc*Ai/Ao)**-1 + ho_Tub_Conc**-1)**-1

                while error > tol:

                    t2 = 0.5*(t2_min + t2_max)

                    # balance global para calcular T2
                    T2 = T1 - (w/W)*(t2 - t1)

                    def f(t):
                        return (U*Ap/(w*Cp_prom))*(T2 + (w/W)*(t2 - t) - t)

                    # condiciones iniciales
                    theta = 0
                    t = t1

                    Longitud = [0]
                    temp = [t]

                    while theta < L:

                        k1 = f(t)
                        k2 = f(t + 0.5*h*k1)
                        k3 = f(t + 0.5*h*k2)
                        k4 = f(t + h*k3)

                        t = t + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

                        theta += h

                        temp.append(t)
                        Longitud.append(theta)

                    t2_calc = temp[-1]

                    error = abs(t2_calc - t2)

                    if t2_calc > t2:
                        t2_min = t2
                    else:
                        t2_max = t2

                # perfil temperatura caliente
                Temp = [T2 + (w/W)*(t2 - t) for t in temp]
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
                        "Fluido caliente (°C)": Temp_plot[:i]
                    })

                    placeholder.line_chart(
                        df,
                        x="Longitud (m)",
                        y=["Fluido frío (°C)", "Fluido caliente (°C)"]
                    )

                    #time.sleep(0.05)  # opcional para visualizar la animación
                col1 , col2 =st.columns(2)
                with col1:                
                    st.info(f"Fluido frio: t1= {t1:.1f} °C , t2= {temp[-1]:.1f} °C")
                with col2:    
                    st.info(f"Fluido Térmico: T1= {Temp[0]:.1f} °C , T2= {Temp[-1]:.1f} °C")
        
    elif st.session_state.uter == "Vapor":
        
        U = ((hi_Tub_Conc*Ai/Ao)**-1 + ho_Tub_Conc**-1)**-1
        Ts = st.slider("Especifique la temperatura del vapor (°C)",min_value=92,max_value=150,step=1)
        T_eb = 91.6
        if st.button("Correr simulación") == True:
            st.success("Esta simulación predice datos reales.")
            t1 = TAF

            h = 0.01

            def f(t):
                return (U*Ap/(w*Cp_prom))*(Ts - t)

            theta = 0
            t = t1

            Longitud = [0]
            temp = [t]

            
            evaporacion = False
            L_evap = None

            while theta < L:

                k1 = f(t)
                k2 = f(t + 0.5*h*k1)
                k3 = f(t + 0.5*h*k2)
                k4 = f(t + h*k3)

                t = t + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

                theta += h

                if t >= T_eb:
                    t = T_eb

                    temp.append(t)
                    Longitud.append(theta)

                    evaporacion = True
                    L_evap = theta

                    break

                temp.append(t)
                Longitud.append(theta)
    
            # temperatura vapor constante
            Temp = [Ts for i in Longitud]
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
                    y=["Fluido frío (°C)", "Vapor (°C)"]
                )

            #time.sleep(0.05)  # opcional para visualizar la animación
            if evaporacion:
                st.warning(
                    f"El fluido frío alcanzó su temperatura de ebullición "
                    f"({T_eb:.1f} °C) a una longitud aproximada de "
                    f"{L_evap:.2f} m.\nLa simulación se detuvo en ese punto "
                    f"ya que a partir de allí comenzaría el cambio de fase."
                )
                st.warning("Se recomienda no operar el equipo bajo las condiciones especificadas. Los resultados indican generación de vapor en el ánulo, zona originalmente destinada al flujo de agua líquida. Esta condición puede incrementar los efectos de corrosión y acelerar el desgaste de los componentes del equipo.")
            else:
                col1 , col2 =st.columns(2)
                with col1:                
                    st.info(f"Fluido frio: t1= {t1:.1f} °C , t2= {temp[-1]:.1f} °C")
                with col2:    
                    st.info(f"Vapor: T1= {Temp[0]:.1f} °C , T2= {Temp[-1]:.1f} °C")
        
    
    