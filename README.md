
# Faculty Teaching Load Sanity Checker

This Streamlit application reorganizes section tally data to make **faculty teaching load** visible and reviewable by **instructor**, across programs.

It is designed for academic administration workflows where faculty often teach in more than one program and workload needs to be reviewed holistically rather than course-by-course.

---

## What this app does

The app takes a section tally Excel spreadsheet and produces a new spreadsheet that:

- Groups courses **by instructor first**
- Shows all programs taught by an instructor together
- Makes shared and cross-listed teaching explicit
- Reduces manual sorting, filtering, and duplication

The output is intended as a **sanity-check view**, not a replacement for institutional systems.

---

## Input

An Excel spreadsheet containing (at minimum) the following columns:

- Program  
- Event ID  
- Section  
- Semester  
- Course title  
- Course type  
- Instructor  
- Max Participants  
- Current Enrollment  
- Available Seats  
- Wait List  
- Meeting Day/Time  
- Course start date  
- Course end Date  

---

## How the data is reorganized

### Instructor-first organization

The output spreadsheet is organized by **instructor**, with each instructor appearing as an explicit header row.

All courses taught by that instructor are listed directly below, regardless of program.

### Sorting rules

Courses are sorted in this order:

1. Instructor (Last name, First name)  
2. Program  
3. Event ID  
4. Section ID  
5. Course title  

---

## Cross-listed and multi-instructor courses

- If a section ID starts with `CL` (for example: `CLA`, `CLB`), the course is treated as cross-listed and listed once per instructor.
- If a course has multiple instructors but the section does **not** start with `CL`:
  - The course is listed once per instructor
  - `CL*` is added to the section ID
  - The asterisk (`*`) indicates the cross-listing was inferred, not present in the original data

This ensures instructional responsibility is visible without altering the source spreadsheet.

---

## Output

The app generates a downloadable Excel file with:

- Explicit instructor header rows
- Program shown as a column (no program header rows)
- One row per instructor per course
- A filename that includes the semester and download date

---

## Part of Academic Admin Tools

This project is part of the **academic-admin-tools** organization, which focuses on building small, transparent systems to support recurring academic administrative work.
