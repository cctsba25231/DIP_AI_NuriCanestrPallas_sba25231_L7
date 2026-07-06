import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fremont Bridge Bicycle Dashboard",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center;'>Fremont Bridge Bicycle Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size:20px;'>Interactive dashboard exploring bicycle crossing patterns across the Fremont Bridge.</p>",
    unsafe_allow_html=True
)

st.markdown("---")

#Load Data
df = pd.read_csv("Fremont_Bridge_Bicycle_Counter.csv")

#Rename columns to make them easier to use
df=df.rename(columns={
    "Date": "date",
     "Fremont Bridge Sidewalks, south of N 34th St Total": "total",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk": "west_sidewalk",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk": "east_sidewalk"
})

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Remove rows with missing or invalid dates
df = df.dropna(subset=["date"])

# Replace missing bicycle counts with 0
df["total"] = df["total"].fillna(0)
df["west_sidewalk"] = df["west_sidewalk"].fillna(0)
df["east_sidewalk"] = df["east_sidewalk"].fillna(0)

# Make count columns whole numbers
df["total"] = df["total"].astype(int)
df["west_sidewalk"] = df["west_sidewalk"].astype(int)
df["east_sidewalk"] = df["east_sidewalk"].astype(int)

# Create useful date columns
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["hour"] = df["date"].dt.hour
df["day_name"] = df["date"].dt.day_name()

# Button to show or hide cleaned data
if st.button("Show / Hide Cleaned Data"):
    st.session_state["show_data"] = not st.session_state.get("show_data", False)

if st.session_state.get("show_data", False):
    st.subheader("Cleaned Data Preview")
    st.dataframe(df.head(20))

    st.subheader("Dataset Information")
    st.write("Number of rows:", df.shape[0])
    st.write("Number of columns:", df.shape[1])

# Create  first two columns
col1, col2 = st.columns(2)

# Total bicycle count by year
with col1:
    yearly_data = df.groupby("year")["total"].sum().reset_index()

    fig_year = px.bar(
        yearly_data,
        x="year",
        y="total",
        title="Total Bicycle Crossings by Year",
        color_discrete_sequence=["#7B2CBF"]
    )

    fig_year.update_layout(
        xaxis_title="Year",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

    st.plotly_chart(fig_year, use_container_width=True)
    
# Monthly bicycle crossings
with col2:
    monthly_data = df.groupby("month")["total"].sum().reset_index()

    fig_month = px.line(
        monthly_data,
        x="month",
        y="total",
        title="Total Bicycle Crossings by Month",
        markers=True,
        color_discrete_sequence=["#9D4EDD"]
    )

    fig_month.update_layout(
        xaxis_title="Month",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

    st.plotly_chart(fig_month, use_container_width=True)

# Create second two columns
col3, col4 = st.columns(2)

#East vs West comparison
with col3:
    sidewalk_totals = pd.DataFrame({
        "Sidewalk": ["West Sidewalk", "East Sidewalk"],
        "Total Crossings": [
            df["west_sidewalk"].sum(),
            df["east_sidewalk"].sum()
        ]
    })

    fig_sidewalk = px.bar(
        sidewalk_totals,
        x="Sidewalk",
        y="Total Crossings",
        title="East vs West Sidewalk Crossings",
        color="Sidewalk",
        color_discrete_sequence=["#7B2CBF", "#C77DFF"]
    )

    fig_sidewalk.update_layout(
        xaxis_title="Sidewalk",
        yaxis_title="Bicycle Crossings",
        title_x=0.5,
        showlegend=False
    )

    st.plotly_chart(fig_sidewalk, use_container_width=True)
    
#Bicycle crossings by day of the week
with col4:

    # Order the days correctly
    day_order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    daily_data = (
        df.groupby("day_name")["total"]
        .sum()
        .reindex(day_order)
        .reset_index()
    )

    fig_day = px.bar(
        daily_data,
        x="day_name",
        y="total",
        title="Bicycle Crossings by Day of the Week",
        color_discrete_sequence=["#9D4EDD"]
    )

    fig_day.update_layout(
        xaxis_title="Day of the Week",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

    st.plotly_chart(fig_day, use_container_width=True)