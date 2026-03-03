import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv("olympics_athletes_dataset.csv")

st.title("Olympics Analytics: Age & Achievement")

st.markdown("""
**The Bettor's Edge:** This tool analyzes historical Olympic data from 1896 to 2024 to identify 
winning athlete profiles. By adjusting the filters, the user can isolate specific demographics to find 
high probability patterns, such as "peak performance ages" or "ideal physical statures" that 
traditional betting markets might overlook.
""")

st.sidebar.header("Filter Results")

min_age = int(df["age"].min())
max_age = int(df["age"].max())
selected_age_range = st.sidebar.slider("Select Athlete Age Range:", min_age, max_age, (20, 35))

all_medals = df["medal"].unique().tolist()
selected_medals = st.sidebar.multiselect("Select Medal Types:", options=all_medals, default=["Gold", "Silver", "Bronze"])

filtered_df = df[
    (df["age"] >= selected_age_range[0]) & 
    (df["age"] <= selected_age_range[1]) & 
    (df["medal"].isin(selected_medals))
]

fig1 = px.pie(filtered_df, names='gender', title="Gender Distribution in Selected Group")

athlete_counts = filtered_df['country_name'].value_counts().head(10).reset_index()
athlete_counts.columns = ['country', 'count']
fig2 = px.bar(athlete_counts, x="country", y="count", color="country", title="Top 10 Countries in Category")

fig3 = px.scatter(filtered_df, x="height_cm", y="weight_kg", color="sport", 
                 hover_name="athlete_name", title="Physical Profile of Selected Athletes")


fig4 = px.histogram(filtered_df, x="age", color="medal", nbins=20, title="Age Distribution of the Selection")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)


st.divider()
st.markdown(f"""

**Analytical Focus:** This project addresses core betting questions: Which genders and countries dominate specific age cohorts? Is there a perfect physical stature for medal winners? And what is the precise age range for peak performance? Basically, what information can help me place a winning bet whether it be on an underdog or first place winner?

**Data Source:** This dashboard utilizes the *Olympics Athletes Dataset (1896-2024)*, sourced from Kaggle at this link, https://www.kaggle.com/datasets/ashyou09/olympics-athletes-dataset-18962024. 
**Date Accessed:** 2/26/2026  

**Sustainability:** To keep this dashboard current as new results are released:
1. Download the updated dataset from Kaggle.
2. Ensure the file is named `olympics_athletes_dataset.csv` and placed in the root directory.
3. Upon committing the new file to GitHub, the Streamlit app will automatically rerun calculations, updating all charts and filters without requiring code changes.
""")
