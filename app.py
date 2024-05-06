import streamlit as st
import numpy as np
import joblib

st.title("Credit Card Fraud Detection Web App")
st.image("image.png")
st.write("""
## About
Credit card fraud is a form of identity theft that involves an unauthorized taking of another's credit card information for the purpose of charging purchases to the account or removing funds from it.

**This Streamlit App utilizes a Machine Learning API in order to detect fraudulent credit card based on the following criteria: hours, type of transaction, amount, balance before and after transaction etc.**

""")

st.sidebar.header('User Input Features of The Transaction')

sender_name = st.text_input("Input Sender ID")
receiver_name = st.text_input("Input Receiver ID")
step = st.sidebar.slider('Number of Hours it took the Transaction to complete:', min_value=0, max_value=1000)
types = st.sidebar.selectbox("Type of Transfer Made:", ('Cash In', 'Cash Out', 'Debit', 'Payment', 'Transfer'))
amount = st.sidebar.number_input("Amount in Rs.", min_value=0, max_value=110000)
oldbalanceorg = st.sidebar.number_input('Original Balance Before Transaction:', min_value=0, max_value=110000)
newbalanceorg = st.sidebar.number_input('New Balance After Transaction:', min_value=0, max_value=110000)
oldbalancedest = st.sidebar.number_input('Old Balance:', min_value=0, max_value=110000)
newbalancedest = st.sidebar.number_input('New Balance:', min_value=0, max_value=110000)
isflaggedfraud = st.sidebar.selectbox('Specify if this was flagged as Fraud by your System:', ('No', 'Yes'))

if st.button("Detection Result"):
    # Load the pre-trained model
    model = joblib.load("credit-card-fraud.pkl")

    # Transform input features
    type_mapping = {'Cash In': 0, 'Cash Out': 1, 'Debit': 2, 'Payment': 3, 'Transfer': 4}
    type_code = type_mapping[types]
    fraud_flag = 1 if isflaggedfraud == 'Yes' else 0
    
    # Prepare input array for prediction
    ip_array = [step, type_code, amount, oldbalanceorg, newbalanceorg, oldbalancedest, newbalancedest, fraud_flag]
    ip_params = np.array([ip_array])

    # Make prediction
    prediction = model.predict(ip_params)

    # Display result
    if prediction[0] == 0:
        st.write("The transaction is not fraudulent.")
    elif prediction[0] == 1:
        st.write("The transaction is fraudulent.")
