# Quick Start Guide - Academic Analytics Lite

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Web App

**Start the Streamlit application:**
```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**

## Features Overview

### 📋 Tab 1: Data View
- **Upload CSV** or use sample data
- **Sort** by any column (ID, name, grade, section)
- **View** all student records in a clean table
- Real-time data validation warnings

### 📊 Tab 2: Analytics
- **Statistics Dashboard**: Mean, median, std dev, min, max
- **Visualizations**:
  - Grade distribution bar chart
  - Score histogram
  - Section comparison chart
  - Box plot analysis
- **Percentile Analysis**: 25th, 50th, 75th, 90th percentiles
- **Outlier Detection**: Automatic IQR-based outlier identification
- **At-Risk Students**: Configurable threshold alerts
- **Top Performers**: Top 10 students leaderboard

### 🔧 Tab 3: Operations
- **Filter Records**: By section
- **Delete Records**: Remove students from dataset
- **Project Fields**: Select specific columns to display
- Real-time array operations

### 📥 Tab 4: Reports
- **Export All Records**: Download complete dataset as CSV
- **Export At-Risk List**: Download struggling students
- **Export by Section**: Individual CSV files per section
- One-click downloads for all reports

## Sidebar Configuration

### Grade Weights (Adjustable)
- Quizzes: 0-100% (default 20%)
- Midterm: 0-100% (default 30%)
- Final: 0-100% (default 40%)
- Attendance: 0-100% (default 10%)

**Note**: Weights should sum to 1.0 (100%)

### Thresholds
- At-Risk Threshold: Minimum passing grade (default 60)

## CSV File Format

Your CSV must include these columns:

```csv
student_id,last_name,first_name,section,quiz1,quiz2,quiz3,quiz4,quiz5,midterm,final,attendance_percent
1001,Smith,John,A,85,90,88,92,87,85,88,95
```

**Required columns:**
- `student_id` - Unique identifier
- `last_name`, `first_name` - Student names
- `section` - Section identifier (A, B, C, etc.)
- `midterm` - Midterm exam score (0-100)
- `final` - Final exam score (0-100)

**Optional columns:**
- `quiz1` through `quiz5` - Quiz scores (can be empty)
- `attendance_percent` - Attendance percentage

## Sample Data

The app includes sample data at `data/input.csv` with 15 students across 3 sections.

Check the "Use sample data" checkbox to load it instantly.

## Tips

1. **Adjust weights** in the sidebar to see how different grading schemes affect outcomes
2. **Upload your own CSV** to analyze your class data
3. **Filter by section** to compare performance across different groups
4. **Download reports** for record-keeping or further analysis
5. **Use the box plot** to identify grade distribution patterns

## Troubleshooting

**App won't start?**
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check that you're in the `testpy` directory

**CSV upload fails?**
- Verify your CSV has all required columns
- Check that scores are between 0-100
- Ensure student_id values are unique

**Weights don't sum to 1.0?**
- Adjust the sliders so the total equals 100%
- The app will show a warning if weights are incorrect

## Command Line Alternative

If you prefer CLI, run the original pipeline:
```bash
python main.py
```

This generates console reports and CSV exports in the `output/` folder.

## Testing

Run unit tests to verify functionality:
```bash
python run_tests.py
```

## Support

For issues or questions, check:
- `README.md` - Full project documentation
- `USAGE.md` - Detailed module documentation
- Sample data in `data/input.csv`
