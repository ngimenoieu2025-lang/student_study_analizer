# data_loader.py
# Handles loading and basic preprocessing of the Excel data

import pandas as pd


def load_log(filepath):
    # Load study log sheet (skip first row due to formatting issues)
    df = pd.read_excel(filepath, sheet_name="Study Log", header=1, skiprows=[0])

    # Rename columns to something consistent
    expected_cols = ["Date", "Student ID", "Student Name", "Subject", "Hours Studied"]
    if len(df.columns) != len(expected_cols):
        raise ValueError("Unexpected format in 'Study Log' sheet")

    df.columns = expected_cols

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Convert date column safely
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert hours to numeric (invalid values become NaN)
    df["Hours Studied"] = pd.to_numeric(df["Hours Studied"], errors="coerce")

    return df


def load_summary(filepath):
    # Load summary sheet
    df = pd.read_excel(filepath, sheet_name="Student Subject Hours", header=1, skiprows=[0])

    # Expected column structure
    expected_cols = [
        "Student ID", "Student Name",
        "Math", "Science", "English", "History",
        "Computer Science", "Biology", "Economics",
        "Total Hours", "Avg Hours",
        "blank", "KPI Label", "KPI Value"
    ]

    if len(df.columns) != len(expected_cols):
        raise ValueError("Unexpected format in 'Student Subject Hours' sheet")

    df.columns = expected_cols

    # Keep only valid student rows (IDs start with 'S')
    df = df[df["Student ID"].astype(str).str.startswith("S")]

    # Reset index after filtering
    df = df.reset_index(drop=True)

    return df