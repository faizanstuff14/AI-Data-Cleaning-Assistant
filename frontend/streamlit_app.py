import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Data Cleaning Assistant", layout="centered")


# DARK THEME

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: white !important;
    }
    .stButton button {
        background-color: #1f6feb;
        color: white;
        border-radius: 8px;
    }
    .stTextInput input, .stFileUploader {
        background-color: #161b22;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(" AI Data Cleaning Assistant")

# SESSION STATE

if "token" not in st.session_state:
    st.session_state.token = None

# AUTH SECTION

if not st.session_state.token:
    st.subheader("Authentication")

    auth_mode = st.radio("Choose action", ["Login", "Register"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if auth_mode == "Register":
        if st.button("Register"):
            response = requests.post(
                f"{API_URL}/auth/register",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                st.success(" Registration successful! Please login.")
            else:
                st.error(response.json().get("detail", "Registration failed"))

    else:
        if st.button("Login"):
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.success(" Login successful")
                st.rerun()
            else:
                st.error(" Invalid credentials")

    st.stop()

# AUTH HEADER

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# UPLOAD CSV

st.subheader("Upload CSV File")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    if st.button("Clean Data"):
        files = {"file": uploaded_file}

        with st.spinner("Cleaning data..."):
            response = requests.post(
                f"{API_URL}/data/upload",
                headers=headers,
                files=files
            )

        if response.status_code == 200:
            result = response.json()

            st.success("File cleaned successfully")

            st.subheader("🧾 Cleaning Steps")
            for step in result["steps"]:
                st.write(f"- {step}")

            st.subheader("⬇️ Downloads")
            st.markdown(f"[Download Cleaned CSV]({API_URL}/{result['cleaned_csv']})")
            st.markdown(f"[Download PDF Report]({API_URL}/{result['pdf_report']})")

        else:
            st.error(response.json().get("detail", "Error cleaning file"))

#USER FILE HISTORY

st.divider()
st.subheader("Your Uploaded Files")

history_response = requests.get(
    f"{API_URL}/data/history",
    headers=headers
)

if history_response.status_code == 200:
    history = history_response.json()

    if not history:
        st.info("No uploads yet.")
    else:
        for file in history:
            st.markdown(f"### 📄 {file['original_filename']}")
            st.write(f"🕒 Uploaded at: {file['uploaded_at']}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"[⬇️ Download Cleaned CSV]({API_URL}/data/download/{file['file_id']})"
                )
            with col2:
                st.markdown(
                    f"[📄 Download PDF Report]({API_URL}/{file['pdf_report']})"
                )

            st.divider()
else:
    st.error(" Failed to load history")

#LOGOUT

if st.button("Logout"):
    st.session_state.token = None
    st.rerun()
