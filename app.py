import pandas as pd
import streamlit as st
import plotly.express as px # Charts-kaga
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Library Analytics", layout="wide")
st.title("📚 Library Book Management System")

# 1. Dataset Creation (Mock Data)
data = {
    "BookID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Title": ["Python Pro", "Data Science", "Harry Potter", "The Hobbit", "SQL Master", "History of Rome", "AI Ethics", "Deep Learning"],
    "Genre": ["Tech", "Tech", "Fantasy", "Fantasy", "Tech", "History", "Tech", "Tech"],
    "BorrowDate": ["2024-01-10", "2024-01-15", "2024-02-01", "2024-02-05", "2024-02-10", "2024-03-01", "2024-03-05", "2024-03-10"],
    "ReturnStatus": ["Returned", "Overdue", "Returned", "Returned", "Overdue", "Returned", "Returned", "Overdue"]
}

df = pd.DataFrame(data)
df['BorrowDate'] = pd.to_datetime(df['BorrowDate'])

# 2. Sidebar Filters
st.sidebar.header("Filters")
selected_genre = st.sidebar.multiselect("Select Genre", options=df["Genre"].unique(), default=df["Genre"].unique())
filtered_df = df[df["Genre"].isin(selected_genre)]

# 3. Key Metrics (Kpi)
col1, col2, col3 = st.columns(3)
col1.metric("Total Books", len(df))
col2.metric("Overdue Books", len(df[df["ReturnStatus"] == "Overdue"]))
col3.metric("Popular Genre", df["Genre"].mode()[0])

# 4. Analysis Sections
tab1, tab2, tab3 = st.tabs(["📊 Genre Analysis", "⚠️ Overdue List", "📈 Borrowing Trends"])

with tab1:
    st.subheader("Borrowing Frequency by Genre")
    genre_counts = filtered_df.groupby("Genre").size().reset_index(name="Counts")
    fig = px.bar(genre_counts, x="Genre", y="Counts", color="Genre", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🚨 Overdue Books (Immediate Action Required)")
    overdue_books = filtered_df[filtered_df["ReturnStatus"] == "Overdue"]
    st.table(overdue_books[["BookID", "Title", "Genre", "BorrowDate"]])

with tab3:
    st.subheader("Peak Borrowing Periods")
    df['Month'] = df['BorrowDate'].dt.strftime('%B')
    trend_data = df.groupby('Month').size().reset_index(name='Borrowings')
    fig2 = px.line(trend_data, x='Month', y='Borrowings', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# 5. Data View
st.subheader("Raw Library Data")
st.dataframe(filtered_df, use_container_width=True)