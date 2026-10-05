import streamlit as st
import pandas as pd
import ollama
from datetime import datetime

# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="ResQNet",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# THEME
# ==========================================================

st.markdown("""
<style>

:root {
    --bg: #080d18;
    --sidebar: #0b1220;
    --card: #111827;
    --card2: #0f172a;
    --border: #243044;
    --text: #f8fafc;
    --muted: #94a3b8;
    --blue: #3b82f6;
    --cyan: #22d3ee;
    --red: #ef4444;
    --orange: #f59e0b;
    --green: #22c55e;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% -10%,
            rgba(37, 99, 235, 0.18),
            transparent 35%
        ),
        var(--bg);
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Normal text */

p, label {
    color: var(--muted);
}

/* Headings */

h1, h2, h3 {
    color: var(--text) !important;
}

/* Navigation radio */

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 6px;
}

[data-testid="stSidebar"] [role="radio"] {
    padding: 12px 14px;
    border-radius: 10px;
    transition: 0.2s;
}

[data-testid="stSidebar"] [role="radio"]:hover {
    background: #172033;
}

[data-testid="stSidebar"] [role="radio"] label {
    color: #cbd5e1 !important;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
    border: 1px solid #334155;
    background: #172033;
    color: white;
}

.stButton > button:hover {
    border-color: var(--blue);
    background: #1d4ed8;
    color: white;
}

/* Inputs */

.stTextInput input,
.stTextArea textarea {
    background: #0f172a !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

[data-baseweb="select"] {
    background: #0f172a !important;
}

[data-baseweb="select"] * {
    color: white !important;
}

/* Metrics */

[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* Divider */

hr {
    border-color: var(--border);
}

/* Alert boxes */

.alert-card {
    padding: 16px;
    border-radius: 12px;
    margin: 8px 0;
    background: var(--card);
    border: 1px solid var(--border);
}

.alert-red {
    border-left: 4px solid var(--red);
}

.alert-orange {
    border-left: 4px solid var(--orange);
}

.alert-green {
    border-left: 4px solid var(--green);
}

/* Logo */

.brand {
    text-align: center;
    padding: 10px 0 22px 0;
}

.brand-icon {
    font-size: 42px;
}

.brand-name {
    font-size: 27px;
    font-weight: 800;
    color: white;
    letter-spacing: -1px;
}

.brand-tag {
    color: #64748b;
    font-size: 9px;
    letter-spacing: 2px;
}

/* Page heading */

.page-title {
    font-size: 34px;
    font-weight: 800;
    color: white;
    letter-spacing: -1px;
}

.page-subtitle {
    color: #64748b;
    margin-bottom: 25px;
}

/* Section title */

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: white;
    margin-top: 25px;
    margin-bottom: 8px;
}

/* Cards */

.feature-card {
    background: linear-gradient(
        145deg,
        #111827,
        #0d1525
    );
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 20px;
    height: 100%;
}

.feature-icon {
    font-size: 25px;
}

.feature-title {
    color: white;
    font-weight: 700;
    font-size: 16px;
    margin-top: 10px;
}

.feature-text {
    color: #64748b;
    font-size: 13px;
    line-height: 1.6;
}

/* AI panel */

.ai-panel {
    background:
        linear-gradient(
            135deg,
            rgba(30, 64, 175, 0.30),
            rgba(15, 23, 42, 0.9)
        );
    border: 1px solid #1e40af;
    border-radius: 16px;
    padding: 22px;
}

/* Status pill */

.online {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    background: rgba(34, 197, 94, 0.12);
    color: #4ade80;
    font-size: 11px;
    font-weight: 700;
}

/* Footer */

.app-footer {
    text-align: center;
    color: #475569;
    font-size: 11px;
    padding: 35px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================

if "requests" not in st.session_state:
    st.session_state.requests = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🚨</div>
        <div class="brand-name">ResQNet</div>
        <div class="brand-tag">
            EMERGENCY RESPONSE NETWORK
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "AI Emergency Assistant",
            "Emergency Requests",
            "Disaster Alerts",
            "Resource Locator",
            "Response Teams",
            "Analytics"
        ],
        index=[
            "Dashboard",
            "AI Emergency Assistant",
            "Emergency Requests",
            "Disaster Alerts",
            "Resource Locator",
            "Response Teams",
            "Analytics"
        ].index(st.session_state.page)
    )

    st.session_state.page = page

    st.divider()

    st.caption("SYSTEM STATUS")

    st.success("AI Engine • Online")
    st.success("Response Network • Online")
    st.success("Data System • Online")

    st.divider()

    st.caption("ResQNet v1.0")
    st.caption("Powered by Streamlit + Ollama")


# ==========================================================
# HEADER FUNCTION
# ==========================================================

def header(title, subtitle):

    left, right = st.columns([5, 1])

    with left:
        st.markdown(
            f'<div class="page-title">{title}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="page-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            '<div style="text-align:right;">'
            '<span class="online">● SYSTEM ONLINE</span>'
            '</div>',
            unsafe_allow_html=True
        )


# ==========================================================
# DASHBOARD
# ==========================================================

if page == "Dashboard":

    header(
        "Emergency Command Center",
        "Monitor disasters, emergency requests and response operations."
    )

    # -----------------------------
    # METRICS
    # -----------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🚨 Active Incidents",
        "07",
        "+2 today"
    )

    c2.metric(
        "🆘 Open Requests",
        str(len(st.session_state.requests)),
        "Live"
    )

    c3.metric(
        "🚑 Response Teams",
        "12",
        "9 available"
    )

    c4.metric(
        "🏥 Relief Centers",
        "18",
        "14 active"
    )

    # -----------------------------
    # MAIN GRID
    # -----------------------------

    left, right = st.columns([1.7, 1])

    with left:

        st.markdown(
            '<div class="section-title">🚨 Priority Incidents</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="alert-card alert-red">
            <b style="color:white;">
            🔴 Flood Warning
            </b>
            <br>
            <span style="color:#94a3b8;">
            High priority • Hyderabad • Response teams alerted
            </span>
        </div>

        <div class="alert-card alert-orange">
            <b style="color:white;">
            🟠 Heavy Rainfall
            </b>
            <br>
            <span style="color:#94a3b8;">
            Medium priority • Secunderabad • Monitoring
            </span>
        </div>

        <div class="alert-card alert-green">
            <b style="color:white;">
            🟢 Strong Wind
            </b>
            <br>
            <span style="color:#94a3b8;">
            Low priority • Kukatpally • Monitoring
            </span>
        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="section-title">📡 Operations</div>',
            unsafe_allow_html=True
        )

        st.write("Requests resolved")
        st.progress(0.76)

        st.write("Resources available")
        st.progress(0.84)

        st.write("Teams deployed")
        st.progress(0.61)

    # -----------------------------
    # AI SECTION
    # -----------------------------

    st.markdown(
        '<div class="section-title">🤖 AI Intelligence</div>',
        unsafe_allow_html=True
    )

    ai1, ai2, ai3 = st.columns(3)

    with ai1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">
                Emergency Analysis
            </div>
            <div class="feature-text">
                Use Ollama AI to analyze emergency reports,
                identify severity and recommend actions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ai2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📍</div>
            <div class="feature-title">
                Resource Coordination
            </div>
            <div class="feature-text">
                Identify suitable emergency resources
                based on the reported situation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ai3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">
                Priority Detection
            </div>
            <div class="feature-text">
                Help responders understand which
                requests require urgent attention.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # QUICK ACTIONS
    # -----------------------------

    st.markdown(
        '<div class="section-title">Quick Actions</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button(
            "🤖 Open AI Assistant",
            use_container_width=True
        ):
            st.session_state.page = "AI Emergency Assistant"
            st.rerun()

    with q2:
        if st.button(
            "🆘 Create Emergency Request",
            use_container_width=True
        ):
            st.session_state.page = "Emergency Requests"
            st.rerun()

    with q3:
        if st.button(
            "🚨 View Disaster Alerts",
            use_container_width=True
        ):
            st.session_state.page = "Disaster Alerts"
            st.rerun()


# ==========================================================
# AI EMERGENCY ASSISTANT
# ==========================================================

elif page == "AI Emergency Assistant":

    header(
        "AI Emergency Assistant",
        "AI-powered emergency situation analysis using Ollama."
    )

    st.markdown("""
    <div class="ai-panel">

    <h3 style="color:white;">
    🧠 ResQNet Intelligence Engine
    </h3>

    <p>
    Describe the emergency situation below. ResQNet AI will
    analyze the situation and provide structured emergency guidance.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    location = st.text_input(
        "📍 Location",
        placeholder="Example: Hyderabad, Telangana"
    )

    emergency = st.text_area(
        "🚨 Describe the emergency",
        height=180,
        placeholder=(
            "Example: Heavy flooding has affected my area. "
            "Water has entered several houses and some people "
            "need immediate evacuation."
        )
    )

    if st.button(
        "🧠 ANALYZE WITH OLLAMA",
        use_container_width=True
    ):

        if not emergency.strip():

            st.warning(
                "Please describe the emergency situation."
            )

        else:

            prompt = f"""
You are ResQNet AI, an emergency-response intelligence assistant.

Location:
{location}

Emergency report:
{emergency}

Analyze this emergency report.

Return your answer with exactly these sections:

### Emergency Type
### Severity
### Immediate Risks
### Recommended Actions
### Required Resources
### Response Priority

Be concise, practical and safety-focused.

Do not claim that you contacted emergency services.
Do not invent real-time information.
"""

            try:

                with st.spinner(
                    "ResQNet AI is analyzing the situation..."
                ):

                    result = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                st.divider()

                st.subheader(
                    "🧠 AI Emergency Assessment"
                )

                st.markdown(
                    result["message"]["content"]
                )

                st.warning(
                    "AI guidance does not replace professional "
                    "emergency services."
                )

            except Exception as error:

                st.error(
                    "Ollama could not be reached."
                )

                st.info(
                    "Make sure Ollama is running and "
                    "llama3.2 is installed."
                )


# ==========================================================
# EMERGENCY REQUESTS
# ==========================================================

elif page == "Emergency Requests":

    header(
        "Emergency Requests",
        "Register and prioritize requests for assistance."
    )

    with st.form("emergency_form"):

        name = st.text_input(
            "Full Name"
        )

        phone = st.text_input(
            "Contact Number"
        )

        location = st.text_input(
            "📍 Current Location"
        )

        emergency_type = st.selectbox(
            "Emergency Type",
            [
                "Medical Emergency",
                "Flood",
                "Fire",
                "Accident",
                "Missing Person",
                "Food / Water",
                "Shelter",
                "Other"
            ]
        )

        priority = st.selectbox(
            "Priority",
            [
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

        description = st.text_area(
            "Emergency Description"
        )

        submitted = st.form_submit_button(
            "🚨 SUBMIT EMERGENCY REQUEST"
        )

        if submitted:

            if not name or not phone or not location:

                st.error(
                    "Please complete your name, contact number "
                    "and location."
                )

            else:

                request_id = (
                    "RQ-"
                    + datetime.now().strftime("%Y%m%d%H%M%S")
                )

                st.session_state.requests.append({
                    "ID": request_id,
                    "Type": emergency_type,
                    "Location": location,
                    "Priority": priority,
                    "Status": "Pending"
                })

                st.success(
                    "Emergency request registered successfully."
                )

                st.info(
                    f"Request ID: {request_id}"
                )

    # Show submitted requests

    if st.session_state.requests:

        st.divider()

        st.subheader("Current Requests")

        st.dataframe(
            pd.DataFrame(st.session_state.requests),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# DISASTER ALERTS
# ==========================================================

elif page == "Disaster Alerts":

    header(
        "Disaster Alerts",
        "Monitor reported disaster situations and severity."
    )

    alerts = pd.DataFrame({
        "Alert": [
            "Flood Warning",
            "Heavy Rainfall",
            "Strong Wind",
            "Road Waterlogging"
        ],
        "Location": [
            "Hyderabad",
            "Secunderabad",
            "Kukatpally",
            "Madhapur"
        ],
        "Severity": [
            "High",
            "Medium",
            "Low",
            "Medium"
        ],
        "Status": [
            "Active",
            "Monitoring",
            "Monitoring",
            "Active"
        ]
    })

    st.dataframe(
        alerts,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "This demonstration uses sample alert data. "
        "Real ResQNet alerts can later be connected to APIs "
        "or a database."
    )


# ==========================================================
# RESOURCE LOCATOR
# ==========================================================

elif page == "Resource Locator":

    header(
        "Resource Locator",
        "Find emergency facilities and relief resources."
    )

    resource_type = st.selectbox(
        "Filter resources",
        [
            "All",
            "Hospital",
            "Shelter",
            "Food",
            "Water",
            "Emergency Unit"
        ]
    )

    resources = pd.DataFrame({
        "Resource": [
            "Emergency Hospital",
            "Community Shelter",
            "Food Distribution Center",
            "Water Distribution Point",
            "Emergency Response Unit"
        ],
        "Type": [
            "Hospital",
            "Shelter",
            "Food",
            "Water",
            "Emergency Unit"
        ],
        "Location": [
            "Hyderabad",
            "Secunderabad",
            "Kukatpally",
            "Madhapur",
            "Banjara Hills"
        ],
        "Status": [
            "Available",
            "Available",
            "Limited",
            "Available",
            "Available"
        ]
    })

    if resource_type != "All":

        resources = resources[
            resources["Type"] == resource_type
        ]

    st.dataframe(
        resources,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# RESPONSE TEAMS
# ==========================================================

elif page == "Response Teams":

    header(
        "Response Operations",
        "Monitor emergency response teams and deployment status."
    )

    teams = pd.DataFrame({
        "Team": [
            "Alpha",
            "Bravo",
            "Charlie",
            "Delta",
            "Echo"
        ],
        "Specialization": [
            "Medical",
            "Fire & Rescue",
            "Flood Response",
            "Rapid Response",
            "Logistics"
        ],
        "Location": [
            "Hyderabad",
            "Secunderabad",
            "Kukatpally",
            "Madhapur",
            "Banjara Hills"
        ],
        "Status": [
            "Available",
            "Deployed",
            "Available",
            "Standby",
            "Available"
        ]
    })

    st.dataframe(
        teams,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# ANALYTICS
# ==========================================================

elif page == "Analytics":

    header(
        "Response Analytics",
        "Operational insights from ResQNet emergency activity."
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Total Requests",
        "124",
        "+18"
    )

    b.metric(
        "Resolved",
        "96",
        "+12"
    )

    c.metric(
        "Pending",
        "28",
        "-6"
    )

    d.metric(
        "Avg Response",
        "14 min",
        "-3 min"
    )

    st.divider()

    st.subheader(
        "Emergency Request Distribution"
    )

    chart_data = pd.DataFrame({
        "Emergency Type": [
            "Medical",
            "Flood",
            "Fire",
            "Accident",
            "Shelter"
        ],
        "Requests": [
            34,
            28,
            17,
            25,
            20
        ]
    })

    st.bar_chart(
        chart_data.set_index("Emergency Type")
    )

    st.subheader(
        "Response Performance"
    )

    performance = pd.DataFrame({
        "Metric": [
            "Requests Resolved",
            "Teams Available",
            "Resources Available"
        ],
        "Percentage": [
            76,
            84,
            91
        ]
    })

    st.bar_chart(
        performance.set_index("Metric")
    )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div class="app-footer">

RESQNET • AI-POWERED DISASTER & EMERGENCY RESPONSE NETWORK

<br>

Python • Streamlit • Ollama

</div>
""", unsafe_allow_html=True)