import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv("olympics_athletes_dataset.csv")

st.title("Olympics Exploratory Data Analysis & Strategic Insights")

selected_year = st.sidebar.slider("Select Year:", int(df["year"].min()), int(df["year"].max()), int(df["year"].max()))
filtered_df = df[df.year == selected_year]

medalists = filtered_df[filtered_df["medal"] != "No Medal"]
fig1 = px.pie(medalists, names='gender', title=f"Medal Distribution by Gender ({selected_year})")

athlete_counts = filtered_df['country_name'].value_counts().head(10).reset_index()
athlete_counts.columns = ['country', 'count']
fig2 = px.bar(athlete_counts, x="country", y="count", color="country", title=f"Top 10 Participating Countries ({selected_year})")

fig3 = px.scatter(filtered_df, x="height_cm", y="weight_kg", color="sport", 
                 hover_name="athlete_name", title="Athlete Physical Profiles by Sport")

country_trend = df.groupby("year")["country_best_rank"].min().reset_index()
fig4 = px.line(country_trend, x="year", y="country_best_rank", title="Global Performance Standard Over Time")

fig4.update_yaxes(autorange="reversed") 

fig5 = px.histogram(medalists, x="age", nbins=20, title=f"Winning Age Distribution ({selected_year})")

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
st.markdown("### 📋 Data Documentation")
st.write("**Source:** Olympics Athletes Dataset (1896-2024)")
st.write(f"**Update Strategy:** This dashboard can be refreshed by replacing the local `olympics_athletes_dataset.csv` with the latest export from the Kaggle/Olympic database.")
