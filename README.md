# Academic Analytics Lite

**Course:** Data Structures and Algorithms (Python)

A lightweight analytics tool for exploring course outcomes using array-based operations and modular Python design.

## Features

- **Clean Data Ingestion**: CSV parsing with validation and error handling
- **Array Operations**: Select, project, sort, insert, delete operations
- **Analytics**: Weighted grades, distributions, percentiles, outliers, improvements
- **Reports**: Console summaries, per-section CSVs, at-risk student lists
- **Configuration**: JSON-based weights, thresholds, and paths
- **Testing**: Unit tests with type hints
- **Web Interface**: Interactive Streamlit dashboard with matplotlib visualizations

## Project Structure

```
testpy/
├── src/
│   ├── ingest.py      # CSV reading and validation
│   ├── transform.py   # Grade calculations
│   ├── analyze.py     # Statistical analysis
│   └── reports.py     # Output generation
├── tests/
│   ├── test_transform.py
│   └── test_analyze.py
├── data/
│   └── input.csv      # Sample student data
├── output/            # Generated reports (created on run)
├── config.json        # Configuration file
├── main.py           # Main pipeline (CLI)
└── app.py            # Streamlit web app

```

## Usage

### Run the Streamlit Web App (Recommended):

```bash
streamlit run app.py
```

### Run the CLI pipeline:

```bash
python main.py
```

### Run tests:

```bash
python run_tests.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to adjust:
- Grade weights (quizzes, midterm, final, attendance)
- Thresholds (at-risk, excellent)
- Input/output paths
- Grade scale

## Data Format

CSV columns: `student_id`, `last_name`, `first_name`, `section`, `quiz1-5`, `midterm`, `final`, `attendance_percent`

## Output

- Console summary with statistics and distributions
- Section comparison report
- Per-section CSV exports
- At-risk student list
- Performance timing

## Design Principles

- Array-based operations (no pandas/numpy required)
- Modular, testable functions
- Clear error handling
- Type hints throughout
- Standard library only
