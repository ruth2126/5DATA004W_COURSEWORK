import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#importing the dataset
df = pd.read_csv("/Users/Ruthf/Downloads/w1920503/project_lifecycle_coursework/Average_Salary_by_Job_Classification.csv")

df.head()
df.shape
df.isnull().sum()
df.info()

print(df['Grade'].unique())
print(df['Position Title'].unique())

df.columns = ['Position Title', 'Position Class Code', 'Grade',
       'Average Salary', 'Number of Employees']

df['Average Salary'] = df['Average Salary'].str.replace('$', "")
df['Average Salary'] = df['Average Salary'].str.replace(',', "")
df['Average Salary'] = df['Average Salary'].astype(float)

df.head()
df.info()

df['Grade'] = "Grade" + " " + df['Grade']
top_twenty_grades = df['Grade'].value_counts(ascending = False)[:20]
top_twenty_grades