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

# Dashboard KPIs
total_records = len(df)
total_crossings = df["total"].sum()
average_hourly = round(df["total"].mean(), 1)
busiest_year = int(df.groupby("year")["total"].sum().idxmax())

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Records", f"{total_records:,}")

with kpi2:
    st.metric("Total Crossings", f"{total_crossings:,}")

with kpi3:
    st.metric("Average Hourly", average_hourly)

with kpi4:
    st.metric("Busiest Year", busiest_year)

st.markdown("---")


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
    
#Bicycle crossings by hour
with col4:

    hourly_data = (
        df.groupby("hour")["total"]
        .sum()
        .reset_index()
    )

    fig_hour = px.bar(
        hourly_data,
        x="hour",
        y="total",
        title="Bicycle Crossings by Hour",
        color_discrete_sequence=["#C77DFF"]
    )

    fig_hour.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

    st.plotly_chart(fig_hour, use_container_width=True)
    

# Heatmap: which days and hours are the busiest
st.subheader("Busiest Times to Cycle")

heatmap_data = (
    df.groupby(["day_name", "hour"])["total"]
    .sum()
    .reset_index()
)

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

heatmap_data["day_name"] = pd.Categorical(
    heatmap_data["day_name"],
    categories=day_order,
    ordered=True
)

heatmap_pivot = heatmap_data.pivot(
    index="day_name",
    columns="hour",
    values="total"
)

fig_heatmap = px.imshow(
    heatmap_pivot,
    title="Bicycle Crossings by Day and Hour",
    color_continuous_scale="Purples"
)

fig_heatmap.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Day of Week",
    title_x=0.5
)

st.plotly_chart(fig_heatmap, use_container_width=True)

#Area Chart
st.subheader("Average Monthly Bicycle Activity")

monthly_average = (
    df.groupby("month")["total"]
    .mean()
    .reset_index()
)

fig_area = px.area(
    monthly_average,
    x="month",
    y="total",
    title="Average Bicycle Crossings by Month",
    color_discrete_sequence=["#9D4EDD"]
)

fig_area.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Bicycle Crossings",
    title_x=0.5
)

st.plotly_chart(fig_area, use_container_width=True)
