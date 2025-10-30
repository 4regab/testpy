"""
Academic Analytics Lite - Main Pipeline
Course: Data Structures and Algorithms (Python)
"""
import json
import time
from src.ingest import read_csv, sort_records, filter_records
from src.transform import add_computed_fields, compute_improvement
from src.analyze import (compute_stats, grade_distribution, identify_at_risk,
                         section_comparison, top_performers, find_outliers)
from src.reports import (print_summary, print_student_list, export_by_section,
                         export_at_risk_list, print_section_comparison)


def load_config(config_path: str = 'config.json') -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def main():
    """Main pipeline execution."""
    start_time = time.time()

    print("="*60)
    print("ACADEMIC ANALYTICS LITE")
    print("="*60)

    # Load configuration
    print("\n[1/6] Loading configuration...")
    config = load_config()
    if not config:
        print("Failed to load configuration. Exiting.")
        return

    weights = config['weights']
    thresholds = config['thresholds']
    paths = config['paths']
    grade_scale = config['grade_scale']

    # Ingest data
    print(f"\n[2/6] Reading data from {paths['input_folder']}/input.csv...")
    records, errors = read_csv(f"{paths['input_folder']}/input.csv")

    if errors:
        print(f"\nWarnings/Errors during ingestion:")
        for error in errors:
            print(f"  - {error}")

    print(f"Successfully loaded {len(records)} student records")

    # Transform data
    print("\n[3/6] Computing grades and transformations...")
    records = add_computed_fields(records, weights, grade_scale)

    # Add improvement metric
    for record in records:
        record['improvement'] = compute_improvement(record)

    # Analyze data
    print("\n[4/6] Performing analytics...")

    # Extract valid grades for statistics
    valid_grades = [r['final_grade']
                    for r in records if r['final_grade'] is not None]

    # Compute statistics
    stats = compute_stats(valid_grades)
    distribution = grade_distribution(records)

    # Identify at-risk students
    at_risk = identify_at_risk(records, thresholds['at_risk'])

    # Find outliers
    outliers = find_outliers(valid_grades)

    # Section comparison
    section_stats = section_comparison(records)

    # Top performers
    top_10 = top_performers(records, 10)

    # Generate reports
    print("\n[5/6] Generating reports...")

    # Print summary
    print_summary(records, stats, distribution)

    # Print section comparison
    print_section_comparison(section_stats)

    # Print at-risk students
    if at_risk:
        print_student_list(
            at_risk, f"At-Risk Students (Grade < {thresholds['at_risk']})")

    # Print top performers
    print_student_list(top_10[:5], "Top 5 Performers")

    # Print outliers
    if outliers:
        print(f"\n--- Grade Outliers (IQR Method) ---")
        print(
            f"Found {len(outliers)} outlier grades: {[round(o, 2) for o in outliers]}")

    # Export data
    print("\n[6/6] Exporting data...")

    # Export by section
    export_by_section(records, paths['output_folder'])

    # Export at-risk list
    if at_risk:
        export_at_risk_list(
            at_risk, f"{paths['output_folder']}/at_risk_students.csv")

    # Performance timing
    elapsed = time.time() - start_time
    print(f"\n✓ Pipeline completed in {elapsed:.2f} seconds")
    print("="*60)


if __name__ == "__main__":
    main()
