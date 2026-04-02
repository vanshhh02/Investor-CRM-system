import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

# ------------------ GLOBAL CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0b0f14;
    color: #e6edf3;
}

.block-container {
    padding: 2rem 3rem;
}

/* Cards */
.card {
    background: #11161c;
    border: 1px solid #1f2933;
    border-radius: 12px;
    padding: 16px;
}

/* Metric */
.metric {
    font-size: 28px;
    font-weight: 600;
}

/* Subtext */
.subtext {
    color: #8b949e;
    font-size: 13px;
}

/* Badge */
.badge {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
}

/* Table row */
.row {
    padding: 12px;
    border-bottom: 1px solid #1f2933;
}
.row:hover {
    background: #161b22;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
}

/* Progress bar */
.progress {
    height: 6px;
    background: #1f2933;
    border-radius: 10px;
}
.progress-fill {
    height: 6px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🚀 Investor CRM")
page = st.sidebar.radio("", ["Dashboard", "Leads", "Reminders", "AI"])

# ------------------ FETCH ------------------
@st.cache_data(ttl=5)
def fetch_leads():
    try:
        return requests.get(f"{BASE_URL}/leads/").json()
    except:
        return []

leads = fetch_leads()

# ------------------ DASHBOARD ------------------
if page == "Dashboard":
    st.title("Dashboard")
    st.caption("Overview of your investor pipeline")

    total = len(leads)
    interested = len([l for l in leads if l["stage"] == "Interested"])
    committed = len([l for l in leads if l["stage"] == "Committed"])

    col1, col2, col3 = st.columns(3)

    def metric_card(title, value, color="white"):
        return f"""
        <div class='card'>
            <div class='subtext'>{title}</div>
            <div class='metric' style='color:{color}'>{value}</div>
        </div>
        """

    col1.markdown(metric_card("Total Leads", total), unsafe_allow_html=True)
    col2.markdown(metric_card("Interested", interested, "#22c55e"), unsafe_allow_html=True)
    col3.markdown(metric_card("Committed", committed, "#8b5cf6"), unsafe_allow_html=True)

    st.markdown("### Pipeline Stages")

    stages = ["Cold", "Contacted", "Interested", "Committed"]
    colors = ["#6366f1", "#f59e0b", "#22c55e", "#8b5cf6"]

    for i, stage in enumerate(stages):
        count = len([l for l in leads if l["stage"] == stage])
        percent = (count / total * 100) if total else 0

        st.markdown(f"""
        <div class='subtext'>{stage} ({count})</div>
        <div class='progress'>
            <div class='progress-fill' style='width:{percent}%; background:{colors[i]}'></div>
        </div>
        """, unsafe_allow_html=True)

# ------------------ LEADS ------------------
elif page == "Leads":
    st.title("Leads")

    col1, col2 = st.columns([3,1])

    search = col1.text_input("Search leads")
    stage_filter = col2.selectbox("Stage", ["All","Cold","Contacted","Interested","Committed"])

    filtered = leads
    if search:
        filtered = [l for l in filtered if search.lower() in l["name"].lower()]
    if stage_filter != "All":
        filtered = [l for l in filtered if l["stage"] == stage_filter]

    # TABLE HEADER
    st.markdown("""
    <div class='row subtext'>
        <b>Name</b> | Email | Stage | Tier
    </div>
    """, unsafe_allow_html=True)

    # ROWS
    for l in filtered:
        stage_color = {
            "Cold": "#6366f1",
            "Contacted": "#f59e0b",
            "Interested": "#22c55e",
            "Committed": "#8b5cf6"
        }.get(l["stage"], "#999")

        tier_color = {
            "High": "#f59e0b",
            "Medium": "#6366f1",
            "Low": "#9ca3af"
        }.get(l["net_worth_tier"], "#999")

        st.markdown(f"""
        <div class='row'>
            <b>{l['name']}</b> — {l['email']} <br>
            <span class='badge' style='background:{stage_color}22;color:{stage_color}'>{l['stage']}</span>
            <span class='badge' style='background:{tier_color}22;color:{tier_color}'>{l['net_worth_tier']}</span>
        </div>
        """, unsafe_allow_html=True)

    # ADD LEAD
    with st.expander("➕ Add Lead"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        linkedin = st.text_input("LinkedIn")
        tier = st.selectbox("Tier", ["High","Medium","Low"])
        interests = st.text_input("Interests")

        if st.button("Add Lead"):
            requests.post(f"{BASE_URL}/leads/", json={
                "name": name,
                "email": email,
                "linkedin": linkedin,
                "net_worth_tier": tier,
                "interest_areas": interests.split(",")
            })
            st.success("Added")
            st.rerun()

# ------------------ REMINDERS ------------------
elif page == "Reminders":
    st.title("Reminders")

    if st.button("Generate Reminders"):
        requests.post(f"{BASE_URL}/reminders/generate")

    if st.button("Load Reminders"):
        reminders = requests.get(f"{BASE_URL}/reminders/").json()

        for r in reminders:
            color = {
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Low": "#22c55e"
            }.get(r["priority"], "#999")

            st.markdown(f"""
            <div class='card' style='border-left:4px solid {color}'>
                <b>{r['message']}</b><br>
                <span class='subtext'>{r['priority']} Priority</span>
            </div>
            """, unsafe_allow_html=True)

# ------------------ AI ------------------
elif page == "AI":
    st.title("AI Insights")

    if not leads:
        st.warning("No leads")
        st.stop()

    lead_map = {l["id"]: l for l in leads}
    selected = st.selectbox("Select Lead", list(lead_map.keys()),
        format_func=lambda x: lead_map[x]["name"])

    col1, col2, col3, col4 = st.columns(4)

    result = ""

    if col1.button("Email"):
        result = requests.get(f"{BASE_URL}/ai/generate-email/{selected}").json()["email"]

    if col2.button("Summary"):
        result = requests.get(f"{BASE_URL}/ai/summary/{selected}").json()["summary"]

    if col3.button("Score"):
        result = str(requests.get(f"{BASE_URL}/ai/score/{selected}").json()["score"])

    if col4.button("Next Action"):
        result = requests.get(f"{BASE_URL}/ai/next-action/{selected}").json()["next_action"]

    if result:
        st.markdown(f"""
        <div class='card'>
            <pre>{result}</pre>
        </div>
        """, unsafe_allow_html=True)