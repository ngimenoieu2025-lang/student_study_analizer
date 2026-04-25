# tests/test_analyzer.py
# Unit tests for StudyAnalyzer
# Run with: pytest

import pytest
import pandas as pd

from src.core.analyzer import StudyAnalyzer, SUBJECTS
# Path to dataset
DATA_PATH = "data/student_study_tracker.xlsx"


class TestStudyAnalyzer:

    def setup_method(self):
        # Create analyzer before each test
        self.analyzer = StudyAnalyzer(DATA_PATH)

    # --- basic loading tests ---

    def test_dataframes_not_empty(self):
        assert not self.analyzer.log_df.empty
        assert not self.analyzer.summary_df.empty

    def test_student_names_exist(self):
        assert "Student Name" in self.analyzer.summary_df.columns

    # --- top students ---

    def test_top_students_length(self):
        top = self.analyzer.get_top_students(n=5)
        assert len(top) == 5

    def test_top_students_sorted(self):
        top = self.analyzer.get_top_students(n=10)
        hours = top["Total Hours"].values

        # Check descending order
        assert all(hours[i] >= hours[i+1] for i in range(len(hours)-1))

    # --- subjects ---

    def test_subject_totals_contains_all_subjects(self):
        totals = self.analyzer.get_subject_totals()
        subjects = totals["Subject"].values

        for subj in SUBJECTS:
            assert subj in subjects

    # --- monthly data ---

    def test_monthly_hours_not_empty(self):
        monthly = self.analyzer.get_monthly_hours()
        assert len(monthly) > 0

    # --- student stats ---

    def test_student_stats_structure(self):
        stats = self.analyzer.get_student_stats("Alex Adams")

        assert isinstance(stats, dict)
        assert "total_hours" in stats
        assert "best_subject" in stats
        assert "worst_subject" in stats

    def test_invalid_student_raises(self):
        with pytest.raises(ValueError):
            self.analyzer.get_student_stats("Fake Person")

    # --- weakest subject ---

    def test_weakest_subject_shape(self):
        weak = self.analyzer.get_weakest_subject()

        # Should have one row per student
        num_students = self.analyzer.summary_df["Student Name"].nunique()
        assert len(weak) == num_students