# Student Study Analyzer

A Python-based data analysis tool that processes student study data from Excel files and generates insights on performance, study habits, and time distribution.

This project was developed as part of a programming course group assignment.

---

## Features

- Load study data from an Excel file (~50 students, ~3000 sessions)
- Identify top students based on total study hours
- Analyze study time per subject
- Show monthly study trends
- Generate detailed statistics for individual students

---

## Technologies

- Python
- pandas
- openpyxl
- pytest

---

## Installation

Make sure you have Python 3.10 or newer.

```bash
git clone https://github.com/ngimenoieu2025-lang/student_study_analizer.git
cd student_study_analyzer
python -m pip install -r requirements.txt
```

---

## How to run

```bash
python -m src.main
```

Run the command from the project root directory.

---

## Running tests

```bash
python -m pytest
```

---

## Project structure

```
student_study_analyzer/
├── data/
│   └── student_study_tracker.xlsx
├── src/
│   ├── main.py
│   ├── core/
│   │   ├── analyzer.py
│   │   ├── data_loader.py
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   └── test_analyzer.py
├── requirements.txt
└── README.md
```

---

## Testing

The project includes unit tests implemented with pytest and is integrated with GitHub Actions for continuous testing.

---

## Notes

The project follows a modular design, separating data loading, analysis, and execution logic to improve readability and maintainability.