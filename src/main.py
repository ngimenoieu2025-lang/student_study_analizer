# main.py
# Entry point of the application
# Run with: python main.py

from .core.analyzer import StudyAnalyzer
# Path to the dataset (relative to project root)
DATA_PATH = "data/student_study_tracker.xlsx"


# Helper function to print rows of a DataFrame using a custom format
def print_rows(df, formatter):
    for i, row in df.iterrows():
        print(formatter(i, row))


def main():
    # Start of program
    print("Loading data...")

    # Try to initialize the analyzer (loads and processes data)
    try:
        analyzer = StudyAnalyzer(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: could not find the file at {DATA_PATH}")
        print("Make sure you are running this from the project root folder.")
        return

    # Display general class statistics
    print("\n--- CLASS SUMMARY ---")
    analyzer.class_summary()

    # Show top students by total study hours
    print("\n--- TOP 5 STUDENTS ---")
    top5 = analyzer.get_top_students(n=5)
    print_rows(
    top5,
    lambda i, r: f"  {i+1}. {r['Student Name']} - {r['Total Hours']:.1f} hrs"
)

    # Show total study hours per subject
    print("\n--- HOURS PER SUBJECT ---")
    subjects = analyzer.get_subject_totals()
    print_rows(
        subjects,
        lambda _, r: f"  {r['Subject']:<22} {r['Total Hours']:.1f} hrs"
    )

    # Show monthly evolution of study hours
    print("\n--- MONTHLY BREAKDOWN ---")
    monthly = analyzer.get_monthly_hours()
    print_rows(
        monthly,
        lambda _, r: f"  {r['Month']}   {round(r['Total Hours'], 1)} hrs"
    )

    # Example: detailed statistics for a specific student
    print("\n--- EXAMPLE: STUDENT REPORT ---")
    student_name = "Alex Adams"
    stats = analyzer.get_student_stats(student_name)

    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nDone!")


# Standard Python entry point
if __name__ == "__main__":
    main()