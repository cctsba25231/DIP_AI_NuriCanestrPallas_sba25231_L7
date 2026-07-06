import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fremont Bridge Bicycle Dashboard",
    layout="wide"
)

st.title("Fremont Bridge Bicycle Dashboard")

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

# Show cleaned data
st.subheader("Cleaned Data Preview")
st.dataframe(df.head())

st.subheader("Dataset Information")
st.write("Number of rows:", df.shape[0])
st.write("Number of columns:", df.shape[1])

# Button to show or hide cleaned data
if st.button("Show / Hide Cleaned Data"):
    st.session_state["show_data"] = not st.session_state.get("show_data", False)

if st.session_state.get("show_data", False):
    st.subheader("Cleaned Data Preview")
    st.dataframe(df.head(20))

    st.subheader("Dataset Information")
    st.write("Number of rows:", df.shape[0])
    st.write("Number of columns:", df.shape[1])