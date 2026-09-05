import joblib
import pandas as pd
import streamlit as st

model = joblib.load("house_price_model.pkl")

st.title("House Price Prediction")

st.write("Enter the details of the house to predict its price.")

area_sqft = st.slider("Area in square feet", min_value=1000, max_value=10000, value=5000)
bathrooms = st.selectbox("Bathrooms", options=[1, 2, 3, 4, 5])
bedrooms = st.selectbox("Bedrooms", options=[1, 2, 3, 4, 5])
location = st.selectbox(
    "Location",
    options=["Karachi", "Lahore", "Islamabad", "Faisalabad", "Rawalpindi"],
)
house_age = st.slider("House Age in years", min_value=0, max_value=50, value=10)

if st.button("Predict Price"):
    new_house_data = pd.DataFrame({
        "area_sqft": [area_sqft],
        "bedrooms": [bedrooms],
        "bathrooms": [bathrooms],
        "location": [location],
        "house_age": [house_age],
    })
    prediction = model.predict(new_house_data)
    st.write(f"The predicted price of the house is {prediction[0]:.2f} PKR")