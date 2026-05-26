import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Student Stress Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM STYLING
# =========================

st.markdown("""
<style>

.stApp{
    background:#D5D8DC;
    color:#0F172A;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarNav"]{
    background-color:#0F172A !important;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

h1,h2,h3,h4{
    color:#0F172A !important;
    font-weight:800;
}

div[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:15px;
    border-left:5px solid #0F172A;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}

table{
    border-collapse:collapse !important;
    width:100% !important;
    border:2px solid #0F172A !important;
    background:white !important;
}

thead tr th{
    background-color:#BFC5CC !important;
    color:#0F172A !important;
    border:1.5px solid #0F172A !important;
    padding:10px !important;
    font-weight:800 !important;
    text-align:center !important;
}

tbody tr td{
    border:1.5px solid #0F172A !important;
    color:#111827 !important;
    padding:10px !important;
    text-align:center !important;
    font-weight:500 !important;
}

div.stDownloadButton > button{
    background-color:#0F172A !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:10px 22px !important;
    font-weight:700 !important;
}

div.stButton > button{
    background-color:#0F172A !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:10px 22px !important;
    font-weight:700 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect(
    "student_stress.db",
    check_same_thread=False
)

st.title("📈 Student Stress Analysis Dashboard")

st.write(
    "Analyze student wellness trends, stress history, and improvement progress."
)

# =========================
# LOAD DATABASE
# =========================

data = pd.read_sql(
    "SELECT * FROM stress_data",
    conn
)

# =========================
# EMPTY DATABASE CHECK
# =========================

if len(data) == 0:

    st.warning(
        "⚠ No student records found."
    )

# =========================
# MAIN SECTION
# =========================

else:

    # =========================
    # SEARCH SECTION
    # =========================

    st.subheader("🔍 Search Your Previous Records")

    search_col1, search_col2, search_col3 = st.columns(3)

    with search_col1:

        entered_name = st.text_input(
            "Enter Student Name"
        )

    with search_col2:

        entered_dob = st.text_input(
            "Enter DOB (YYYY-MM-DD)"
        )

    with search_col3:

        entered_gender = st.selectbox(
            "Select Gender",
            ["Male", "Female", "Other"]
        )

    search_button = st.button(
        "🔎 Search Student Records"
    )

    if search_button:

        student_data = data[

            (data["student_name"].str.lower()
            == entered_name.lower())

            &

            (data["dob"].astype(str)
            == entered_dob)

            &

            (data["gender"]
            == entered_gender)

        ].copy()

        # =========================
        # NO RECORDS FOUND
        # =========================

        if len(student_data) == 0:

            st.error(
                "❌ No matching student records found."
            )

            st.stop()

        # =========================
        # STUDENT IDENTITY
        # =========================

        student_data["student_identity"] = (

            student_data["student_name"]
            + " | "
            + student_data["dob"]
            + " | "
            + student_data["gender"]
        )

        # =========================
        # DATE CONVERSION
        # =========================

        student_data["analysis_date"] = pd.to_datetime(
            student_data["analysis_date"]
        )

        # =========================
        # SORT DATA
        # =========================

        student_data = student_data.sort_values(
            by="analysis_date"
        )

        latest = student_data.iloc[-1]

        # =========================
        # STUDENT DETAILS
        # =========================

        st.subheader("👤 Student Details")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "👤 Name",
            latest["student_name"]
        )

        col2.metric(
            "📅 DOB",
            latest["dob"]
        )

        col3.metric(
            "⚧ Gender",
            latest["gender"]
        )

        # =========================
        # CURRENT ANALYSIS
        # =========================

        st.subheader("📊 Current Analysis")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Stress Score",
            latest["stress_score"]
        )

        m2.metric(
            "Stress Level",
            latest["stress_level"]
        )

        m3.metric(
            "Study Hours",
            latest["study_hours"]
        )

        m4.metric(
            "Sleep Hours",
            latest["sleep_hours"]
        )

        # =========================
        # STRESS TREND GRAPH
        # =========================

        st.subheader(
            "📈 Student Stress Trend Over Time"
        )

        trend_fig = px.line(

            student_data,

            x="analysis_date",

            y="stress_score",

            markers=True,

            title="Stress Score Progress"
        )

        trend_fig.update_traces(

            line=dict(
                color="#0F172A",
                width=3
            ),

            marker=dict(
                size=9,
                color="#2563EB"
            )
        )

        trend_fig.update_layout(

            plot_bgcolor="#EEF2F7",

            paper_bgcolor="#EEF2F7",

            font=dict(
                color="black"
            ),

            title_font=dict(
                color="black"
            ),

            xaxis=dict(
                showgrid=True,
                gridcolor="black",
                linecolor="black",
                tickfont=dict(color="black"),
                title_font=dict(color="black")
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="black",
                linecolor="black",
                tickfont=dict(color="black"),
                title_font=dict(color="black")
            )
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True
        )

        # =========================
        # LIFESTYLE GRAPH
        # =========================

        st.subheader(
            "📊 Lifestyle Comparison Analysis"
        )

        comparison_fig = px.bar(

            student_data,

            x="analysis_date",

            y=[
                "study_hours",
                "sleep_hours",
                "screen_time",
                "exercise_hours"
            ],

            barmode="group",

            title="Lifestyle Changes Over Time"
        )

        comparison_fig.update_layout(

            plot_bgcolor="#EEF2F7",

            paper_bgcolor="#EEF2F7",

            font=dict(color="black"),

            title_font=dict(color="black"),

            xaxis=dict(
                showgrid=True,
                gridcolor="black",
                linecolor="black",
                tickfont=dict(color="black"),
                title_font=dict(color="black")
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="black",
                linecolor="black",
                tickfont=dict(color="black"),
                title_font=dict(color="black")
            )
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )

        # =========================
        # PREVIOUS RECORDS
        # =========================

        st.subheader(
            "📄 Previous Student Records"
        )

        display_table = student_data[[
            "study_hours",
            "sleep_hours",
            "screen_time",
            "exercise_hours",
            "exam_score",
            "stress_score",
            "stress_level",
            "recommendation",
            "analysis_date"
        ]]

        st.markdown(
            display_table.to_html(index=False),
            unsafe_allow_html=True
        )

        # =========================
        # PDF DOWNLOAD
        # =========================

        pdf_buffer = BytesIO()

        pdf = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "Previous Student Stress Records",
                styles["Title"]
            )
        )

        pdf_data = [
            display_table.columns.tolist()
        ] + display_table.astype(str).values.tolist()

        table = Table(
            pdf_data,
            repeatRows=1
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ]))

        elements.append(table)

        pdf.build(elements)

        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Download Previous Student Records PDF",
            data=pdf_buffer,
            file_name="previous_student_records.pdf",
            mime="application/pdf"
        )

        # =========================
        # ALERT SECTION
        # =========================

        st.subheader(
            "🚨 Stress Detection Alert"
        )

        latest_stress = latest["stress_score"]

        if latest_stress >= 70:

            st.error(
                "🚨 HIGH STRESS DETECTED!"
            )

        elif latest_stress >= 40:

            st.warning(
                "⚠ Moderate stress detected."
            )

        else:

            st.success(
                "✅ Stress level looks healthy."
            )

        # =========================
        # PROGRESS COMPARISON
        # =========================

        if len(student_data) >= 2:

            first_score = student_data.iloc[0][
                "stress_score"
            ]

            latest_score = latest[
                "stress_score"
            ]

            improvement = (
                first_score - latest_score
            )

            st.subheader(
                "📉 Stress Progress Comparison"
            )

            if improvement > 0:

                st.success(
                    f"✅ Stress improved by {improvement} points!"
                )

            elif improvement < 0:

                st.error(
                    f"🚨 Stress increased by {abs(improvement)} points!"
                )

            else:

                st.info(
                    "ℹ No overall stress change detected."
                )

        # =========================
        # SUGGESTIONS
        # =========================

        st.subheader(
            "🧠 Improvement Areas & Suggestions"
        )

        improvement_found = False

        if latest["sleep_hours"] < 6:

            st.warning(
                "😴 Improve sleep duration for better mental wellness."
            )

            improvement_found = True

        if latest["screen_time"] > 5:

            st.warning(
                "📱 Reduce excessive screen time."
            )

            improvement_found = True

        if latest["exercise_hours"] == 0:

            st.warning(
                "🏃 Add daily physical exercise."
            )

            improvement_found = True

        if latest["study_hours"] > 8:

            st.warning(
                "📚 Avoid continuous long study hours without breaks."
            )

            improvement_found = True

        if improvement_found == False:

            st.success(
                "✅ No major improvement areas detected."
            )

    else:

        st.info(
            "👆 Enter your details and click search."
        )