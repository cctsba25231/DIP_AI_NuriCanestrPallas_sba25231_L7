#Import the libraries needed for the dashboard

import streamlit as st				#Used to create the interactive dashboard
import pandas as pd					#Used to load, clean and organise the data
import plotly.express as px			# Used to create interactive visualisations

# Set up the Streamlit page
#"wide" layout gives more space for charts side by side
st.set_page_config(
    page_title="Fremont Bridge Bicycle Dashboard",
    layout="wide"
)

#Create a centred dashboard title using HTML inside Streamlit

st.markdown(
    "<h1 style='text-align: center;'>Fremont Bridge Bicycle Dashboard</h1>",
    unsafe_allow_html=True
)

#Add a centred subtitle explaining the purpose of the dashboard
st.markdown(
    "<p style='text-align: center; font-size:20px;'>Interactive dashboard exploring bicycle crossing patterns across the Fremont Bridge.</p>",
    unsafe_allow_html=True
)

st.markdown("---")

#Load the CSV file into a pandas DataFrame
df = pd.read_csv("Fremont_Bridge_Bicycle_Counter.csv")

#Rename columns names to shorter names
df=df.rename(columns={
    "Date": "date",
     "Fremont Bridge Sidewalks, south of N 34th St Total": "total",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk": "west_sidewalk",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk": "east_sidewalk"
})

# Convert the date column into a date/time format
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

# Create extra date columns from the main date column
df["year"] = df["date"].dt.year						# Used for yearly trends
df["month"] = df["date"].dt.month					# Used fro monthly trends
df["day"] = df["date"].dt.day						# Store the day of the month
df["hour"] = df["date"].dt.hour						# Used to analyse busy hours
df["day_name"] = df["date"].dt.day_name()			# Used for weekdays analysis

# Create a button that lets us to show or hide the clean data
# st.session_state remembers wether the data is currently visible
if st.button("Show / Hide Data"):
    st.session_state["show_data"] = not st.session_state.get("show_data", False)

#Only shows the cleaned data table if we click the button
if st.session_state.get("show_data", False):
    st.subheader("Cleaned Data Preview")
    st.dataframe(df.head(20))

    st.subheader("Dataset Information")
    st.write("Number of rows:", df.shape[0])
    st.write("Number of columns:", df.shape[1])

# Create KPI's for the top of the dashboard
total_records = len(df)
total_crossings = df["total"].sum()
average_hourly = round(df["total"].mean(), 1)
busiest_year = int(df.groupby("year")["total"].sum().idxmax())

#Create four columns for the KPI's
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

#Display the KPI's
with kpi1:
    st.metric("Total Records", f"{total_records:,}")

with kpi2:
    st.metric("Total Crossings", f"{total_crossings:,}")

with kpi3:
    st.metric("Average Hourly", average_hourly)

with kpi4:
    st.metric("Busiest Year", busiest_year)

st.markdown("---")


# Create two columns for the first row of charts
col1, col2 = st.columns(2)

# Chart 1: Total Bycycle Crossing by Year

with col1:

# Group the data by year and add all bicycle crossing for each year
    yearly_data = df.groupby("year")["total"].sum().reset_index()

#Create an interective bar chart using Plotly
    fig_year = px.bar(
        yearly_data,
        x="year",
        y="total",
        title="Total Bicycle Crossings by Year",
        color_discrete_sequence=["#7B2CBF"]
    )

