

import streamlit as st
import pandas as pd
import sqlite3
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Admin Panel",
    page_icon="🔐",
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

.admin-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #CBD5E1;
    box-shadow: 0px 6px 18px rgba(15,23,42,0.12);
    min-height: 140px;
}

div.stButton > button {
    background-color: #0F172A !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect(
    "student_stress.db",
    check_same_thread=False
)

cursor = conn.cursor()

st.title("🔐 Admin Control Panel")

st.write("Manage student stress database securely.")

admin_password = st.text_input(
    "Enter Admin Password",
    type="password"
)

correct_password = "ranjani07"

if admin_password == correct_password:

    st.success("✅ Admin Access Granted")

    data = pd.read_sql(
        "SELECT * FROM stress_data",
        conn
    )

    if len(data) == 0:

        st.warning("⚠ No records found.")

    else:

        st.subheader("📄 Student Records")

        table_html = data.to_html(
            index=False,
            escape=False
        )

        components.html(
            f"""
            <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}

            th {{
                background-color: #E5E7EB;
                color: black;
                border: 1.5px solid black;
                padding: 10px;
                text-align: center;
                font-weight: bold;
            }}

            td {{
                border: 1.5px solid black;
                padding: 10px;
                text-align: center;
                color: black;
                background-color: white;
            }}
            </style>

            {table_html}
            """,
            height=300,
            scrolling=True
        )

        data["record_identity"] = (
            data["student_name"]
            + " | "
            + data["dob"]
            + " | "
            + data["analysis_date"]
        )

        st.subheader("🗑 Record Deletion Controls")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("""
            <div class="admin-card">
            <h3>Single Record</h3>
            <p>Delete one selected student record.</p>
            </div>
            """, unsafe_allow_html=True)

            single_record = st.selectbox(
                "Select Record",
                data["record_identity"]
            )

            if st.button("Delete Selected"):

                selected_row = data[
                    data["record_identity"] == single_record
                ].iloc[0]

                cursor.execute(
                    """
                    DELETE FROM stress_data
                    WHERE student_name = ?
                    AND dob = ?
                    AND analysis_date = ?
                    """,
                    (
                        selected_row["student_name"],
                        selected_row["dob"],
                        selected_row["analysis_date"]
                    )
                )

                conn.commit()

                st.success("✅ Selected record deleted.")

        with col2:

            st.markdown("""
            <div class="admin-card">
            <h3>Multiple Records</h3>
            <p>Delete multiple selected records.</p>
            </div>
            """, unsafe_allow_html=True)

            multiple_records = st.multiselect(
                "Select Records",
                data["record_identity"]
            )

            if st.button("Delete Multiple"):

                if len(multiple_records) == 0:

                    st.warning("⚠ Select at least one record.")

                else:

                    for record in multiple_records:

                        selected_row = data[
                            data["record_identity"] == record
                        ].iloc[0]

                        cursor.execute(
                            """
                            DELETE FROM stress_data
                            WHERE student_name = ?
                            AND dob = ?
                            AND analysis_date = ?
                            """,
                            (
                                selected_row["student_name"],
                                selected_row["dob"],
                                selected_row["analysis_date"]
                            )
                        )

                    conn.commit()

                    st.success("✅ Multiple records deleted.")

        with col3:

            st.markdown("""
            <div class="admin-card">
            <h3>Delete Entire Database</h3>
            <p>Remove all student records permanently.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚨 Delete All Records"):

                cursor.execute("DELETE FROM stress_data")

                conn.commit()

                st.success("✅ Entire database deleted.")

else:

    if admin_password == "":

        st.warning("🔒 Enter admin password to access admin panel.")

    else:

        st.error("❌ Wrong password. Please try again.")