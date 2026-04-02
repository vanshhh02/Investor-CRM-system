import streamlit as st
import requests

BASE_URL = "http://backend:8000"

st.set_page_config(page_title="Investor CRM", layout="wide")

st.title("🚀 AI Investor Outreach CRM")

# -------- FETCH LEADS --------
@st.cache_data(ttl=5)
def fetch_leads():
    try:
        res = requests.get(f"{BASE_URL}/leads/")
        return res.json()
    except:
        return []

leads = fetch_leads()
lead_map = {lead["id"]: lead for lead in leads}

# -------- ADD LEAD --------
with st.expander("➕ Add New Lead"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")

    with col2:
        linkedin = st.text_input("LinkedIn")
        tier = st.selectbox("Net Worth Tier", ["High", "Medium", "Low"])

    interests = st.text_input("Interest Areas (comma separated)")

    if st.button("Add Lead"):
        with st.spinner("Adding lead..."):
            requests.post(f"{BASE_URL}/leads/", json={
                "name": name,
                "email": email,
                "linkedin": linkedin,
                "net_worth_tier": tier,
                "interest_areas": interests.split(",")
            })

        st.toast("✅ Lead added")
        st.rerun()


# -------- DISPLAY LEADS --------
st.header("📋 Leads")

if not leads:
    st.info("No leads yet. Add your first investor 🚀")

cols = st.columns(2)

for i, lead in enumerate(leads):
    color = {
        "Cold": "#888",
        "Contacted": "#f39c12",
        "Interested": "#2ecc71",
        "Committed": "#3498db"
    }.get(lead["stage"], "#888")

    card_html = f"""
    <div style="padding:10px;border-radius:8px;border:1px solid #333;margin-bottom:10px;">
        <b>{lead['name']}</b>
        <span style="color:{color};font-size:12px;"> ● {lead['stage']}</span><br>
        <span style="font-size:13px;">📧 {lead['email']}</span><br>
        <span style="font-size:12px;color:gray;">{lead['interest_areas']}</span>
    </div>
    """

    with cols[i % 2]:
        st.markdown(card_html, unsafe_allow_html=True)


# -------- ACTIONS --------
st.header("⚙️ Actions")

if leads:
    selected_lead_id = st.selectbox(
        "Select Lead",
        list(lead_map.keys()),
        format_func=lambda x: f"{lead_map[x]['name']} ({lead_map[x]['stage']})"
    )

    col1, col2 = st.columns(2)

    # -------- UPDATE STAGE --------
    with col1:
        new_stage = st.selectbox(
            "Update Stage",
            ["Cold", "Contacted", "Interested", "Committed"]
        )

        if st.button("Update Stage"):
            with st.spinner("Updating stage..."):
                requests.patch(
                    f"{BASE_URL}/leads/{selected_lead_id}/stage",
                    json={"new_stage": new_stage}
                )

            st.toast("✅ Stage updated")
            st.rerun()

    # -------- ADD INTERACTION --------
    with col2:
        interaction_type = st.selectbox(
            "Interaction Type",
            ["call", "email", "meeting"]
        )
        notes = st.text_area("Notes")

        if st.button("Add Interaction"):
            with st.spinner("Saving interaction..."):
                requests.post(f"{BASE_URL}/interactions", json={
                    "lead_id": selected_lead_id,
                    "type": interaction_type,
                    "notes": notes
                })

            st.toast("✅ Interaction added")


# -------- REMINDERS --------
st.header("⏰ Reminders")

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Reminders"):
        with st.spinner("Generating smart reminders..."):
            requests.post(f"{BASE_URL}/reminders/generate")

        st.toast("⏰ Reminders generated")

with col2:
    if st.button("Load Reminders"):
        with st.spinner("Fetching reminders..."):
            res = requests.get(f"{BASE_URL}/reminders/")
            reminders = res.json()

        if not reminders:
            st.warning("No reminders yet ⚠️")
        else:
            for r in reminders:
                color = {
                    "High": "red",
                    "Medium": "orange",
                    "Low": "green"
                }.get(r["priority"], "gray")

                st.markdown(f"""
                <div style="padding:10px;border-left:5px solid {color};margin-bottom:10px;">
                    <b>{r['message']}</b><br>
                    Priority: <span style="color:{color}">{r['priority']}</span>
                </div>
                """, unsafe_allow_html=True)


# -------- AI SECTION --------
st.header("🤖 AI Insights")

if leads:
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✉️ Email"):
            with st.spinner("Generating email..."):
                res = requests.get(f"{BASE_URL}/ai/generate-email/{selected_lead_id}")
            st.code(res.json()["email"], language="markdown")

    with col2:
        if st.button("🧠 Summary"):
            with st.spinner("Summarizing..."):
                res = requests.get(f"{BASE_URL}/ai/summary/{selected_lead_id}")
            st.info(res.json()["summary"])

    with col3:
        if st.button("📊 Score"):
            res = requests.get(f"{BASE_URL}/ai/score/{selected_lead_id}")
            st.success(f"Score: {res.json()['score']}")


# -------- NEXT ACTION --------
st.header("🔥 Next Best Action")

if leads:
    if st.button("Get Recommendation"):
        with st.spinner("Thinking... 🤖"):
            res = requests.get(f"{BASE_URL}/ai/next-action/{selected_lead_id}")

        st.success("🔥 " + res.json()["next_action"])