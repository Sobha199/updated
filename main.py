
import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Load login data
login_data = pd.read_csv("login coder.csv")

# Session management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# --- Page 1: Login ---
def login_page():
    st.image("s2m-logo.png", width=200)
    st.markdown("<h3 style='color:skyblue;'>S2M Health Private Ltd - Login</h3>", unsafe_allow_html=True)

    st.markdown("###")
    username = st.text_input("Emp ID", key="emp_id", help="Enter your Employee ID")
    password = st.text_input("Password", type="password", help="Enter your password")

    if st.button("Sign In"):
        with st.spinner("Verifying..."):
            time.sleep(1)
            user = login_data[login_data["Emp ID"].astype(str) == username]
            if not user.empty and user.iloc[0]["Password"] == password:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user_info = {
                    "Emp ID": user.iloc[0]["Emp ID"],
                    "Emp Name": user.iloc[0]["Emp Name"],
                    "Login Name": user.iloc[0]["Login Name"],
                    "Team Lead Name": user.iloc[0]["Team Lead Name"]
                }
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

# --- Page 2: Form Submission ---
def form_page():
    st.title("Coder Submission Form")

    today = datetime.today().strftime('%Y-%m-%d')
    emp_id = st.session_state.user_info["Emp ID"]
    emp_name = st.session_state.user_info["Emp Name"]
    team_lead = st.session_state.user_info["Team Lead Name"]
    login_names = login_data["Login Name"].unique()

    with st.form("coder_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", value=datetime.today())
            st.text_input("Emp ID", value=emp_id, disabled=True)
            st.text_input("Emp Name", value=emp_name, disabled=True)
            project = st.selectbox("Project", ["Elevance MA", "Elevance ACA", "Health OS"])
            project_category = st.selectbox("Project Category", ["Entry", "Recheck", "QA"])
        with col2:
            login_name = st.multiselect("Login Name", login_names)
            login_id = ", ".join(login_name)
            st.text_input("Login ID", value=login_id, disabled=True)
            st.text_input("Team Lead", value=team_lead, disabled=True)

        chart_id = st.text_input("Chart ID")
        page_no = st.text_input("Page No")
        dos = st.text_input("No of DOS")
        codes = st.text_input("No of Codes")
        error_type = st.text_input("Error Type")
        error_comments = st.text_area("Error Comments")
        no_of_errors = st.text_input("No of Errors")
        chart_status = st.text_input("Chart Status")
        auditor_emp_id = st.text_input("Auditor Emp ID")
        auditor_name = st.text_input("Auditor Name")

        submitted = st.form_submit_button("Submit")
        if submitted:
            new_data = {
                "Date": date,
                "Emp ID": emp_id,
                "Emp Name": emp_name,
                "Project": project,
                "Project Category": project_category,
                "Login ID": login_id,
                "Login Name": login_name,
                "Team Lead Name": team_lead,
                "Chart ID": chart_id,
                "Page No": page_no,
                "No of DOS": dos,
                "No of Codes": codes,
                "Error Type": error_type,
                "Error Comments": error_comments,
                "No of Errors": no_of_errors,
                "Chart Status": chart_status,
                "Auditor Emp ID": auditor_emp_id,
                "Auditor Name": auditor_name
            }
            df = pd.DataFrame([new_data])
            df.to_csv("form_data.csv", mode='a', header=not os.path.exists("form_data.csv"), index=False)
            st.success("Form submitted!")

# --- Page 3: Dashboard ---
def dashboard_page():
    st.title("Dashboard Overview")
    if not os.path.exists("form_data.csv"):
        st.warning("No data submitted yet.")
        return
    df = pd.read_csv("form_data.csv")
    st.dataframe(df)

    working_days = df["Date"].nunique()
    charts = df["Chart ID"].nunique()
    dos = pd.to_numeric(df["No of DOS"], errors='coerce').sum()
    icd = pd.to_numeric(df["No of Codes"], errors='coerce').sum()
    cph = round(icd / working_days, 2) if working_days > 0 else 0

    st.metric("Working Days", working_days)
    st.metric("No. of Charts", charts)
    st.metric("No. of DOS", dos)
    st.metric("No. of ICDs", icd)
    st.metric("CPH (Codes per Day)", cph)

# --- Router ---
def main():
    st.set_page_config(page_title="S2M Coder Portal", layout="wide", page_icon="💻")
    if not st.session_state.logged_in:
        login_page()
    else:
        page = st.sidebar.selectbox("Select Page", ["Form Submission", "Dashboard"])
        if page == "Form Submission":
            form_page()
        elif page == "Dashboard":
            dashboard_page()

main()
