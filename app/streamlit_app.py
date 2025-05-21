import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

# --- Mock Authentication Section ---
st.sidebar.header("User Login")
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

user_id_input = st.sidebar.text_input("Enter your username or user ID", value=st.session_state.user_id)
login_btn = st.sidebar.button("Login")

if login_btn:
    if user_id_input.strip() == "":
        st.sidebar.warning("Please enter a username or user ID.")
    else:
        st.session_state.user_id = user_id_input.strip()
        st.sidebar.success(f"Logged in as: {st.session_state.user_id}")

if not st.session_state.user_id:
    st.warning("Please login with a username or user ID to use the app.")
    st.stop()

# --- Main App ---
st.title("Explainify")
st.write("Enter your query and get both a casual and an academic summary.")

form_error = False  # Track if validation fails

with st.form("query_form"):
    user_query = st.text_area("Your Query")
    submitted = st.form_submit_button("Generate")
    if submitted:
        if not user_query.strip():
            form_error = True
            st.error("Please enter a query before generating summaries.")
        else:
            with st.spinner("Generating summaries..."):
                response = requests.post(
                    f"{API_URL}/generate",
                    json={"user_id": st.session_state.user_id, "query": user_query}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.last_casual = data["casual_summary"]
                    st.session_state.last_academic = data.get("formal_summary") or data.get("academic_summary")
                else:
                    st.error("Error generating summaries.")

if "last_casual" in st.session_state:
    st.subheader("Casual Summary")
    st.write(st.session_state.last_casual)
if "last_academic" in st.session_state:
    st.subheader("Academic Summary")
    st.write(st.session_state.last_academic)

st.sidebar.header("History")
if st.sidebar.button("Refresh History"):
    st.session_state.history = None

if "history" not in st.session_state or st.session_state.history is None:
    resp = requests.get(f"{API_URL}/history", params={"user_id": st.session_state.user_id})
    if resp.status_code == 200:
        st.session_state.history = resp.json()
    else:
        st.session_state.history = []

for item in st.session_state.history:
    with st.sidebar.expander(f"{item['query'][:30]}... ({item['created_at'][:10]})"):
        st.write("**Casual Summary:**", item.get("casual_response", "N/A"))
        st.write("**Academic Summary:**", item.get("formal_response", item.get("academic_response", "N/A")))
