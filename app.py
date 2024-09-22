import streamlit as st
import requests

# Endpoint da api onde será realizada a request após preenchimento do form
api_url = "http://localhost:5000/patients"

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

    # Envie uma requisição POST para a API
    response = requests.post(api_url, data=data)

    # Mostrar resposta da API
    if response.status_code == 200:
        st.success("Data sent successfully!")
        resp = response.json()["outcome"]
        if resp == 0:
            st.success("The informed patient was not classified as a potential carrier of heart disease")
        else:
            st.error("The informed patient was classified as a potential carrier of heart disease.")
    else:
        st.error(f"Error sending data, please try again. {response.status_code} {response.json()}")
