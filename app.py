import streamlit as st
import pandas as pd
import os
from io import BytesIO
import random
import requests
from streamlit_lottie import st_lottie

# --- Page Configuration ---
st.set_page_config(page_title="Data Sweeper", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        html, body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Roboto', sans-serif;
        }
        .big-title {
            font-size: 42px;
            font-weight: 800;
            text-align: center;
            color: #FF6F61;
            margin-bottom: 5px;
            letter-spacing: 1px;
            animation: fadeIn 1s ease-in;
        }
        .small-text {
            font-size: 18px;
            color: #b3b3b3;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(135deg, #FF6F61, #FF4B4B);
            color: white;
            font-size: 16px;
            font-weight: 600;
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            background: #FF4B4B;
            color:white;
            transform: scale(1.05);
        }
        .stFileUploader {
            text-align: center;
            # border: 2px dashed #FF6F61;
            padding: 20px;
            border-radius: 10px;
        }
        .stDataFrame {
            background-color: #1e1e2f;
            color: #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# --- Lottie Animation Loader ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a Lottie animation
lottie_data = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_kdx6cani.json")

# --- Sidebar Enhancements ---
with st.sidebar:
    st.header("📊 Data Sweeper Hub")
    quotes = [
        "Data is the new oil. – Clive Humby",
        "Without data, you're just another person with an opinion. – W. Edwards Deming",
        "In God we trust, all others bring data. – W. Edwards Deming",
        "Data really powers everything that we do. – Jeff Weiner",
        "Torture the data, and it will confess to anything. – Ronald Coase"
    ]
    st.info(random.choice(quotes))
    if lottie_data:
        st_lottie(lottie_data, height=150)

# --- Main Header ---
st.markdown("<h1 class='big-title'>📂 Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown("<p class='small-text'>Convert, clean, and visualize CSV & Excel files easily!</p>", unsafe_allow_html=True)

# --- File Uploader ---
st.markdown("<div class='stFileUploader'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("📤 Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file format: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading file {file.name}: {e}")
            continue
        
        # --- File Information & Data Preview ---
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 📄 File Information")
            st.write(f"**Name:** {file.name}")
            st.write(f"**Size:** {file.size / 1024:.2f} KB")
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
        with col2:
            st.markdown("### 🔍 Data Preview")
            st.dataframe(df.head())
        
        # --- Data Cleaning Options ---
        st.markdown("---")
        st.markdown(f"### 🛠️ Data Cleaning Options for {file.name}")
        col3, col4 = st.columns(2)
        with col3:
            if st.button(f"🗑 Remove Duplicates ({file.name})", key=f"remove_dup_{file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")
        with col4:
            if st.button(f"📌 Fill Missing Values ({file.name})", key=f"fill_missing_{file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing values filled with column mean!")
        
        # --- Column Selection ---
        st.markdown("### 🎯 Select Columns")
        selected_columns = st.multiselect(f"🔍 Choose columns for {file.name}", df.columns, default=list(df.columns))
        df = df[selected_columns]
        
        # --- Data Visualization ---
        st.markdown("---")
        st.markdown(f"### 📊 Data Visualization for {file.name}")
        if st.checkbox(f"📈 Show Graph for {file.name}"):
            numeric_df = df.select_dtypes(include=["number"])
            if not numeric_df.empty:
                st.line_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns available for visualization.")
        
        # --- File Conversion Options ---
        st.markdown("---")
        st.markdown(f"### 🔄 Convert {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"convert_{file.name}")
        
        if st.button(f"🔄 Convert {file.name}", key=f"convert_btn_{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='xlsxwriter')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.download_button(label=f"⬇️ Download {file_name}", data=buffer, file_name=file_name, mime=mime_type, key=f"download_{file.name}")

# --- Footer ---
st.markdown("---")
st.markdown("<p class='small-text'>🚀 Built with ❤️ by Hamza</p>", unsafe_allow_html=True)




