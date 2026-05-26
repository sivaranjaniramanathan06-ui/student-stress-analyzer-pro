import streamlit as st
import sqlite3
from datetime import datetime, date
import pytz
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Student Stress Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* Main App */

.stApp{
    background:#D5D8DC;
    color:#0F172A;
}

/* Headings */

h1,h2,h3{
    color:#0F172A !important;
    font-weight:800;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background-color:#0F172A !important;
}

[data-testid="stSidebar"] > div:first-child{
    background-color:#0F172A !important;
}

[data-testid="stSidebarNav"]{
    background-color:#0F172A !important;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

/* Inputs */

.stTextInput input,
.stDateInput input{
    background:white !important;
    color:#0F172A !important;
    border-radius:10px !important;
    border:1px solid #0F172A !important;
}

/* Selectbox */

.stSelectbox div[data-baseweb="select"]{
    background:white !important;
    color:#0F172A !important;
    border-radius:10px !important;
}

/* Sliders */

.stSlider{
    background:white;
    padding:15px;
    border-radius:15px;
    margin-bottom:15px;
    border:1px solid #CBD5E1;
}

/* Buttons */

div.stButton > button{
    background-color:#0F172A !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:10px 24px !important;
    font-weight:700 !important;
    font-size:16px !important;
    width:100%;
}

/* Hover */

div.stButton > button:hover{
    background-color:#1E293B !important;
    color:white !important;
}

/* Metrics */

div[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    border-left:5px solid #0F172A;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect(
    'student_stress.db',
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# CREATE TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS stress_data (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,
    dob TEXT,
    gender TEXT,

    study_hours INTEGER,
    sleep_hours INTEGER,
    screen_time INTEGER,
    exercise_hours INTEGER,
    exam_score INTEGER,

    stress_score INTEGER,
    stress_level TEXT,
    recommendation TEXT,

    analysis_date TEXT
)
""")

conn.commit()

# =========================
# TITLE
# =========================

st.title("🍃Student Stress-Level Analysis")

st.write(
    "Analyze individual student wellness and stress levels."
)

# =========================
# INPUT AREA
# =========================

left_col, right_col = st.columns(2)

# LEFT

with left_col:

    student_name = st.text_input(
        "👤 Student Name"
    )

    dob = st.date_input(
        "📅 Date of Birth",
        min_value=date(1995,1,1),
        max_value=date.today()
    )

    gender = st.selectbox(
        "⚧ Gender",
        ["Male","Female","Other"]
    )


# BUTTON POSITION
analyze = st.button(
    "🚀 Analyze Stress"
)

# RIGHT

with right_col:

    study_hours = st.slider(
        "📚 Study Hours",
        0,
        15,
        6
    )

    sleep_hours = st.slider(
        "😴 Sleep Hours",
        0,
        12,
        7
    )

    screen_time = st.slider(
        "📱 Screen Time",
        0,
        12,
        4
    )

    exercise_hours = st.slider(
        "🏃 Exercise Hours",
        0,
        5,
        1
    )

    exam_score = st.slider(
        "📝 Exam Score",
        0,
        100,
        75
    )

# =========================
# ANALYSIS
# =========================

if analyze:

    stress_score = 0

    if study_hours > 8:
        stress_score += 30

    if sleep_hours < 6:
        stress_score += 30

    if screen_time > 5:
        stress_score += 20

    if exercise_hours == 0:
        stress_score += 20

    # STRESS LEVEL

    if stress_score >= 70:
        stress_level = "High"

    elif stress_score >= 40:
        stress_level = "Medium"

    else:
        stress_level = "Low"

    # RECOMMENDATION

    if stress_level == "High":

        recommendation = (
            "High stress detected. Improve sleep, reduce screen time, exercise daily, and take breaks."
        )

    elif stress_level == "Medium":

        recommendation = (
            "Moderate stress detected. Maintain healthy balance and relaxation."
        )

    else:

        recommendation = (
            "Healthy lifestyle maintained."
        )

    # INDIAN TIME

    india_time = datetime.now(
        pytz.timezone('Asia/Kolkata')
    ).strftime("%Y-%m-%d %H:%M:%S")

    # SAVE TO DATABASE

    cursor.execute("""
    INSERT INTO stress_data (

        student_name,
        dob,
        gender,

        study_hours,
        sleep_hours,
        screen_time,
        exercise_hours,
        exam_score,

        stress_score,
        stress_level,
        recommendation,

        analysis_date

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,

    (

        student_name,
        str(dob),
        gender,

        study_hours,
        sleep_hours,
        screen_time,
        exercise_hours,
        exam_score,

        stress_score,
        stress_level,
        recommendation,

        india_time
    ))

    conn.commit()

    # =========================
    # REPORT
    # =========================

    st.success(
        "✅ Student analysis saved successfully."
    )

    st.subheader(
        "📊 Individual Stress Analysis Report"
    )

    m1,m2,m3 = st.columns(3)

    m1.metric(
        "Stress Score",
        stress_score
    )

    m2.metric(
        "Stress Level",
        stress_level
    )

    m3.metric(
        "Exam Score",
        exam_score
    )

    # =========================
    # PIE CHART
    # =========================

    chart_data = pd.DataFrame({

        "Category":[
            "Study",
            "Sleep",
            "Screen",
            "Exercise"
        ],

        "Value":[
            study_hours,
            sleep_hours,
            screen_time,
            exercise_hours
        ]
    })

    pie_chart = px.pie(
        chart_data,
        names="Category",
        values="Value",
        title="Student Lifestyle Distribution"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    # =========================
    # WELLNESS SUGGESTIONS
    # =========================

    st.subheader(
        "🧠 Wellness Suggestions"
    )

    if sleep_hours < 6:

        st.warning(
            "😴 Improve sleep duration."
        )

    if screen_time > 5:

        st.warning(
            "📱 Reduce screen time."
        )

    if exercise_hours == 0:

        st.warning(
            "🏃 Add daily exercise."
        )

    if study_hours > 8:

        st.warning(
            "📚 Avoid excessive study hours without breaks."
        )

    st.success(recommendation)