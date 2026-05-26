import streamlit as st

st.set_page_config(
    page_title="Student Stress Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.block-container {
    background-color: #EAF4FF !important;
}

[data-testid="stSidebar"] {
    background: #0F172A !important;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    max-width: 1180px;
}

.hero {
    background: linear-gradient(135deg, #FFFFFF 0%, #EEF2FF 100%);
    padding: 55px 45px;
    border-radius: 30px;
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.10);
    border: 1px solid #E2E8F0;
    text-align: center;
}

.hero-title {
    font-size: 58px;
    font-weight: 900;
    color: #0F172A !important;
    margin-bottom: 12px;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 23px;
    color: #475569 !important;
    font-weight: 500;
}

.quote {
    margin-top: 22px;
    font-size: 18px;
    color: #6366F1 !important;
    font-style: italic;
    font-weight: 600;
}

.feature-card {
    background: #FFFFFF;
    padding: 34px 28px;
    border-radius: 24px;
    min-height: 230px;
    box-shadow: 0 14px 35px rgba(15, 23, 42, 0.10);
    border: 1px solid #E2E8F0;
    text-align: center;
    transition: 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 45px rgba(99, 102, 241, 0.20);
    border: 1px solid #C7D2FE;
}

.feature-card h2 {
    color: #0F172A !important;
    font-size: 27px;
    margin-bottom: 14px;
    font-weight: 800;
}

.feature-card p {
    color: #475569 !important;
    font-size: 16px;
    line-height: 1.7;
}

.info-box {
    background: #FFFFFF;
    color: #1E293B !important;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    font-weight: 700;
    border-left: 6px solid #10B981;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
}

.highlight {
    color: #6366F1 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">Student Stress Analyzer</div>
    <div class="hero-subtitle">
        Smart wellness tracking system for student stress monitoring and improvement analysis
    </div>
    <div class="quote">
        “Understand stress early. Improve habits steadily. Build a healthier academic life.”
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>📊 Stress Analytics</h2>
        <p>
        Evaluates stress using study hours, sleep duration, screen time,
        exercise habits, and academic performance.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2>📈 Progress Tracking</h2>
        <p>
        Compares previous and current stress reports to identify improvement
        areas and lifestyle changes.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2>🔐 Secure Records</h2>
        <p>
        Stores student records in a database and provides admin-controlled
        report access and record management.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

st.markdown(
    "<div class='info-box'>Use the sidebar to enter student data, analyze reports, and manage saved records securely.</div>",
    unsafe_allow_html=True
)