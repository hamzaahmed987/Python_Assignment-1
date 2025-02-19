import streamlit as st
import random
import pandas as pd
from datetime import datetime

# Custom CSS for improved styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ddeeff, #99c2ff);
    }
    .main {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: auto;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #eef2f3, #d4e0ff);
        padding: 20px;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #1a3c6e;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .stButton button {
        background: linear-gradient(135deg, #3498db, #1abc9c);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #1abc9c, #3498db);
    }
    .stMarkdown {
        font-size: 18px;
        color: #1a3c6e;
    }
    .profile-card {
        background: linear-gradient(135deg, #3498db, #1abc9c);
        color: white;
        padding: 35px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
   .profile-pic img {
    border-radius: 50%;
    width: 100px;
    height: 100px;
    object-fit: cover;
    margin-bottom: 10px;
    margin-top: 30px; 
    border: 3px solid white;
}
    .badge {
        display: inline-block;
        background: #4caf50;
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 14px;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session State for User Data
if "users" not in st.session_state:
    st.session_state.users = {}

# App Title
st.markdown("<h1>Growth Mindset Challenge</h1>", unsafe_allow_html=True)

# Sidebar - User Profile
st.sidebar.markdown("<h2>👤 Your Profile</h2>", unsafe_allow_html=True)
name = st.sidebar.text_input("Enter Coder name")
goal = st.sidebar.text_input("Your biggest learning goal?")
learning_style = st.sidebar.selectbox("Your Learning Style", ["Visual", "Reading/Writing", "Hands-on", "Listening"])
profile_pic = st.sidebar.file_uploader("Upload a profile picture", type=["jpg", "jpeg", "png"])
bio = st.sidebar.text_area("Write a short bio about yourself")
interests = st.sidebar.text_input("Your interests (e.g., coding, art, science)")
email = st.sidebar.text_input("Your email (optional)")

if name:
    if name not in st.session_state.users:
        st.session_state.users[name] = {
            "effort": 5,
            "learning": 5,
            "badges": [],
            "profile_pic": None,
            "bio": "",
            "interests": "",
            "email": "",
        }

    st.session_state.users[name].update({
        "profile_pic": profile_pic,
        "bio": bio,
        "interests": interests,
        "email": email,
    })

    # User Profile Card
    st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
    if st.session_state.users[name]["profile_pic"]:
        st.image(st.session_state.users[name]["profile_pic"], width=100)
    st.markdown(f"<h2> Hello, {name}!</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>Your Goal: <i>{goal}</i></p>", unsafe_allow_html=True)
    st.markdown(f"<p>Learning Style: <i>{learning_style}</i></p>", unsafe_allow_html=True)
    st.markdown(f"<p>Bio: <i>{bio}</i></p>", unsafe_allow_html=True)
    st.markdown(f"<p>Interests: <i>{interests}</i></p>", unsafe_allow_html=True)
    st.markdown(f"<p>Email: <i>{email}</i></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Learning Badges
    if st.session_state.users[name]["badges"]:
        st.markdown("<h3>🏅 Your Achievements</h3>", unsafe_allow_html=True)
        for badge in st.session_state.users[name]["badges"]:
            st.markdown(f"<span class='badge'>{badge}</span>", unsafe_allow_html=True)
