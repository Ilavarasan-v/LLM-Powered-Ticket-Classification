import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="LLM Ticket Classification Dashboard",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 LLM Powered Ticket Classification Dashboard")
st.markdown("---")

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_CSV = os.path.join(BASE_DIR, "outputs", "ticket_classifications.csv")

try:
    df = pd.read_csv(OUTPUT_CSV)
except FileNotFoundError:
    st.error("ticket_classifications.csv not found.")
    st.stop()

# ----------------------------------------------------
# Metrics
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tickets", len(df))

col2.metric(
    "Categories",
    df["category"].nunique()
)

col3.metric(
    "High/Critical",
    len(df[df["urgency"].isin(["High", "Critical"])])
)

negative_count = len(df[df["sentiment"] == "Negative"])

col4.metric(
    "Negative Tickets",
    negative_count
)

st.divider()

# ----------------------------------------------------
# Charts
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Category Distribution")

    fig = px.bar(
        df["category"].value_counts().reset_index(),
        x="category",
        y="count",
        labels={
            "category": "Category",
            "count": "Tickets"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Urgency Distribution")

    fig = px.pie(
        df,
        names="urgency",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# Sentiment Chart
# ----------------------------------------------------

st.subheader("Sentiment Distribution")

fig = px.bar(
    df["sentiment"].value_counts().reset_index(),
    x="sentiment",
    y="count",
    labels={
        "sentiment": "Sentiment",
        "count": "Tickets"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Filter
# ----------------------------------------------------

st.subheader("Filter Tickets")

category = st.selectbox(

    "Select Category",

    ["All"] + sorted(df["category"].unique())

)

filtered = df

if category != "All":

    filtered = filtered[
        filtered["category"] == category
    ]

st.dataframe(
    filtered,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Search Ticket
# ----------------------------------------------------

st.subheader("Search Ticket")

ticket_id = st.text_input("Enter Ticket ID")

if ticket_id:

    result = df[
        df["ticket_id"].str.upper()
        ==
        ticket_id.upper()
    ]

    if len(result):

        st.success("Ticket Found")

        st.write(result)

    else:

        st.error("Ticket Not Found")

st.divider()

# ----------------------------------------------------
# Download
# ----------------------------------------------------

st.download_button(

    "⬇ Download CSV",

    df.to_csv(index=False),

    file_name="ticket_classifications.csv",

    mime="text/csv"

)

st.markdown("---")

st.caption("LLM Powered Ticket Classification Dashboard")