import pandas as pd
import streamlit as st
import requests
from streamlit_option_menu import option_menu

#Config da página
st.set_page_config(layout="centered")


# Menu
selected2 = option_menu(None, ["Home", "Patients"],
                        icons=['house', "list-task"],
                        menu_icon="cast", default_index=0, orientation="horizontal")
selected2

# Requests
api_url = "http://127.0.0.1:5000/patient"

def fetch_data_from_backend(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se não houve erro na requisição
        data = response.json()  # Presume que a resposta é em formato JSON

        # Verificação e conversão do JSON para DataFrame
        if isinstance(data, list):
            # Caso onde os dados são uma lista de dicionários
            df = pd.json_normalize(data)
        elif isinstance(data, dict):
            # Caso onde os dados são um único dicionário
            df = pd.json_normalize(data)  # Normaliza o JSON
        else:
            st.error("Formato de resposta não suportado.")
            return pd.DataFrame()

        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao fazer request: {e}")
        return pd.DataFrame()


if selected2 == "Home":
    # Streamlit Form
    st.title("Insert new patient data")
    age = st.number_input("Age",
                          min_value=0,
                          value=0,
                          step=1)
    sex = st.selectbox("Sex (0 Male - 1 Female)", (0, 1))
    cp = st.selectbox("Chest Pain (intensity 0 - 3)", (0, 1, 2, 3))
    trestbps = st.number_input("Resting blood pressure (in mm Hg on admission to the hospital)",
                               min_value=0,
                               value=0,
                               step=1,
                               format='%d')
    chol = st.number_input("Serum cholesterol in mg/dl",
                           min_value=0,
                           value=0,
                           step=1,
                           format='%d')
    fbs = st.selectbox("Fasting blood sugar > 120 mg/dl (0 No - 1 Yes)", (0, 1))
    restecg = st.selectbox("Patient's Resting ECG Levels", (0, 1, 2))
    thalach = st.number_input("Patient's Thalach Levels",
                              min_value=0,
                              value=0,
                              step=1,
                              format='%d')
    exang = st.selectbox("Exercise induced angina (0 = no; 1 = yes)", (0, 1))
    oldpeak = st.number_input('ST depression induced by exercise relative to rest (decimal)')
    slope = st.number_input("Patient's Slope Levels",
                            min_value=0,
                            value=0,
                            step=1,
                            format='%d')
    ca = st.number_input("Patient's CA Levels",
                         min_value=0,
                         value=0,
                         step=1,
                         format='%d')
    thal = st.number_input("Patient's THAL Levels",
                           min_value=0,
                           value=0,
                           step=1,
                           format='%d')

    # Quando o usuário clicar no botão "Enviar"
    if st.button("Send"):
        data = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal,
        }

        # Envia request para API
        response = requests.post(api_url, data=data)

        # Verifica se o response cod é de sucesso, e exibe a classificação do paciente informado.
        if response.status_code == 200:
            st.success("Data sent successfully!")
            resp = response.json()["outcome"]
            if resp == 0:
                st.success("The informed patient was not classified as a potential carrier of heart disease")
            else:
                st.error("The informed patient was classified as a potential carrier of heart disease.")
        else:
            st.error(f"Error sending data, please try again. {response.status_code} {response.json()}")
elif selected2 == "Patients":
    st.title("Patients List")
    if st.button("Fetch data"):
        with st.spinner("Fetching data..."):
            data_frame = fetch_data_from_backend(api_url)
            if not data_frame.empty:
                st.success("Data loaded successfully!")
                st.dataframe(data_frame)  # Exibe os dados em uma tabela interativa
            else:
                st.warning("Empty data!")
