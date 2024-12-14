import streamlit as st
def app():
    st.title("Body Mass Index Calculator")

    weight = st.number_input("Enter your weight (kg):")
    height = st.number_input("Enter your height (m):")

    if st.button("Calculate BMI"):
        result = bmi(weight, height)
        st.write("Your BMI is:", result)