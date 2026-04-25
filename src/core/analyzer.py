# analyzer.py
# Main analysis class for the project
# Groups all data processing and statistics in one place

import pandas as pd
from .data_loader import load_log, load_summary
SUBJECTS = ["Math", "Science", "English", "History", "Computer Science", "Biology", "Economics"]


class StudyAnalyzer:
    # Initialize analyzer and load data
    def __init__(self, filepath):
        self.filepath = filepath
        self.log_df = load_log(filepath)
        self.summary_df = load_summary(filepath)

    # Return top n students sorted by total study hours
    def get_top_students(self, n=5):
        top = self.summary_df[["Student Name", "Total Hours"]].copy()
        top["Total Hours"] = pd.to_numeric(top["Total Hours"], errors="coerce")

        top = top.sort_values("Total Hours", ascending=False).head(n)
        return top.reset_index(drop=True)

    # Compute total study hours per subject across all students
    def get_subject_totals(self):
        totals = self.summary_df[SUBJECTS].apply(pd.to_numeric, errors="coerce").sum()

        result = pd.DataFrame({
            "Subject": totals.index,
            "Total Hours": totals.values
        })

        return result.sort_values("Total Hours", ascending=False).reset_index(drop=True)

    # Find weakest subject (least hours) for each student
    def get_weakest_subject(self):
        numeric = self.summary_df[SUBJECTS].apply(pd.to_numeric, errors="coerce")
        weakest = numeric.idxmin(axis=1)

        result = pd.DataFrame({
            "Student Name": self.summary_df["Student Name"],
            "Weakest Subject": weakest
        })

        return result.reset_index(drop=True)

    # Compute total study hours per month
    def get_monthly_hours(self):
        df = self.log_df.copy()

        # Extract month from date column
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        monthly = df.groupby("Month")["Hours Studied"].sum().reset_index()
        monthly.columns = ["Month", "Total Hours"]

        return monthly

    # Get detailed statistics for a specific student
    def get_student_stats(self, name):
        # Check if student exists
        if name not in self.summary_df["Student Name"].values:
            raise ValueError(f"Student '{name}' not found in the data.")

        row = self.summary_df[self.summary_df["Student Name"] == name].iloc[0]
        student_log = self.log_df[self.log_df["Student Name"] == name]

        hours = pd.to_numeric(row[SUBJECTS], errors="coerce")

        stats = {
            "name": name,
            "total_hours": round(float(pd.to_numeric(row["Total Hours"], errors="coerce")), 1),
            "num_sessions": len(student_log),
            "avg_session": round(float(student_log["Hours Studied"].mean()), 2),
            "best_subject": hours.idxmax(),
            "worst_subject": hours.idxmin(),
        }

        return stats

    # Print a quick summary of the dataset
    def class_summary(self):
        total_hours = self.log_df["Hours Studied"].sum()
        num_students = self.summary_df["Student Name"].nunique()
        num_sessions = len(self.log_df)
        best_subject = self.get_subject_totals().iloc[0]["Subject"]

        print(f"Total students:   {num_students}")
        print(f"Total sessions:   {num_sessions}")
        print(f"Total hours:      {round(total_hours, 1)}")
        print(f"Most studied:     {best_subject}")