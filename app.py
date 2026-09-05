import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="House price prediction",
    page_icon=":material/home:",
    layout="centered",
)

LOCATIONS = ["Karachi", "Lahore", "Islamabad", "Faisalabad", "Rawalpindi"]


@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")


model = load_model()

with st.sidebar:
    st.header("About", icon=":material/info:")
    st.caption(
        "This app estimates a home price in Pakistan using a random forest "
        "model trained on area, rooms, location, and house age."
    )
    st.badge("Model ready", icon=":material/check_circle:", color="green")

st.title("House price prediction", icon=":material/home:")
st.caption("Enter the property details, then estimate the market price.")

with st.container(horizontal=True):
    st.badge("Random forest", icon=":material/analytics:", color="green")
    st.badge("Five cities", icon=":material/location_city:", color="blue")

st.space("small")

with st.form("prediction_form"):
    st.subheader("Property details", icon=":material/real_estate_agent:")

    location = st.selectbox("Location", options=LOCATIONS)

    area_sqft = st.slider(
        "Area (sqft)",
        min_value=1000,
        max_value=10000,
        value=2000,
        step=50,
    )

    room_cols = st.columns(2)
    with room_cols[0]:
        bedrooms = st.selectbox("Bedrooms", options=[1, 2, 3, 4, 5])
    with room_cols[1]:
        bathrooms = st.selectbox("Bathrooms", options=[1, 2, 3, 4, 5])

    house_age = st.slider(
        "House age (years)",
        min_value=0,
        max_value=50,
        value=10,
    )

    submitted = st.form_submit_button(
        "Predict price",
        icon=":material/payments:",
        type="primary",
        width="stretch",
    )

if submitted:
    new_house_data = pd.DataFrame(
        {
            "area_sqft": [area_sqft],
            "bedrooms": [bedrooms],
            "bathrooms": [bathrooms],
            "location": [location],
            "house_age": [house_age],
        }
    )
    prediction = float(model.predict(new_house_data)[0])

    st.subheader("Estimated price", icon=":material/payments:")
    st.metric(
        "Predicted market value",
        f"PKR {prediction:,.0f}",
        border=True,
    )

    with st.container(horizontal=True):
        st.metric("Location", location, border=True)
        st.metric("Area", f"{area_sqft:,} sqft", border=True)
        st.metric("Bedrooms", bedrooms, border=True)
        st.metric("Bathrooms", bathrooms, border=True)
        st.metric("Age", f"{house_age} yr", border=True)

    st.toast("Price estimated", icon=":material/check_circle:")
else:
    st.caption("Your estimated price will appear here after you submit the form.")
