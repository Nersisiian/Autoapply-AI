import streamlit as st

# Кастомный CSS для стильного интерфейса
st.markdown(\"\"\"
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #6C63FF, #3F3D9E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #6C63FF;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #5A52D5;
    }
</style>
\"\"\", unsafe_allow_html=True)
import requests
import pandas as pd
import time

API_URL = "http://backend:8000"

st.set_page_config(page_title="AutoApply AI", layout="wide")
st.title("рџ¤– AutoApply AI вЂ” Intelligent Job Application System")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Upload Resume", "Browse Jobs", "Generate Applications", "Autopilot", "Application Tracker"]
)

if page == "Upload Resume":
    st.header("рџ“„ Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    if uploaded_file:
        with st.spinner("Parsing and embedding..."):
            files = {"file": uploaded_file}
            resp = requests.post(f"{API_URL}/resume/upload", files=files)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"Resume uploaded! ID: {data['id']}")
                st.json(data["parsed_data"])
                st.session_state["resume_id"] = data["id"]
            else:
                st.error("Upload failed")

elif page == "Browse Jobs":
    st.header("рџ”Ќ Job Listings")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fetch New Jobs"):
            with st.spinner("Fetching jobs..."):
                resp = requests.post(f"{API_URL}/jobs/fetch")
                st.success(resp.json()["message"])
    with col2:
        if "resume_id" in st.session_state:
            if st.button("Match Jobs to My Resume"):
                with st.spinner("Computing fit scores..."):
                    resp = requests.get(f"{API_URL}/jobs/match/{st.session_state['resume_id']}")
                    if resp.status_code == 200:
                        matched = resp.json()
                        st.session_state["matched_jobs"] = matched
                        st.success("Matching complete!")
                    else:
                        st.error("Matching failed")

    # Show jobs
    resp = requests.get(f"{API_URL}/jobs/")
    if resp.status_code == 200:
        jobs = resp.json()
        if jobs:
            df = pd.DataFrame(jobs)
            st.dataframe(df[["id", "title", "company", "location", "source"]], use_container_width=True)
            st.session_state["jobs"] = jobs
        else:
            st.info("No jobs in database. Click 'Fetch New Jobs'.")

    if "matched_jobs" in st.session_state:
        st.subheader("Matched Jobs (sorted by fit)")
        df_matched = pd.DataFrame(st.session_state["matched_jobs"])
        st.dataframe(df_matched[["id", "title", "company", "fit_score"]], use_container_width=True)

elif page == "Generate Applications":
    st.header("вњЌпёЏ Generate Cover Letters & Apply")
    if "matched_jobs" not in st.session_state or "resume_id" not in st.session_state:
        st.warning("Please upload resume and match jobs first.")
    else:
        jobs = st.session_state["matched_jobs"]
        job_options = {f"{j['title']} @ {j['company']} (Score: {j['fit_score']:.1f})": j for j in jobs}
        selected = st.selectbox("Select a job", list(job_options.keys()))
        job = job_options[selected]

        if st.button("Generate Cover Letter"):
            with st.spinner("AI is writing..."):
                payload = {"job_id": job["id"], "resume_id": st.session_state["resume_id"]}
                resp = requests.post(f"{API_URL}/llm/cover-letter", json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    st.subheader("Cover Letter")
                    st.text_area("", data["cover_letter"], height=300)
                    st.subheader("Why You're a Match")
                    st.write(data["explanation"])
                    st.subheader("Improvement Suggestions")
                    for s in data["suggestions"]:
                        st.write(f"- {s}")
                    st.session_state["current_cover"] = data
                    st.session_state["current_job"] = job
                else:
                    st.error("Generation failed")

        if "current_cover" in st.session_state:
            if st.button("Simulate Application Submission"):
                app_data = {
                    "job_id": st.session_state["current_job"]["id"],
                    "resume_id": st.session_state["resume_id"],
                    "fit_score": st.session_state["current_job"]["fit_score"],
                    "cover_letter": st.session_state["current_cover"]["cover_letter"],
                    "notes": "Generated manually"
                }
                resp = requests.post(f"{API_URL}/applications/", json=app_data)
                if resp.status_code == 200:
                    st.success("Application recorded (simulation mode)")
                    st.balloons()
                else:
                    st.error("Failed to record application")

elif page == "Autopilot":
    st.header("рџљЂ Job Opportunity Autopilot")
    st.markdown("""
    **Let AI work for you 24/7.**  
    Enable autopilot and the system will continuously find new jobs, 
    match them to your resume, and auto-generate applications when the fit score is high enough.
    """)

    # Fetch current config
    resp = requests.get(f"{API_URL}/autopilot/config")
    if resp.status_code != 200:
        st.error("Could not load autopilot config.")
    else:
        config = resp.json()
        with st.form("autopilot_settings"):
            resume_id = st.number_input("Resume ID to use", min_value=1, value=config.get("resume_id", 0))
            is_active = st.checkbox("Enable Autopilot", value=config.get("is_active", False))
            fit_threshold = st.slider("Minimum Fit Score to Auto-Apply", 0, 100, int(config.get("fit_threshold", 70)))
            check_interval = st.number_input("Check Interval (minutes)", min_value=15, value=config.get("check_interval_minutes", 60))
            max_apps = st.number_input("Max Applications Per Run", min_value=1, value=config.get("max_applications_per_run", 5))
            submitted = st.form_submit_button("Save Settings")
            if submitted:
                update_data = {
                    "resume_id": resume_id,
                    "is_active": is_active,
                    "fit_threshold": fit_threshold,
                    "check_interval_minutes": check_interval,
                    "max_applications_per_run": max_apps
                }
                resp = requests.post(f"{API_URL}/autopilot/config", json=update_data)
                if resp.status_code == 200:
                    st.success("Autopilot settings updated!")
                else:
                    st.error("Update failed.")

    if st.button("Run Autopilot Now (Test)"):
        with st.spinner("Running autopilot cycle..."):
            resp = requests.post(f"{API_URL}/autopilot/run")
            if resp.status_code == 200:
                st.success("Autopilot cycle completed. Check Application Tracker.")
            else:
                st.error("Autopilot run failed.")

elif page == "Application Tracker":
    st.header("рџ“Љ Your Applications")
    resp = requests.get(f"{API_URL}/applications/")
    if resp.status_code == 200:
        apps = resp.json()
        if apps:
            df = pd.DataFrame(apps)
            st.dataframe(df[["id", "job_id", "fit_score", "status", "applied_at"]], use_container_width=True)
            # Status update
            col1, col2 = st.columns(2)
            with col1:
                app_id = st.number_input("Application ID to update", min_value=1, step=1)
            with col2:
                new_status = st.selectbox("New Status", ["draft", "applied", "interview", "rejected", "offer"])
            if st.button("Update Status"):
                patch_resp = requests.patch(f"{API_URL}/applications/{app_id}/status?status={new_status}")
                if patch_resp.status_code == 200:
                    st.success("Updated")
                    st.rerun()
                else:
                    st.error("Update failed")
        else:
            st.info("No applications yet.")
