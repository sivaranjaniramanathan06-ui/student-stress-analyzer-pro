import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime
import pytz
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, A4

st.set_page_config(
    page_title="CSV Stress Analyzer",
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


[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarNav"] {
    background-color: #0F172A !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3 {
    color: #0F172A !important;
    font-weight: 800;
}

div[data-testid="stMetric"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
    border-left: 5px solid #0F172A;
}

div.stButton > button,
div.stDownloadButton > button {
    background-color: #0F172A !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 700 !important;
}

.custom-table table {
    width: 100%;
    border-collapse: collapse !important;
    border: 2px solid #0F172A !important;
    background-color: white !important;
}

.custom-table th {
    background-color: #D5D8DC !important;
    color: #0F172A !important;
    border: 1.5px solid #0F172A !important;
    padding: 10px !important;
    font-weight: 800 !important;
    text-align: center !important;
}

.custom-table td {
    border: 1.5px solid #0F172A !important;
    color: #111827 !important;
    padding: 10px !important;
    text-align: center !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect(
    "student_stress.db",
    check_same_thread=False
)

cursor = conn.cursor()

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

st.title("📊 CSV Student Stress Analysis Dashboard")

st.write("Upload a CSV file to analyze overall student stress patterns.")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

def calculate_stress(row):
    score = 0

    if row["StudyHours"] > 8:
        score += 30

    if row["SleepHours"] < 6:
        score += 30

    if row["ScreenTime"] > 5:
        score += 20

    if row["ExerciseHours"] == 0:
        score += 20

    return min(score, 100)


def stress_level(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


def recommendation(level):
    if level == "High":
        return "Improve sleep, reduce screen time, exercise daily."
    elif level == "Medium":
        return "Maintain balance and practice relaxation."
    else:
        return "Healthy lifestyle maintained."


def style_graph(fig):
    fig.update_layout(
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="#F8FAFC",
        font=dict(color="black"),
        title_font=dict(color="black"),
        legend_font=dict(color="black"),
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
    return fig


def create_pdf_report(filtered_data, high_stress):
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
            "Student Stress Analysed Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 18))

    metrics_text = f"""
    <b>Total Students:</b> {len(filtered_data)}
    <br/><br/>
    <b>Average Stress Score:</b> {round(filtered_data["StressScore"].mean(), 1)}
    <br/><br/>
    <b>High Stress Students:</b> {len(high_stress)}
    <br/><br/>
    <b>Average Sleep Hours:</b> {round(filtered_data["SleepHours"].mean(), 1)}
    """

    elements.append(
        Paragraph(
            metrics_text,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 18))

    elements.append(
        Paragraph(
            "Student Dataset",
            styles["Heading2"]
        )
    )

    pdf_table_data = filtered_data.drop(
        columns=["DisplayScore"]
    )

    table_data = [
        pdf_table_data.columns.tolist()
    ] + pdf_table_data.astype(str).values.tolist()

    report_table = Table(
        table_data,
        repeatRows=1
    )

    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elements.append(report_table)
    elements.append(Spacer(1, 18))

    elements.append(
        Paragraph(
            "High Stress Students",
            styles["Heading2"]
        )
    )

    if len(high_stress) > 0:
        high_table_data = high_stress.drop(
            columns=["DisplayScore"]
        )

        high_pdf_data = [
            high_table_data.columns.tolist()
        ] + high_table_data.astype(str).values.tolist()

        high_table = Table(
            high_pdf_data,
            repeatRows=1
        )

        high_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        elements.append(high_table)

    else:
        elements.append(
            Paragraph(
                "No high stress students detected.",
                styles["BodyText"]
            )
        )

    pdf.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer


if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    required_columns = [
        "Student",
        "DOB",
        "Gender",
        "StudyHours",
        "SleepHours",
        "ScreenTime",
        "ExerciseHours",
        "ExamScore"
    ]

    missing = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing:

        st.error(f"Missing columns: {missing}")

    else:

        data["StressScore"] = data.apply(
            calculate_stress,
            axis=1
        )

        data["StressLevel"] = data["StressScore"].apply(
            stress_level
        )

        data["Recommendation"] = data["StressLevel"].apply(
            recommendation
        )

        data["DisplayScore"] = data["StressScore"].replace(0, 3)

        st.success("✅ CSV uploaded and analyzed successfully.")

        st.subheader("🔍 Filter & Sort Students")

        f1, f2 = st.columns(2)

        with f1:
            selected_level = st.selectbox(
                "Filter by Stress Level",
                ["All", "High", "Medium", "Low"]
            )

        with f2:
            sort_option = st.selectbox(
                "Sort by Stress Score",
                [
                    "Highest to Lowest",
                    "Lowest to Highest"
                ]
            )

        filtered_data = data.copy()

        if selected_level != "All":
            filtered_data = filtered_data[
                filtered_data["StressLevel"] == selected_level
            ]

        if sort_option == "Highest to Lowest":
            filtered_data = filtered_data.sort_values(
                by="StressScore",
                ascending=False
            )
        else:
            filtered_data = filtered_data.sort_values(
                by="StressScore",
                ascending=True
            )

        save_csv = st.button(
            "💾 Save CSV Records to Student Stress Records"
        )

        if save_csv:

            india_time = datetime.now(
                pytz.timezone("Asia/Kolkata")
            ).strftime("%Y-%m-%d %H:%M:%S")

            for index, row in filtered_data.iterrows():

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
                """, (
                    row["Student"],
                    row["DOB"],
                    row["Gender"],
                    int(row["StudyHours"]),
                    int(row["SleepHours"]),
                    int(row["ScreenTime"]),
                    int(row["ExerciseHours"]),
                    int(row["ExamScore"]),
                    int(row["StressScore"]),
                    row["StressLevel"],
                    row["Recommendation"],
                    india_time
                ))

            conn.commit()

            st.success("✅ CSV records saved successfully.")

        st.subheader("📌 Dashboard Metrics")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Students",
            len(filtered_data)
        )

        c2.metric(
            "Average Stress",
            round(filtered_data["StressScore"].mean(), 1)
        )

        c3.metric(
            "High Stress Count",
            len(filtered_data[filtered_data["StressLevel"] == "High"])
        )

        c4.metric(
            "Average Sleep",
            round(filtered_data["SleepHours"].mean(), 1)
        )

        st.subheader("📄 Student Dataset")

        dataset_html = filtered_data.drop(
            columns=["DisplayScore"]
        ).to_html(index=False)

        st.markdown(
            f"""
            <div class="custom-table">
                {dataset_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("🎯 Average Stress Meter")

        avg_stress = filtered_data["StressScore"].mean()

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_stress,
            title={"text": "Average Stress Score"},
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#0F172A"
                },
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#10B981"
                    },
                    {
                        "range": [40, 70],
                        "color": "#FB923C"
                    },
                    {
                        "range": [70, 100],
                        "color": "#EF4444"
                    }
                ]
            }
        ))

        gauge.update_layout(
            paper_bgcolor="#F8FAFC",
            font={"color": "black"}
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        st.subheader("📊 Student Wellness Insights")

        chart1, chart2 = st.columns(2)

        with chart1:

            bar_chart = px.bar(
                filtered_data,
                x="Student",
                y="DisplayScore",
                text="StressScore",
                color="StressLevel",
                title="Student Stress Scores",
                color_discrete_map={
                    "Low": "#10B981",
                    "Medium": "#FB923C",
                    "High": "#EF4444"
                }
            )

            bar_chart.update_traces(
                textposition="outside"
            )

            bar_chart = style_graph(bar_chart)

            st.plotly_chart(
                bar_chart,
                use_container_width=True
            )

        with chart2:

            pie_chart = px.pie(
                filtered_data,
                names="StressLevel",
                title="Stress Level Distribution",
                color="StressLevel",
                color_discrete_map={
                    "Low": "#10B981",
                    "Medium": "#FB923C",
                    "High": "#EF4444"
                }
            )

            pie_chart.update_layout(
                paper_bgcolor="#F8FAFC",
                font=dict(color="black")
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        st.subheader("📈 Student Lifestyle Comparison")

        comparison_chart = px.line(
            filtered_data,
            x="Student",
            y=[
                "StudyHours",
                "SleepHours",
                "ScreenTime",
                "ExerciseHours"
            ],
            markers=True,
            title="Student Lifestyle Comparison"
        )

        comparison_chart = style_graph(comparison_chart)

        st.plotly_chart(
            comparison_chart,
            use_container_width=True
        )

        st.subheader("🚨 High Stress Alerts")

        high_stress = filtered_data[
            filtered_data["StressLevel"] == "High"
        ]

        if len(high_stress) > 0:

            st.error(
                f"{len(high_stress)} high stress students detected."
            )

            high_stress_html = high_stress.drop(
                columns=["DisplayScore"]
            ).to_html(index=False)

            st.markdown(
                f"""
                <div class="custom-table">
                    {high_stress_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.success("✅ No high stress students detected.")

        pdf_buffer = create_pdf_report(
            filtered_data,
            high_stress
        )

        st.download_button(
            label="📥 Download Complete Stress Analysed Report PDF",
            data=pdf_buffer,
            file_name="complete_stress_analysed_report.pdf",
            mime="application/pdf"
        )

else:

    st.info("📂 Upload a CSV file to start analysis.")