# Improve th chart lables and centre the title
    fig_year.update_layout(
        xaxis_title="Year",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

# Display the chart in Streamlit
    st.plotly_chart(fig_year, use_container_width=True)
    
# Chart 2: Total Bicycle Crossings by Month
with col2:
    
# Group the data by month and add all crossings for each month    
    monthly_data = df.groupby("month")["total"].sum().reset_index()

# Create an interactive line chart
# markers=True adds points to the line, making the trend easier to follow
    fig_month = px.line(
        monthly_data,
        x="month",
        y="total",
        title="Total Bicycle Crossings by Month",
        markers=True,
        color_discrete_sequence=["#9D4EDD"]
    )

# Improve labels and centre the title
    fig_month.update_layout(
        xaxis_title="Month",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

# Display the chart
    st.plotly_chart(fig_month, use_container_width=True)

# Create two columns for the second row of charts
col3, col4 = st.columns(2)

# Chart 3: East vs West Sidewalk Crossings
# This chart compares the total bicycle crossings on the west and east sidewalks
with col3:
    
# Create a new table with the total crossings for each sidewalk    
    sidewalk_totals = pd.DataFrame({
        "Sidewalk": ["West Sidewalk", "East Sidewalk"],
        "Total Crossings": [
            df["west_sidewalk"].sum(),
            df["east_sidewalk"].sum()
        ]
    })

# Creat a bar chart to compare the two sidewalk totals
    fig_sidewalk = px.bar(
        sidewalk_totals,
        x="Sidewalk",
        y="Total Crossings",
        title="East vs West Sidewalk Crossings",
        color="Sidewalk",
        color_discrete_sequence=["#7B2CBF", "#C77DFF"]
    )

# Improve labels, centre title, and hide the lagend because labels are on the x-axis
    fig_sidewalk.update_layout(
        xaxis_title="Sidewalk",
        yaxis_title="Bicycle Crossings",
        title_x=0.5,
        showlegend=False
    )

# Display the chart 
    st.plotly_chart(fig_sidewalk, use_container_width=True)
    
# Chart 4: Bycycle Crossings by Hour
# This chart is useful for identifying commuting peaks
with col4:

# Group the data by hour and add all crossings for each hour
    hourly_data = (
        df.groupby("hour")["total"]
        .sum()
        .reset_index()
    )

# Create a bar chart showing bicycle activity by hour
    fig_hour = px.bar(
        hourly_data,
        x="hour",
        y="total",
        title="Bicycle Crossings by Hour",
        color_discrete_sequence=["#C77DFF"]
    )

# Improce labels and centre title
    fig_hour.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Bicycle Crossings",
        title_x=0.5
    )

# Display the chart
    st.plotly_chart(fig_hour, use_container_width=True)
    

# Chart 5: Heatmap by Day and Hour
# The heatmap shows when cycling activity is highest during the week.
# It combines day of the weel and hour of the day.

# Group the data by day and hour, then add the total crossings
heatmap_data = (
    df.groupby(["day_name", "hour"])["total"]
    .sum()
    .reset_index()
)

# Set the correct order for the days the week
day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

# Convert day_name into an ordered category, this makes the heatmap diplay Monday to Sunday correctly
heatmap_data["day_name"] = pd.Categorical(
    heatmap_data["day_name"],
    categories=day_order,
    ordered=True
)

#Convert the data into a pivot table
heatmap_pivot = heatmap_data.pivot(
    index="day_name",
    columns="hour",
    values="total"
)

# Create a heatmap
# Darker purple means higher bicycle activity
fig_heatmap = px.imshow(
    heatmap_pivot,
    title="Bicycle Crossings by Day and Hour",
    color_continuous_scale="Purples"
)

# Improve labels and centre title
fig_heatmap.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Day of Week",
    title_x=0.5
)

# Display the heatmap across the full with of the dashboard
st.plotly_chart(fig_heatmap, use_container_width=True)

# Chart 6: Average Montly Bicycle Activity

# Group the data by month and calculate the average crossings for each month
monthly_average = (
    df.groupby("month")["total"]
    .mean()
    .reset_index()
)

# Create and area chart
fig_area = px.area(
    monthly_average,
    x="month",
    y="total",
    title="Average Bicycle Crossings by Month",
    color_discrete_sequence=["#9D4EDD"]
)

# Improve labels and centre title
fig_area.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Bicycle Crossings",
    title_x=0.5
)

# Display the chart
st.plotly_chart(fig_area, use_container_width=True)
