"""
Data transformation module for Academic Analytics Lite.
Handles grade calculations and transformations.
"""
from typing import Dict, List, Optional


def compute_quiz_average(record: Dict) -> Optional[float]:
    """
    Compute average of quiz scores, ignoring None values.

    Args:
        record: Student record

    Returns:
        Average quiz score or None if no valid quizzes
    """
    quiz_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5']
    quiz_scores = [record.get(field)
                   for field in quiz_fields if record.get(field) is not None]

    if not quiz_scores:
        return None

    return sum(quiz_scores) / len(quiz_scores)


def compute_final_grade(record: Dict, weights: Dict) -> Optional[float]:
    """
    Compute weighted final grade.

    Args:
        record: Student record
        weights: Dictionary with weight configuration

    Returns:
        Final grade or None if insufficient data
    """
    quiz_avg = compute_quiz_average(record)
    midterm = record.get('midterm')
    final = record.get('final')
    attendance = record.get('attendance_percent')

    # Need at least midterm and final
    if midterm is None or final is None:
        return None

    # Calculate weighted components
    grade = 0.0
    total_weight = 0.0

    if quiz_avg is not None:
        grade += quiz_avg * weights['quizzes']
        total_weight += weights['quizzes']

    grade += midterm * weights['midterm']
    total_weight += weights['midterm']

    grade += final * weights['final']
    total_weight += weights['final']

    if attendance is not None:
        grade += attendance * weights['attendance']
        total_weight += weights['attendance']

    # Normalize if missing components
    if total_weight > 0:
        return grade / total_weight * (weights['quizzes'] + weights['midterm'] +
                                       weights['final'] + weights['attendance'])

    return None


def letter_grade(numeric_grade: Optional[float], grade_scale: Dict) -> str:
    """
    Convert numeric grade to letter grade.

    Args:
        numeric_grade: Numeric grade value
        grade_scale: Dictionary mapping letters to minimum scores

    Returns:
        Letter grade
    """
    if numeric_grade is None:
        return 'N/A'

    # Sort grades by threshold descending
    sorted_grades = sorted(grade_scale.items(),
                           key=lambda x: x[1], reverse=True)

    for letter, threshold in sorted_grades:
        if numeric_grade >= threshold:
            return letter

    return 'F'


def add_computed_fields(records: List[Dict], weights: Dict, grade_scale: Dict) -> List[Dict]:
    """
    Add computed fields to all records.

    Args:
        records: Array of student records
        weights: Weight configuration
        grade_scale: Grade scale configuration

    Returns:
        Records with added computed fields
    """
    enhanced_records = []

    for record in records:
        enhanced = record.copy()

        # Add quiz average
        enhanced['quiz_average'] = compute_quiz_average(record)

        # Add final grade
        final_grade = compute_final_grade(record, weights)
        enhanced['final_grade'] = final_grade

        # Add letter grade
        enhanced['letter_grade'] = letter_grade(final_grade, grade_scale)

        enhanced_records.append(enhanced)

    return enhanced_records


def compute_improvement(record: Dict) -> Optional[float]:
    """
    Compute improvement from midterm to final.

    Args:
        record: Student record

    Returns:
        Improvement percentage or None
    """
    midterm = record.get('midterm')
    final = record.get('final')

    if midterm is None or final is None or midterm == 0:
        return None

    return ((final - midterm) / midterm) * 100
