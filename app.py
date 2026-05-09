
rt streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Faculty Teaching Load Sanity Checker")

st.title("Faculty Teaching Load Sanity Checker")

st.write(
    "Upload a section tally spreadsheet to reorganize teaching load "
    "by instructor, with clear visibility across programs."
)

uploaded_file = st.file_uploader(
    "Upload section tally Excel file",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # -------------------------------
    # Required columns
    # -------------------------------
    required_columns = [
        "Program",
        "Event ID",
        "Section",
        "Semester",
        "Course title",
        "Course type",
        "Instructor",
        "Max Participants",
        "Current Enrollment",
        "Available Seats",
        "Wait List",
        "Meeting Day/Time",
        "course start date",
        "course end Date",
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    expanded_rows = []

    # -------------------------------
    # Expand multi-instructor courses
    # -------------------------------
    for _, row in df.iterrows():
        instructors = (
            str(row["Instructor"])
            .replace("-", ",")
            .split(",")
        )
        instructors = [i.strip() for i in instructors if i.strip()]

        for instructor in instructors:
            new_row = row.copy()
            new_row["Instructor"] = instructor

            section = str(row["Section"])
            if len(instructors) > 1 and not section.startswith("CL"):
                new_row["Section"] = f"CL{section}*"

            expanded_rows.append(new_row)

    out_df = pd.DataFrame(expanded_rows)

    # -------------------------------
    # Sort rows (final agreed order)
    # -------------------------------
    out_df = out_df.sort_values(
        by=[
            "Instructor",
            "Program",
            "Event ID",
            "Section",
            "Course title",
        ]
    )

    # -------------------------------
    # Insert instructor header rows
    # -------------------------------
    final_rows = []
    current_instructor = None

    for _, row in out_df.iterrows():
        if row["Instructor"] != current_instructor:
            header_row = {col: "" for col in out_df.columns}
            header_row["Instructor"] = f"INSTRUCTOR: {row['Instructor']}"
            final_rows.append(header_row)
            current_instructor = row["Instructor"]

        final_rows.append(row.to_dict())

    final_df = pd.DataFrame(final_rows)

    # -------------------------------
    # File naming
    # -------------------------------
    semester = str(out_df["Semester"].iloc[0])
    download_date = datetime.now().strftime("%B %Y")

    filename = (
        f"Faculty Load Section Tally {semester} "
        f"downloaded {download_date}.xlsx"
    )

    st.success("Your teaching load spreadsheet is ready.")

    st.download_button(
        label="Download Excel file",
        data=final_df.to_excel(index=False),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
