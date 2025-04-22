import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("/Users/Ruthf/Downloads/w1920503/project_lifecycle_coursework/Average_Salary_by_Job_Classification.csv")

st.write("salary dashboard application")
st.dataframe(df.head())
st.dataframe(df.shape)