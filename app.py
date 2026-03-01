import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Smart Data Visualizer", layout="wide")

st.title("Smart Data Visualization Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Shape of dataset:", df.shape)
        st.write("Columns:", df.columns.tolist())

    with col2:
        st.write("Summary Statistics")
        st.dataframe(df.describe())

    st.sidebar.header("Visualization Settings")

    chart_type = st.sidebar.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"]
    )

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if len(numeric_columns) > 0:
        x_axis = st.sidebar.selectbox("Select X-axis", df.columns)
        y_axis = st.sidebar.selectbox("Select Y-axis", numeric_columns)

        st.subheader("Visualization")

        if chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram":
            fig = px.histogram(df, x=y_axis)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔥 Correlation Heatmap")
        plt.figure(figsize=(10,6))
        sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )
    else:
        st.warning("No numeric columns found for visualization.")