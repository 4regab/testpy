"""
Data ingestion module for Academic Analytics Lite.
Handles CSV reading, validation, and cleaning.
"""
from typing import List, Dict, Optional, Tuple
import csv


def read_csv(filepath: str) -> Tuple[List[Dict], List[str]]:
    """
    Read CSV file and return array of student records.

    Args:
        filepath: Path to CSV file

    Returns:
        Tuple of (valid_records, error_messages)
    """
    records = []
    errors = []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=2):
                record, error = validate_row(row, row_num)

                if error:
                    errors.append(error)

                if record:
                    records.append(record)

    except FileNotFoundError:
        errors.append(f"File not found: {filepath}")
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return records, errors


def validate_row(row: Dict, row_num: int) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Validate and clean a single row of data.

    Args:
        row: Dictionary from CSV reader
        row_num: Row number for error reporting

    Returns:
        Tuple of (cleaned_record, error_message)
    """
    try:
        # Required fields
        student_id = row.get('student_id', '').strip()
        if not student_id:
            return None, f"Row {row_num}: Missing student_id"

        # Clean string fields
        record = {
            'student_id': student_id,
            'last_name': row.get('last_name', '').strip(),
            'first_name': row.get('first_name', '').strip(),
            'section': row.get('section', '').strip()
        }

        # Parse numeric fields with validation
        numeric_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5',
                          'midterm', 'final', 'attendance_percent']

        for field in numeric_fields:
            value = row.get(field, '').strip()

            if value == '':
                record[field] = None
            else:
                try:
                    num_value = float(value)

                    # Validate score range
                    if 0 <= num_value <= 100:
                        record[field] = num_value
                    else:
                        record[field] = None
                        return record, f"Row {row_num}: {field} out of range (0-100): {num_value}"

                except ValueError:
                    record[field] = None
                    return record, f"Row {row_num}: Invalid {field} value: {value}"

        return record, None

    except Exception as e:
        return None, f"Row {row_num}: Validation error: {str(e)}"


def filter_records(records: List[Dict], condition_func) -> List[Dict]:
    """
    Filter records based on a condition function.

    Args:
        records: Array of student records
        condition_func: Function that returns True for records to keep

    Returns:
        Filtered array of records
    """
    return [record for record in records if condition_func(record)]


def project_fields(records: List[Dict], fields: List[str]) -> List[Dict]:
    """
    Project (select) specific fields from records.

    Args:
        records: Array of student records
        fields: List of field names to keep

    Returns:
        Array of records with only specified fields
    """
    return [{field: record.get(field) for field in fields} for record in records]


def sort_records(records: List[Dict], key_field: str, reverse: bool = False) -> List[Dict]:
    """
    Sort records by a specific field.

    Args:
        records: Array of student records
        key_field: Field name to sort by
        reverse: Sort in descending order if True

    Returns:
        Sorted array of records
    """
    return sorted(records, key=lambda x: x.get(key_field, 0), reverse=reverse)


def insert_record(records: List[Dict], record: Dict, position: Optional[int] = None) -> List[Dict]:
    """
    Insert a record into the array.

    Args:
        records: Array of student records
        record: Record to insert
        position: Position to insert at (None = append)

    Returns:
        New array with record inserted
    """
    new_records = records.copy()

    if position is None:
        new_records.append(record)
    else:
        new_records.insert(position, record)

    return new_records


def delete_record(records: List[Dict], student_id: str) -> List[Dict]:
    """
    Delete a record by student_id.

    Args:
        records: Array of student records
        student_id: ID of student to remove

    Returns:
        New array with record removed
    """
    return [record for record in records if record.get('student_id') != student_id]
