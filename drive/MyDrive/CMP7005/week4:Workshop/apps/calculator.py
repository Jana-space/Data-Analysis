import streamlit as st

# Define functions for calculations
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def prod(a, b):
    return a * b

def div(a, b):
    return a / b

def si(p, r, t):
    return (p * r * t) / 100

def ci(p, r, t):
    return p * pow((1 + r / 100), t)

def sqr(num):
    return num**2

def sqrt(num):
    return num**0.5

# Create Streamlit app
def app():
    st.title("Calculator")

    # Select operation
    operation = st.selectbox("Choose an operation:", ["Addition", "Subtraction", "Multiplication", "Division", "Simple Interest", "Compound Interest", "Square", "Square Root"])

    # Get input values based on operation
    if operation == "Addition":
        num1 = st.number_input("Enter the first number:")
        num2 = st.number_input("Enter the second number:")
        result = add(num1, num2)
    elif operation == "Subtraction":
        num1 = st.number_input("Enter the first number:")
        num2 = st.number_input("Enter the second number:")
        result = sub(num1, num2)
    elif operation == "Multiplication":
        num1 = st.number_input("Enter the first number:")
        num2 = st.number_input("Enter the second number:")
        result = prod(num1, num2)
    elif operation == "Division":
        num1 = st.number_input("Enter the first number:")
        num2 = st.number_input("Enter the second number:")
        result = div(num1, num2)
    elif operation == "Simple Interest":
        principal = st.number_input("Enter the principal amount:")
        rate = st.number_input("Enter the interest rate:")
        time = st.number_input("Enter the time period:")
        result = si(principal, rate, time)
    elif operation == "Compound Interest":
        principal = st.number_input("Enter the principal amount:")
        rate = st.number_input("Enter the interest rate:")
        time = st.number_input("Enter the time period:")
        result = ci(principal, rate, time)
    elif operation == "Square":
        num = st.number_input("Enter the number:")
        result = sqr(num)
    elif operation == "Square Root":
        num = st.number_input("Enter the number:")
        result = sqrt(num)

    # Display the result
    if st.button("Calculate"):
        st.write("Result:", result)