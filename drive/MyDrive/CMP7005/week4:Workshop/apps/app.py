import streamlit as st
from multiapp import MultiApp
#from app import calculator,bmi
import calculator
import bmi

app = MultiApp()

# Add all your application here
#app.add_app("Data page for demo", data.app)
app.add_app("calculator", calculator.app)
app.add_app("bmi", bmi.app)

# The main app
app.run()