#importing libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

#importing the dataset
df = pd.read_csv(r'Average_Salary_by_Job_Classification.csv')

# Data Cleaning / Preprocessing 
df.columns = ['Position Title', 'Position Class Code', 'Grade', 'Average Salary', 'Number of Employees']

# Cleaning Average Salary Column
df['Average Salary'] = df['Average Salary'].str.replace('$', "", regex=False).str.replace(',', "", regex=False).astype(float)

# Modify Grade Column for Readability
df['Grade'] = "Grade " + df['Grade']

# Creating Streamlit app

# Sidebar and Filters 
st.sidebar.header('Filter Options')

# Grade Filter
grades = sorted(df['Grade'].unique().tolist())
default_grades = ['Grade 10', 'Grade 11', 'Grade 12', 'Grade 13', 'Grade 14']

selected_grades = st.sidebar.multiselect(
    'Select up to 10 Job Grades:',
    options=grades,
    default=[grade for grade in default_grades if grade in grades],
    max_selections=10
)

# Salary Range Filter
min_salary = int(df['Average Salary'].min())
max_salary = int(df['Average Salary'].max())

salary_range = st.sidebar.slider(
    'Select Salary Range:',
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)
)

# Position Title Search (We applied this to only the downloadable table)
position_search = st.sidebar.text_input('Search for Position Title:')

# Applying Filters 
# Filters for Visuals and KPIs
filtered_df_visuals = df.copy()

if selected_grades:
    filtered_df_visuals = filtered_df_visuals[filtered_df_visuals['Grade'].isin(selected_grades)]

    filtered_df_visuals = filtered_df_visuals[
    (filtered_df_visuals['Average Salary'] >= salary_range[0]) &
    (filtered_df_visuals['Average Salary'] <= salary_range[1])
]

# Filters for the downloadable Table 
filtered_df_table = df.copy()

if position_search:
    filtered_df_table = filtered_df_table[
        filtered_df_table['Position Title'].str.contains(position_search, case=False, na=False)
    ]

if selected_grades:
    filtered_df_table = filtered_df_table[filtered_df_table['Grade'].isin(selected_grades)]

filtered_df_table = filtered_df_table[
    (filtered_df_table['Average Salary'] >= salary_range[0]) &
    (filtered_df_table['Average Salary'] <= salary_range[1])
]

# Dashboard Title 
st.title('Montgomery County Job Dashboard')

# KPI Section 

# Full Dataset KPIs
total_positions = df['Position Title'].nunique()
total_employees = df['Number of Employees'].sum()
mean_salary = df['Average Salary'].mean()

# Filtered Dataset KPIs
filtered_total_positions = filtered_df_visuals['Position Title'].nunique()
filtered_total_employees = filtered_df_visuals['Number of Employees'].sum()
filtered_mean_salary = filtered_df_visuals['Average Salary'].mean()

# Displaying the KPIs
st.subheader('Overall KPIs')
col1, col2, col3 = st.columns(3)
col1.metric("Total Positions", total_positions)
col2.metric("Total Employees", total_employees)
col3.metric("Mean Average Salary", f"£{mean_salary:,.2f}")

st.subheader('Filtered KPIs')
col1, col2, col3 = st.columns(3)
col1.metric("Filtered Positions", filtered_total_positions)
col2.metric("Filtered Employees", filtered_total_employees)
col3.metric("Filtered Mean Salary", f"£{filtered_mean_salary:,.2f}")

# Visual 1: Top 20 Positions by Average Salary
st.subheader('Top 20 Positions by Average Salary (Filtered)')

fig1, ax1 = plt.subplots(figsize=(10,6))
top_positions = filtered_df_visuals.sort_values('Average Salary', ascending=False).head(20)
sns.barplot(data=top_positions, x='Average Salary', y='Position Title', ax=ax1, palette='Blues_r')
ax1.set_title('Top 20 Positions')
st.pyplot(fig1)

# Visual 2a: Average Salary Distribution by Job Grade (Boxplot)
st.subheader('Average Salary Distribution by Job Grade')
if not selected_grades:
    st.info('Kindly select grades in the left pane to view visuals.')
elif filtered_df_visuals.empty:
    st.info('No data available for the selected grades and salary range.')
else:
    fig2, ax2 = plt.subplots(figsize=(10,6))
    sns.boxplot(data=filtered_df_visuals, x='Grade', y='Average Salary', palette='Set3', ax=ax2)
    plt.xticks(rotation=45)
    ax2.set_title('Salary Distribution by Selected Filters')
    st.pyplot(fig2)

# Visual 2b: Pie Chart of Employees per Grade
st.subheader('Employee Distribution by Job Grade')

if not selected_grades:
    st.info('Kindly select grades in the left pane to view visuals.')
elif filtered_df_visuals.empty:
    st.info('No data available for the selected grades and salary range.')
else:
    fig_pie, ax_pie = plt.subplots(figsize=(8,8))
    grade_counts = filtered_df_visuals.groupby('Grade')['Number of Employees'].sum()
    ax_pie.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax_pie.axis('equal') 
    ax_pie.set_title('Employee Distribution by Job Grade')
    st.pyplot(fig_pie)
# Visual 3: Histogram of Average Salary (Unfiltered) 
st.subheader('Distribution of Average Salary (Full Dataset)')

fig3, ax3 = plt.subplots(figsize=(10,6))
sns.histplot(df['Average Salary'], bins=30, kde=True, color='skyblue', ax=ax3)
ax3.set_title('Average Salary Distribution')
st.pyplot(fig3)


# Visual 4: Most Filled Positions (Top 10) 
st.subheader('Most Filled Positions (Top 10)')

most_filled = df.sort_values('Number of Employees', ascending=False).head(10)
st.dataframe(most_filled[['Position Title', 'Number of Employees']])
# Visual 5: Least Filled Positions (Bottom 10) 
st.subheader('Least Filled Positions (Bottom 10)')

least_filled = df.sort_values('Number of Employees', ascending=True).head(10)
st.dataframe(least_filled[['Position Title', 'Number of Employees']])

# Visual 6: Top 10 Paid Job Grades 
st.subheader('Top 10 Paid Job Grades')

grade_salary = df.groupby('Grade')['Average Salary'].mean().reset_index()
top10_grades = grade_salary.sort_values('Average Salary', ascending=False).head(10)

fig4, ax4 = plt.subplots(figsize=(10,6))
sns.barplot(data=top10_grades, x='Average Salary', y='Grade', palette='Greens', ax=ax4)
ax4.set_title('Top 10 Paid Job Grades')
st.pyplot(fig4)
# Visual 7: Bottom 10 Paid Job Grades 
st.subheader('Bottom 10 Paid Job Grades')

bottom10_grades = grade_salary.sort_values('Average Salary', ascending=True).head(10)

fig5, ax5 = plt.subplots(figsize=(10,6))
sns.barplot(data=bottom10_grades, x='Average Salary', y='Grade', palette='Reds', ax=ax5)
ax5.set_title('Bottom 10 Paid Job Grades')
st.pyplot(fig5)

# Downloadable Filtered Table 
st.subheader('Filtered Data Table')

if not filtered_df_table.empty:
    st.dataframe(filtered_df_table)
    
    csv = filtered_df_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download filtered data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )
else:
    st.info('No data available for the selected filters.')




