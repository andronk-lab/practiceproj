import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv("olympics_athletes_dataset.csv")

st.title("Olympics Analytics: Age & Achievement")

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

country_trend = df[df["medal"].isin(selected_medals)].groupby("year")["country_best_rank"].min().reset_index()
fig4 = px.line(country_trend, x="year", y="country_best_rank", title="Global Rank Trend for Selected Medals")
fig4.update_yaxes(autorange="reversed") 

fig5 = px.histogram(filtered_df, x="age", color="medal", nbins=20, title="Age Distribution of the Selection")

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

st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.markdown("### Data Documentation")
st.write("**Source:** Olympics Athletes Dataset (1896-2024)")
st.write(f"**Sustainability:** Filters for Medal and Age allow for deeper cohort analysis as new datasets are added.")
