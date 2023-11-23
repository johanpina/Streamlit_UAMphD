import streamlit as st
import pickle
import pandas as pd
st.title("vamos a predecir cosas 🚀")

@st.cache_resource
def load_model(modelName):
    with open(f'models/data/model{modelName}.pkl','rb') as gb:
        modelo = pickle.load(gb)
    return modelo

model_text = st.selectbox("Select Slider", options=["Bayesian", "Random Forest", "ExtraTrees","Gradient Boosting","Decision Tree"])

modelo = None
try:
    if model_text == "Bayesian":
        st.write("Bayesian")
        modelo = load_model("B")
    elif model_text == "Random Forest":
        st.write("Random Forest")
        modelo = load_model("RF")
    elif model_text == "ExtraTrees":
        st.write("ExtraTrees")
        modelo = load_model("ET")
    elif model_text == "Gradient Boosting":
        st.write("Gradient Boosting")
        modelo = load_model("GB")
    elif model_text == "Decision Tree":
        st.write("Decision Tree")
        modelo = load_model("DT")

    st.sidebar.success(f"Modelo {model_text} cargado correctamente ✅")
except:
    st.sidebar.error(f"Modelo {model_text} no encontrado ❌")

st.subheader("Machine Learning modelo seleccionado") 

st.subheader("Algoritmo de Machine Learning")
st.write("Definición del algoritmo implementado para predecir los patrones de flujo.")

st.subheader("Características de entrada")

features = ['Velocidad superficial del líquido (Vsl)', 'Velocidad superficial del gas (Vsg)', 'Viscosidad del líquido (VisL)', 'Viscosidad del gas (VisG)', 'Densidad del líquido (DenL)', 'Densidad del gas (DenG)', 'Tensión superficial (ST)', 'Ángulo de inclinación tubería (Ang)', 'Diámetro de la tubería (ID)']
st.write("A continuación, ingrese los valores de las características que serán utilizadas para la clasificación de patrones de flujo en los modelos de Machine Learning:")        

def user_input_parameters():
    inputs = {}
    for i, feature in enumerate(features):
        row, col = i // 3, i % 3
        with st.container():
            if i % 3 == 0:
                cols = st.columns(3)
            inputs[feature] = cols[col].text_input(feature)
    data_features = {
        'Vsl' : inputs[features[0]],
        'Vsg' : inputs[features[1]],
        'VisL' : inputs[features[2]],
        'VisG' : inputs[features[3]],
        'DenL': inputs[features[4]],
        'DenG' : inputs[features[5]],
        'ST' : inputs[features[6]],
        'Ang' : inputs[features[7]],
        'ID' : inputs[features[8]]
        }
    features_df = pd.DataFrame(data_features, index = [0])
    return features_df


df = user_input_parameters()


# Crear un nuevo DataFrame con una fila adicional 'Valor'
df = df.T.reset_index()
df.columns = ['Característica', 'Valor']
df = df.set_index('Característica').T

st.table(df)

st.subheader("Predicción de patrones de flujo")

predict_button, clear_button = st.columns(2)
predict_clicked = predict_button.button('PREDECIR')

prediction = None

if predict_clicked:
# Validar que todos los campos contengan valores numéricos
    for value in df.values.flatten():
        if not value or not value.isdigit():
            st.warning("Por favor, complete todos los datos con valores numéricos antes de hacer la predicción.")
            break
        else:
            prediction = modelo.predict(df)
    
    st.success(f"El patrón de flujo es: {prediction[0]}")

    # Crear un diccionario para asociar las predicciones con sus descripciones
    prediction_descriptions = {
        'DB': 'Flujo de burbujas dispersas (DB)',
        'SS': 'Flujo estratificado uniforme (SS)',
        'SW': 'Flujo estratificado ondulado (SW)',
        'A': 'Flujo anular (A)',
        'I': 'Flujo intermitente (I)',
        'B': 'Flujo de burbujas (B)',

    }

    # Mostrar la descripción completa de la predicción
    st.success(prediction_descriptions[prediction[0]])

    if prediction[0] in ["I", "A"]:
        st.warning("Alerta: Presta atención a posibles fallos en la tubería.")


