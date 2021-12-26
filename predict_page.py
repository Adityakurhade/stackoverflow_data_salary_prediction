# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:51:03 2021

@author: Adi Kurhade
"""

import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('stacksalary_model.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_ed = data["le_ed"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    
    st.write("""### Select options from below to submit information
             Predicted salary will be the annual salary in USD ($) 
             of full time working professional""")
            
    countries = (
        "United States of America",
        "India",
        "United Kingdom of Great Britain and Northern Ireland",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )
    
    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )
    
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level",education)
    
    experience = st.slider("Years of Experience", 0,50,2)
    
    ok = st.button("Calculate Salary")
    if ok:
        x = np.array([[country, education, experience]])
        x[:,0] = le_country.transform(x[:,0])
        x[:,1] = le_ed.transform(x[:,1])
        x = x.astype(float)
        x
        
        salary = regressor.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
