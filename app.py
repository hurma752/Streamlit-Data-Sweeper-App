import streamlit as st  
import pandas as pd  
import os
from io import BytesIO

# Page configuration
st.set_page_config(page_title="💽 Data Sweeper", layout='wide')

# Title and description
st.title("💽 Data Sweeper")
st.write("✨ Transform your files between **CSV** and **Excel** formats with built-in data cleaning and visualization tools!")

# File uploader
upload_files = st.file_uploader("📤 Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()[1:]

        # Read file into DataFrame
        if file_ext == "csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File info
        st.write(f"📄 **File Name:** `{file.name}`")
        st.write(f"📦 **File Size:** `{round(file.size / 1024, 2)} KB`")
        st.write("🔍 **Preview:**")
        st.dataframe(df.head())

        # Data cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"🧽 Clean Data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧼 Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🩹 Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include='number').columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled (mean of numeric columns).")

        # Column selection
        st.subheader("🧩 Select Columns to Keep")
        columns = st.multiselect(f"📌 Choose columns for `{file.name}`", df.columns, default=list(df.columns))
        df = df[columns]

        # Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Chart for `{file.name}`"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric data available for charting.")

        # Conversion
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"📥 Convert `{file.name}` to:", ("CSV", "Excel"), key=file.name)

        if st.button(f"🔃 Convert `{file.name}`"):
            if conversion_type == "CSV":
                buffer = BytesIO()
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                new_file_name = file.name.replace(file_ext, "csv")
                mime_type = "text/csv"
            else:  # Excel
                buffer = BytesIO()
                df.to_excel(buffer, index=False)
                buffer.seek(0)
                new_file_name = file.name.replace(file_ext, "xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            st.download_button(
                label=f"⬇️ Download `{new_file_name}`",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type,
                key=f"{file.name}_download"
            )
            st.success(f"🎉 `{file.name}` converted to **{conversion_type}** and ready to download!")
