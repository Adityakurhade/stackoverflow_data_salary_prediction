# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:51:41 2021

@author: Adi Kurhade
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "others"
    return categorical_map


def clean_experience(years):
    if years == "Less than 1 year":
        return 0.5
    if years == "More than 50 years":
        return 50
    return float(years)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country",
           "EdLevel",
           "YearsCodePro",
           "Employment",
           "ConvertedCompYearly"
          ]]
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis=1)
    df = df[df.Salary.notnull()]
    df = df.dropna()
    df1 = df[df["Employment"]== "Employed full-time"]
    df1.drop(['Employment'],axis=1, inplace=True)
    
    country_map = shorten_categories(df1.Country.value_counts(), 400)
    df1['Country'] = df1['Country'].map(country_map)
    df1 = df1[df1["Salary"] <= 250000]
    df1 = df1[df1["Salary"] >= 10000]
    df1 = df1[df1['Country'] != 'Other']
    
    df1['YearsCodePro'] = df1['YearsCodePro'].apply(clean_experience)
    df1['Education'] = df1['EdLevel'].apply(clean_education)
    df1.drop("EdLevel",axis =1, inplace=True)
    return df1

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salary")
    st.write("""
         ### Stack Overflow Developer Survey 2021
         """
         )
    data = df['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels = data.index, autopct="%1.1f%%",shadow = True,
        startangle =90)
    ax1.axis("equal")

    st.write("""### Number of Data from different Countries""")
    st.pyplot(fig1)

    st.write(
    """
    ### Mean Salary based on country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write("""
             ### Mean salary based on Experience
             """)
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
    
    
    

