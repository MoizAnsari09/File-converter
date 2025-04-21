import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📁 File Converter & Cleaner", layout="wide")
st.title("📁 File Converter & Cleaner")
st.write("Upload your file to clean data and convert formats 🚀")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1].lower()
        
        try:
            if ext == "csv":
                df = pd.read_csv(file)
            elif ext == "xlsx":
                df = pd.read_excel(file)
            else:
                st.warning(f"Unsupported file format: {ext}")
                continue
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
            continue

        st.subheader(f"🔍 Preview - {file.name}")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            numeric_cols = df.select_dtypes(include="number").columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.success("Missing values filled successfully.")
            st.dataframe(df.head())

        select_columns = st.multiselect(f"Select columns to include - {file.name}", df.columns.tolist(), default=df.columns.tolist())
        df = df[select_columns]
        st.dataframe(df.head())

        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include='number').empty:
            numeric_data = df.select_dtypes(include="number")
            st.bar_chart(numeric_data.iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"⬇️ Download {file.name} as {format_choice}"):
            output = BytesIO()
            new_name = file.name.rsplit(".", 1)[0] + (".csv" if format_choice == "CSV" else ".xlsx")

            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            output.seek(0)
            st.download_button(
                label="⬇️ Download File",
                file_name=new_name,
                data=output,
                mime=mime
            )
            st.success("Processing complete 🎉")