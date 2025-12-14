import streamlit as st
import random
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from pathlib import Path


#sobre la google sheets
def guardar_en_sheets(registro):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(creds)

    sheet = client.open("Resultados_fracciones_4").sheet1
    sheet.append_row(list(registro.values()))


# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(page_title="Fracciones Aventureras", page_icon="🧙‍♂️", layout="centered")

st.title("🧙‍♂️ Fracciones Aventureras")
st.markdown("### Ayuda al Mago de las Fracciones a superar los retos mágicos")

st.write(
    "Elige tu nombre, tu grupo y tu número de lista "
    "Contesta con calma, ¡cada respuesta correcta te da una ⭐!"
)

# =========================
# DATOS DEL ALUMNO
# =========================
col1, col2, col3= st.columns(3)
with col1:
    nombre_alumno = st.text_input("Nombre del alumno:", "")
with col2:
    grupo = st.selectbox(
    "Elige tu grupo:",
    [
        "40",
        "41",
        "42",
        "43"
    ])
with col3:        
    no_de_lista=st.text_input("Ingresa tu número de lista:", "")    



st.title("🍕 Fracciones con Pizza")
st.markdown("### Encuentra la fracción equivalente")
st.write("Resuelve los 10 ejercicios. ¡Son muy fáciles!")

# =========================
# ESTADO DE LA TAREA
# =========================
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "aciertos" not in st.session_state:
    st.session_state.aciertos = 0

if "resultados" not in st.session_state:
    st.session_state.resultados = []

# =========================
# EJERCICIOS FIJOS (SIN ALEATORIEDAD)
# =========================
ejercicios = [
    {
        "pregunta": "🍕 La pizza está dividida en 2 partes iguales.\n\n"
                    "Se comieron **1/2** de la pizza.\n\n"
                    "¿Qué fracción representa la misma cantidad?",
        "opciones": ["1/4", "2/4", "1/3", "3/4"],
        "correcta": "2/4"
    },
    {
        "pregunta": "🍕 La pizza está dividida en 3 partes iguales.\n\n"
                    "Se comieron **1/3** de la pizza.\n\n"
                    "¿Qué fracción representa la misma cantidad?",
        "opciones": ["1/6", "2/6", "1/2", "3/6"],
        "correcta": "2/6"
    }
]

# =========================
# MOSTRAR EJERCICIO
# =========================
if st.session_state.indice < len(ejercicios):

    ej = ejercicios[st.session_state.indice]

    st.markdown(f"## Ejercicio {st.session_state.indice + 1} de 2")
    st.markdown(ej["pregunta"])

    respuesta = st.radio(
        "Elige una opción:",
        ej["opciones"],
        key=f"resp_{st.session_state.indice}"
    )

    if st.button("Enviar respuesta"):
        acerto = respuesta == ej["correcta"]

        if acerto:
            st.success("✅ ¡Correcto!")
            st.session_state.aciertos += 1
        else:
            st.error(f"❌ Incorrecto. La respuesta correcta es **{ej['correcta']}**")

        #st.session_state.resultados.append({
        #   "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #    "nombre": nombre_alumno,
        #    "grupo": grupo,
        #    "numero_lista": no_de_lista,
        #    "ejercicio": st.session_state.indice + 1,
        #    "respuesta": respuesta,
        #    "correcta": ej["correcta"],
        #    "acerto": acerto
        #})

        st.session_state.indice += 1
        st.rerun()

# =========================
# FINAL Y GUARDADO EN CSV
# =========================
else:
    st.success("🎉 ¡Terminaste la actividad!")

    total_ejercicios = len(ejercicios)
    aciertos = st.session_state.aciertos

    st.markdown(
        f"""
        **Nombre:** {nombre_alumno}  
        **Grupo:** {grupo}  
        **Número de lista:** {no_de_lista}  

        ✅ **Aciertos:** {aciertos} / {total_ejercicios}
        """
    )

    # ---- REGISTRO ÚNICO POR ALUMNO ----
    registro_final = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nombre": nombre_alumno,
        "Grupo": grupo,
        "Numero_lista": no_de_lista,
        "Aciertos": aciertos,
        "Total_ejercicios": total_ejercicios
    }

    df = pd.DataFrame([registro_final])

    archivo = Path("resultados_fracciones_pizza.csv")

    if archivo.exists():
        df.to_csv(archivo, mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv(archivo, index=False, encoding="utf-8")
        guardar_en_sheets(registro_final)
        st.success("📊 Tu resultado fue enviado a tu maestra")
