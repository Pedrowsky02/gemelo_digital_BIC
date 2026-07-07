import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
from scipy.stats import linregress
import time

def Tanque_Agitado():
    A_serp = 0.4
    A_chaq = 0.4
    psi_pascal =  6894.76
    
    def Cp(t):
        return PropsSI('C','T',t+273.15,'P',560/760*101325,'Water')
    def rho(t):
        return PropsSI('D','T',t+273.15,'P',560/760*101325,'Water') 
    
    ## PRIMERO TRES INPUTS E INFORMACIÓN DEL EQUIPO
    col1, col2 = st.columns(2)
    with col1:
        State = st.selectbox("Seleccione el modo de operación",["Batch","Semibatch"])
        ModAgi = st.selectbox("Seleccione el modo de agitación", ["Sin Agitación","Mecánica"]) 
    MetCal = st.selectbox("Seleccione el método de calentamiento", ["Serpentin","Chaqueta"])
    with col2:
        df = pd.DataFrame({
            "Especificación": [
                "Diámetro Tanque",
                "Diámetro Impulsor (Paleta de agitación)",
                "Capacidad Tanque",
                "Utilidad Térmica"
                ],
            "Valor": [
                "~0.30 m",
                "~0.14 m",
                "~30 L",
                "Vapor"
            ]
        })
        st.table(df) ## Visualizaicón especificaciones
    
    ## Input temperatura vapor    
    T_sat = float(st.slider("Especifique la temperatura de entrada del vapor (°C)",
                      min_value= 95,
                      max_value= 130,
                      value = 110,
                      step = 1
                      ))
    ## RPM'S
    if ModAgi == "Mecánica":
        N_rev = float(st.slider("Especifique las rpm del impulsor (1/min)",
                      min_value= 5,
                      max_value= 80,
                      value = 40,
                      step = 1
                      ))
    
    ## DESARROLLO DE SIMULACIÓN
    if State == "Batch":
        ValCon1 = st.selectbox("Seleccione el desarrollo de la simulación",
                              ["Temperatura Final","Tiempo de Simulación"])
    
        if "Valcon" not in st.session_state:
            Valcon = ValCon1
    
        col1, col2 = st.columns(2)
        with col1:
            t1 = float(st.slider("Especifique la temperatura inicial en el tanque (°C)",
                        min_value= 15,
                        max_value= 85,
                        value = 20,
                        step = 1
                        ))
        
        if Valcon == "Temperatura Final":
            with col2:
                t2 = float(st.slider("Especifique la temperatura final del tanque (°C)",
                        min_value= int(t1),
                        max_value= 92,
                        value = int(t1)+1,
                        step = 1
                        ))
            Cp_prom = (Cp(t1)+Cp(t2))/2    
        elif Valcon == "Tiempo de Simulación":
            with col2:
                tiempototal = st.number_input("Ingrese el tiempo de simulación (min)", 1,1000000000,step=1)
            Cp_prom = (Cp(t1)+Cp(70))/2
            
            
        #Definición constantes
        with col1:
            vol_tanque = st.number_input("Ingrese el el volumen de agua en el tanque (L)", 1,30,step=1)
        M = vol_tanque/1000 * PropsSI('D','P', 101325*560/760,'T', t1+273.15, 'Water') #Masa de agua en el tanque
        with col2:
            st.write("")
            st.write("")
            st.write(f"{M:.3f} kg de agua")
        # Determinación del coeficiente global de transferencia
        if ModAgi == "Sin Agitación":
            if MetCal == "Serpentin":
                A = A_serp
                U = 150
            else:
                A = A_chaq
                U = 100 # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            def f(t):
                return U*A*(T_sat - t)/(M*Cp_prom) #U(T_sat,t)
        elif ModAgi == "Mecánica":
            if MetCal == "Serpentin":
                A = A_serp
                U = 300 #U_serp_batch_AM(Nrev)  
            else:
                A = A_chaq
                U = 250 #U_serp_batch_AM(Nrev) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            def f(t):
                return U*A*(T_sat - t)/(M*Cp_prom)
        
        if st.button("Correr simulación") == True:
            st.success("Esta simulación predice datos reales")
            if Valcon == "Temperatura Final":
                #RK4 
                h = 0.01  # paso de tiempo (segundos)
                theta = 0
                T = t1
                tiempo = [theta]
                temperatura = [T]

                while T < t2:
                    k1 = f(T)
                    k2 = f(T + 0.5*h*k1)
                    k3 = f(T + 0.5*h*k2)
                    k4 = f(T + h*k3)
                    T = T + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
                    theta = theta + h
                    tiempo.append(theta)
                    temperatura.append(T)        
            
                n_puntos = 50
                paso = max(1, len(tiempo)//n_puntos)
                tiempo_plot = tiempo[::paso]
                temperatura_plot = temperatura[::paso]
            
                placeholder = st.empty()
            
                for i in range(1, len(tiempo_plot)+1):

                    df = pd.DataFrame({
                        "Tiempo (s)": tiempo_plot[:i],
                        "Temperatura (°C)": temperatura_plot[:i],
                                        
                    })

                    placeholder.line_chart(
                        df,
                        x="Tiempo (s)",
                        y="Temperatura (°C)"
                    )
                st.info(f"Para la configuración especificada, el tiempo necesario para calentar {vol_tanque:.0f} litros de agua de {t1:.0f} °C hasta {t2:0.0f} °C es {tiempo[-1]:0.0f} s ({tiempo[-1]/60:0.1f} min).")
            elif Valcon == "Tiempo de Simulación":
                tiempototal = tiempototal*60
                t_max = PropsSI('T','P',560*101325/760,'Q',0,'Water')-273.15
                h = 0.1 
                theta = 0
                T = t1
                tiempo = [theta]
                temperatura = [T]

                evaporacion = False
                t_evap = None

                while theta < tiempototal:

                    k1 = f(T)
                    k2 = f(T + 0.5*h*k1)
                    k3 = f(T + 0.5*h*k2)
                    k4 = f(T + h*k3)

                    T = T + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
                    theta += h

                    if T >= t_max:

                        T = t_max

                        tiempo.append(theta)
                        temperatura.append(T)

                        evaporacion = True
                        t_evap = theta

                        break

                    tiempo.append(theta)
                    temperatura.append(T)
                # tiempo = [theta]
                # temperatura = [T]
                # t_evap = 0

                # while theta < tiempototal:
                #     k1 = f(T)
                #     k2 = f(T + 0.5*h*k1)
                #     k3 = f(T + 0.5*h*k2)
                #     k4 = f(T + h*k3)

                #     T = T + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
                #     theta = theta + h

                #     tiempo.append(theta)
                #     if temperatura[-1] >=  t_max:
                #         temperatura.append(t_max)
                #     else:
                #         temperatura.append(T)

                #     if temperatura[-1] == temperatura[-2]:
                #         t_evap+=1

                # ind_evap = len(temperatura) - t_evap
                
                n_puntos = 50
                paso = max(1, len(tiempo)//n_puntos)
                tiempo_plot = tiempo[::paso]
                temperatura_plot = temperatura[::paso]
            
                placeholder = st.empty()
            
                for i in range(1, len(tiempo_plot)+1):
                    df = pd.DataFrame({
                        "Tiempo (s)": tiempo_plot[:i],
                        "Temperatura (°C)": temperatura_plot[:i],                  
                    })
                    placeholder.line_chart(
                        df,
                        x="Tiempo (s)",
                        y="Temperatura (°C)"
                    )
                if evaporacion:
                    st.warning(
                        f"El contenido del tanque alcanzó la temperatura de "
                        f"ebullición ({t_max:.1f} °C) después de "
                        f"{t_evap:.0f} s ({t_evap/60:.1f} min). "
                        f"La simulación se detuvo en ese punto debido al inicio "
                        f"del cambio de fase."
                    )
                else:
                    st.info(
                        f"Temperatura final: {temperatura[-1]:.2f} °C"
                    )
        
    if State == "Semibatch":
        col1, col2 = st.columns(2)
        with col1:
            Qin = float(st.number_input("Especifique el flujo de alimentación al tanque (mL/s)",10,1000, step = 10))      
        with col2:
            t1 = float(st.slider("Especifique la temperatura de ingreso del agua (°C)",
                        min_value= 15,
                        max_value= 35,
                        value = 20,
                        step = 1
                        )) 
        if ModAgi == "Sin Agitación":
            if MetCal == "Serpentin":
                A = A_serp
                U = 150
            else:
                A = A_chaq
                U = 100 # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            def f(t,M):
                return (Fin*Cp_prom*(t1-t) + U*A*(T_sat - t))/(M*Cp_prom)#U(T_sat,t)*A*(T_sat - t))/(M*Cp_prom)
        elif ModAgi == "Mecánica":
            if MetCal == "Serpentin":
                A = A_serp
                U = 300 #U_serp_batch_AM(Nrev)  
            else:
                A = A_chaq
                U = 250 #U_serp_batch_AM(Nrev) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            def f(t,M):
                return (Fin*Cp_prom*(t1-t) + U*A*(T_sat - t))/(M*Cp_prom)
            
        Cp_prom = (Cp(t1)+Cp(70))/2
        Fin = Qin/10**6 * PropsSI('D','T',t1+273.15,'P',560/760*101325,'Water') #Conversión mL/s a kg/s
        t_max = PropsSI('T','P',560*101325/760,'Q',0,'Water')-273.15
        M = 1  # kg inicial
        Masa_tanque=[M]
        
        tiempototal = 30000 / Qin
        
        if st.button("Correr simulación") == True:
            st.warning("Esta simulación se basa en datos teóricos, sube tus datos experimentales para predecir el comportamiento real.")
            h = 0.01
            theta = 0
            T = t1

            tiempo = [theta]
            temperatura = [T]
            t_evap = 0
        
            while theta < tiempototal:

                k1 = f(T,M)
                k2 = f(T + 0.5*h*k1, M + 0.5*h*k1)
                k3 = f(T + 0.5*h*k2, M + 0.5*h*k1)
                k4 = f(T + h*k3, M + h*k3)

                T = T + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

                M += Fin*h
                theta += h

                tiempo.append(theta)
                Masa_tanque.append(M)
            
                if temperatura[-1] >=  t_max:
                    temperatura.append(t_max)
                else:
                    temperatura.append(T)
                    
                if temperatura[-1] == temperatura[-2]:
                    t_evap+=1
        
            ind_evap = len(temperatura)-t_evap
            
            
            n_puntos = 100
            paso = max(1, len(tiempo)//n_puntos)
            tiempo_plot = tiempo[::paso]
            temperatura_plot = temperatura[::paso]
            
            placeholder = st.empty()
            
            for i in range(1, len(tiempo_plot)+1):
                df = pd.DataFrame({
                    "Tiempo (s)": tiempo_plot[:i],
                    "Temperatura (°C)": temperatura_plot[:i],                  
                })
                placeholder.line_chart(
                    df,
                    x="Tiempo (s)",
                    y="Temperatura (°C)"
                )
        
            if temperatura[-1] >= t_max:
                st.info(f"Temperatura final: {temperatura[-1]:.2f} °C \nEl contenido del tanque se evapora desde tiempo = {tiempo[ind_evap]:0.0f} s ({tiempo[ind_evap]/60:0.1f} min)")
            else:
                st.info(f"Temperatura final: {temperatura[-1]:.2f} °C \nTiempo total de llenado: {tiempototal:.0f} s ({tiempototal/60:.1f} min).")
          
