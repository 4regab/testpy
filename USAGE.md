# Academic Analytics Lite - Usage Guide

## Quick Start

### Run the main pipeline:
```bash
cd testpy
python main.py
```

### Run all tests:
```bash
python run_tests.py
```

### Run individual test modules:
```bash
python tests/test_transform.py
python tests/test_analyze.py
```

## What It Does

The pipeline processes student data through 6 stages:

1. **Load Configuration** - Reads weights, thresholds, and paths from `config.json`
2. **Ingest Data** - Reads and validates `data/input.csv`
3. **Transform Data** - Computes weighted grades and letter grades
4. **Analyze Data** - Calculates statistics, distributions, outliers
5. **Generate Reports** - Prints summaries to console
6. **Export Data** - Creates CSV files in `output/` folder

## Output Files

After running `main.py`, you'll find:

- `output/section_A.csv` - All students in section A
- `output/section_B.csv` - All students in section B  
- `output/section_C.csv` - All students in section C
- `output/at_risk_students.csv` - Students below threshold

## Customization

Edit `config.json` to change:

```json
{
  "weights": {
    "quizzes": 0.20,    // Quiz average weight
    "midterm": 0.30,    // Midterm exam weight
    "final": 0.40,      // Final exam weight
    "attendance": 0.10  // Attendance weight
  },
  "thresholds": {
    "at_risk": 60.0,    // Grade threshold for at-risk
    "excellent": 90.0   // Grade threshold for excellent
  },
  "grade_scale": {
    "A": 90,
    "B": 80,
    "C": 70,
    "D": 60,
    "F": 0
  }
}
```

## Adding New Data

Replace `data/input.csv` with your own CSV file. Required columns:

- `student_id` - Unique identifier (required)
- `last_name`, `first_name` - Student names
- `section` - Section identifier (A, B, C, etc.)
- `quiz1` through `quiz5` - Quiz scores (0-100, can be empty)
- `midterm` - Midterm exam score (0-100, required)
- `final` - Final exam score (0-100, required)
- `attendance_percent` - Attendance percentage (0-100)

## Module Functions

### ingest.py
- `read_csv()` - Read and validate CSV
- `filter_records()` - Filter by condition
- `sort_records()` - Sort by field
- `insert_record()` - Add new record
- `delete_record()` - Remove record

### transform.py
- `compute_quiz_average()` - Average quiz scores
- `compute_final_grade()` - Weighted final grade
- `letter_grade()` - Convert to letter grade
- `compute_improvement()` - Midterm to final improvement

### analyze.py
- `compute_stats()` - Mean, median, std, min, max
- `compute_percentile()` - Calculate percentiles
- `find_outliers()` - Detect outliers (IQR method)
- `grade_distribution()` - Count by letter grade
- `identify_at_risk()` - Find struggling students
- `section_comparison()` - Compare sections
- `top_performers()` - Get top N students

### reports.py
- `print_summary()` - Console summary report
- `print_student_list()` - Formatted student table
- `export_to_csv()` - Export records to CSV
- `export_by_section()` - Create per-section CSVs
- `export_at_risk_list()` - Export at-risk students
- `print_section_comparison()` - Section stats table

## Design Principles

- **Array-based**: Uses Python lists and dictionaries (no pandas/numpy)
- **Modular**: Each module has a single responsibility
- **Testable**: Unit tests for core functions
- **Type hints**: Clear function signatures
- **Error handling**: Validates data and reports issues
- **Standard library only**: No external dependencies

## Performance

The pipeline processes 15 student records in ~0.02 seconds. Performance scales linearly with record count.

## Troubleshooting

**Missing data**: Missing quiz scores are ignored in average calculation. Missing midterm or final results in no final grade.

**Invalid scores**: Scores outside 0-100 range are set to None and reported as warnings.

**File not found**: Ensure `data/input.csv` exists and `config.json` is in the project root.
