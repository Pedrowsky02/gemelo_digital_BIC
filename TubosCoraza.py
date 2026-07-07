import streamlit as st

def TubosyCoraza():

    if "Configuracion_TC" not in st.session_state:
        st.session_state.Configuracion_TC = None

    # Pantalla de selección
    if st.session_state.Configuracion_TC is None:

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
        if st.button("Cambiar configuración",width="stretch"):
            st.session_state.Configuracion_TC = None
            st.rerun()

        if st.session_state.Configuracion_TC == "Pitch Triangular - 1 Paso":
            col1,col2 = st.columns(2)
            with col1:
                QAF = st.number_input("Especifique el caudal del fluido frio (mL/s)", min_value=1, max_value=1000,step=1)
            with col2:
                TAF = st.slider("Especifique la temperatura de ingreso del fluido frio (°C)", min_value=15, max_value=30, step=1)
            MetCal = st.selectbox("Seleccione el fluido de calentamiento",{"Agua Caliente","Vapor"})
            if MetCal == "Agua Caliente":
                ConfigFlow = st.selectbox("Seleccione la configuración de flujo",["Paralelo","Contraflujo"])
                col1, col2 = st.columns(2)
                with col1:
                    QAC = st.number_input("Especifique el caudal del fluido caliente (mL/s)", min_value=1, max_value=1000,step=1)
                with col2:
                    TAC = st.slider("Especifique la temperatura de ingreso del fluido Caliente (°C)", min_value=TAF+1, max_value=80, step=1)
            else:
                T_sat = st.slider("Especifique la temperatura de ingreso del vapor (°C)",min_value=93,max_value=150,step=1)
            if st.button("Correr Simulación") == True:
                pass
            
            
        elif st.session_state.Configuracion_TC == "Pitch Triangular - 2 Paso":
            col1,col2 = st.columns(2)
            with col1:
                QAF = st.number_input("Especifique el caudal del fluido frio (mL/s)", min_value=1, max_value=1000,step=1)
            with col2:
                TAF = st.slider("Especifique la temperatura de ingreso del fluido frio (°C)", min_value=15, max_value=30, step=1)
            MetCal = st.selectbox("Seleccione el fluido de calentamiento",{"Agua Caliente","Vapor"})
            if MetCal == "Agua Caliente":
                ConfigFlow = st.selectbox("Seleccione la configuración de flujo",["Paralelo","Contraflujo"])
                col1, col2 = st.columns(2)
                with col1:
                    QAC = st.number_input("Especifique el caudal del fluido caliente (mL/s)", min_value=1, max_value=1000,step=1)
                with col2:
                    TAC = st.slider("Especifique la temperatura de ingreso del fluido Caliente (°C)", min_value=TAF+1, max_value=80, step=1)
            else:
                T_sat = st.slider("Especifique la temperatura de ingreso del vapor (°C)",min_value=93,max_value=150,step=1)
            if st.button("Correr Simulación") == True:
                pass


        elif st.session_state.Configuracion_TC == "Pitch Triangular - Sin Bafles":
            col1,col2 = st.columns(2)
            with col1:
                QAF = st.number_input("Especifique el caudal del fluido frio (mL/s)", min_value=1, max_value=1000,step=1)
            with col2:
                TAF = st.slider("Especifique la temperatura de ingreso del fluido frio (°C)", min_value=15, max_value=30, step=1)
            MetCal = st.selectbox("Seleccione el fluido de calentamiento",{"Agua Caliente","Vapor"})
            if MetCal == "Agua Caliente":
                ConfigFlow = st.selectbox("Seleccione la configuración de flujo",["Paralelo","Contraflujo"])
                col1, col2 = st.columns(2)
                with col1:
                    QAC = st.number_input("Especifique el caudal del fluido caliente (mL/s)", min_value=1, max_value=1000,step=1)
                with col2:
                    TAC = st.slider("Especifique la temperatura de ingreso del fluido Caliente (°C)", min_value=TAF+1, max_value=80, step=1)
            else:
                T_sat = st.slider("Especifique la temperatura de ingreso del vapor (°C)",min_value=93,max_value=150,step=1)
            if st.button("Correr Simulación") == True:
                pass


        elif st.session_state.Configuracion_TC == "Pitch Cuadrado - 1 Paso":
            col1,col2 = st.columns(2)
            with col1:
                QAF = st.number_input("Especifique el caudal del fluido frio (mL/s)", min_value=1, max_value=1000,step=1)
            with col2:
                TAF = st.slider("Especifique la temperatura de ingreso del fluido frio (°C)", min_value=15, max_value=30, step=1)
            MetCal = st.selectbox("Seleccione el fluido de calentamiento",{"Agua Caliente","Vapor"})
            if MetCal == "Agua Caliente":
                ConfigFlow = st.selectbox("Seleccione la configuración de flujo",["Paralelo","Contraflujo"])
                col1, col2 = st.columns(2)
                with col1:
                    QAC = st.number_input("Especifique el caudal del fluido caliente (mL/s)", min_value=1, max_value=1000,step=1)
                with col2:
                    TAC = st.slider("Especifique la temperatura de ingreso del fluido Caliente (°C)", min_value=TAF+1, max_value=80, step=1)
            else:
                T_sat = st.slider("Especifique la temperatura de ingreso del vapor (°C)",min_value=93,max_value=150,step=1)
            if st.button("Correr Simulación") == True:
                pass
        