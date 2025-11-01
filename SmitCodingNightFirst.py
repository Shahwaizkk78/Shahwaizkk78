import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def download_summary(df):
    summary = df.describe(include='all')
    buffer = BytesIO()
    summary.to_csv(buffer)
    buffer.seek(0)
    return buffer
    
st.title("Interactive Data Explorer")

menu = st.sidebar.radio(
    "Navigation",
    ["Data Summary", "Visualization", "Missing Data", "Download Report", "About"]
)

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

        if len(numeric_cols) == 0:
            st.warning("No numeric columns detected.")
        if len(cat_cols) == 0:
            st.warning("No categorical columns detected.")
    else:
        st.stop()
else:
    st.info("Please upload a CSV file to begin.")
    st.stop()
    
if menu == "Data Summary":
    st.subheader("Dataset Overview")
    

    st.subheader("Descriptive Statistics")
    

elif menu == "Visualization":
    st.subheader("Data Visualization")

    viz_type = st.sidebar.selectbox(
        "Select Visualization Type",
        ["Histogram", "Bar Chart", "Box Plot", "Heatmap", "Scatter Plot", "Pairplot"]
    )

    if viz_type == "Histogram":
        col = st.selectbox("Select Numeric Column", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

    elif viz_type == "Bar Chart":
        col = st.selectbox("Select Categorical Column", cat_cols)
        fig, ax = plt.subplots()
        df[col].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    elif viz_type == "Box Plot":
        col = st.selectbox("Select Numeric Column", numeric_cols)
        fig, ax = plt.subplots()
        sns.boxplot(x=df[col], ax=ax)
        st.pyplot(fig)

    elif viz_type == "Heatmap":
        fig, ax = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    elif viz_type == "Scatter Plot":
        x_col = st.selectbox("X-Axis", numeric_cols)
        y_col = st.selectbox("Y-Axis", numeric_cols)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)

    elif viz_type == "Pairplot":
        sns.pairplot(df[numeric_cols])
        st.pyplot()

elif menu == "Missing Data":
    st.subheader("Missing Data Handling")

    missing_data = df.isnull().sum()
    st.write("Missing Values per Column:")
    st.write(missing_data)

    st.write("Missing Data Heatmap:")
    fig, ax = plt.subplots()
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax)
    st.pyplot(fig)

    st.write("Options:")
    action = st.radio("Choose Action", ["None", "Drop Missing Rows", "Fill with Mean"])

    if action != "None":
        confirm = st.button(f"Confirm {action}")
        if confirm:
            if action == "Drop Missing Rows":
                df.dropna(inplace=True)
                st.success("Missing rows dropped successfully.")
            elif action == "Fill with Mean":
                df.fillna(df.mean(numeric_only=True), inplace=True)
                st.success("Missing values filled with mean.")


elif menu == "Download Report":
    st.subheader("Download Descriptive Statistics Report")
    csv_buffer = download_summary(df)
    st.download_button(
        label="Download Summary CSV",
        data=csv_buffer,
        file_name="summary_report.csv",
        mime="text/csv"
    )
    
elif menu == "About":
    st.markdown("""import seaborn as sns

    ### About
    This interactive data analysis tool was built with **Streamlit**.
    
    **Features:**
    - Upload and explore CSV datasets
    - Visualize data interactively
    - Handle missing values easily
    - Download summary statistics
    """)
