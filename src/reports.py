"""
Reporting module for Academic Analytics Lite.
Handles output generation and exports.
"""
from typing import List, Dict
import csv
import os


def print_summary(records: List[Dict], stats: Dict, distribution: Dict) -> None:
    """
    Print summary report to console.

    Args:
        records: Array of student records
        stats: Statistics dictionary
        distribution: Grade distribution dictionary
    """
    print("\n" + "="*60)
    print("ACADEMIC ANALYTICS LITE - SUMMARY REPORT")
    print("="*60)

    print(f"\nTotal Students: {len(records)}")

    print("\n--- Overall Statistics ---")
    if stats['mean'] is not None:
        print(f"Mean Grade: {stats['mean']:.2f}")
        print(f"Median Grade: {stats['median']:.2f}")
        print(f"Std Deviation: {stats['std']:.2f}")
        print(f"Min Grade: {stats['min']:.2f}")
        print(f"Max Grade: {stats['max']:.2f}")
    else:
        print("No valid grades to compute statistics")

    print("\n--- Grade Distribution ---")
    for letter, count in sorted(distribution.items()):
        if letter != 'N/A' or count > 0:
            percentage = (count / len(records) *
                          100) if len(records) > 0 else 0
            print(f"{letter}: {count} ({percentage:.1f}%)")

    print("\n" + "="*60 + "\n")


def print_student_list(records: List[Dict], title: str = "Student List") -> None:
    """
    Print formatted student list.

    Args:
        records: Array of student records
        title: Title for the list
    """
    print(f"\n--- {title} ---")
    print(f"{'ID':<10} {'Name':<25} {'Section':<10} {'Final Grade':<12} {'Letter':<8}")
    print("-" * 75)

    for record in records:
        student_id = record.get('student_id', 'N/A')
        name = f"{record.get('first_name', '')} {record.get('last_name', '')}".strip(
        )
        section = record.get('section', 'N/A')
        final_grade = record.get('final_grade')
        letter = record.get('letter_grade', 'N/A')

        grade_str = f"{final_grade:.2f}" if final_grade is not None else "N/A"

        print(f"{student_id:<10} {name:<25} {section:<10} {grade_str:<12} {letter:<8}")

    print()


def export_to_csv(records: List[Dict], filepath: str, fields: List[str] = None) -> bool:
    """
    Export records to CSV file.

    Args:
        records: Array of student records
        filepath: Output file path
        fields: List of fields to export (None = all)

    Returns:
        True if successful, False otherwise
    """
    if not records:
        print(f"No records to export to {filepath}")
        return False

    try:
        # Create directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Determine fields
        if fields is None:
            fields = list(records[0].keys())

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(
                file, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(records)

        print(f"Exported {len(records)} records to {filepath}")
        return True

    except Exception as e:
        print(f"Error exporting to {filepath}: {str(e)}")
        return False


def export_by_section(records: List[Dict], output_folder: str) -> None:
    """
    Export separate CSV files for each section.

    Args:
        records: Array of student records
        output_folder: Output folder path
    """
    # Group by section
    sections = {}
    for record in records:
        section = record.get('section', 'Unknown')
        if section not in sections:
            sections[section] = []
        sections[section].append(record)

    # Export each section
    for section, section_records in sections.items():
        filename = f"section_{section}.csv"
        filepath = os.path.join(output_folder, filename)
        export_to_csv(section_records, filepath)


def export_at_risk_list(records: List[Dict], filepath: str) -> bool:
    """
    Export at-risk students to CSV.

    Args:
        records: Array of at-risk student records
        filepath: Output file path

    Returns:
        True if successful, False otherwise
    """
    fields = ['student_id', 'last_name', 'first_name', 'section',
              'final_grade', 'letter_grade', 'attendance_percent']

    return export_to_csv(records, filepath, fields)


def print_section_comparison(section_stats: Dict[str, Dict]) -> None:
    """
    Print section comparison report.

    Args:
        section_stats: Dictionary mapping section to statistics
    """
    print("\n--- Section Comparison ---")
    print(f"{'Section':<10} {'Count':<8} {'Mean':<8} {'Median':<8} {'Std':<8}")
    print("-" * 50)

    for section, stats in sorted(section_stats.items()):
        count = stats['count']
        mean = f"{stats['mean']:.2f}" if stats['mean'] is not None else "N/A"
        median = f"{stats['median']:.2f}" if stats['median'] is not None else "N/A"
        std = f"{stats['std']:.2f}" if stats['std'] is not None else "N/A"

        print(f"{section:<10} {count:<8} {mean:<8} {median:<8} {std:<8}")

    print()
