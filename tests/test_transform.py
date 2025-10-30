"""
Unit tests for transform module.
"""
from src.transform import (compute_quiz_average, compute_final_grade,
                           letter_grade, compute_improvement)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_compute_quiz_average():
    """Test quiz average calculation."""
    # All quizzes present
    record = {'quiz1': 80, 'quiz2': 85, 'quiz3': 90, 'quiz4': 85, 'quiz5': 80}
    assert compute_quiz_average(record) == 84.0

    # Some quizzes missing
    record = {'quiz1': 80, 'quiz2': None,
              'quiz3': 90, 'quiz4': None, 'quiz5': 80}
    assert compute_quiz_average(record) == 83.33333333333333

    # All quizzes missing
    record = {'quiz1': None, 'quiz2': None,
              'quiz3': None, 'quiz4': None, 'quiz5': None}
    assert compute_quiz_average(record) is None

    print("✓ test_compute_quiz_average passed")


def test_compute_final_grade():
    """Test final grade calculation."""
    weights = {
        'quizzes': 0.20,
        'midterm': 0.30,
        'final': 0.40,
        'attendance': 0.10
    }

    # Complete record
    record = {
        'quiz1': 80, 'quiz2': 85, 'quiz3': 90, 'quiz4': 85, 'quiz5': 80,
        'midterm': 85,
        'final': 88,
        'attendance_percent': 95
    }
    final = compute_final_grade(record, weights)
    assert final is not None
    assert 85 < final < 90

    # Missing midterm
    record = {'quiz1': 80, 'midterm': None,
              'final': 88, 'attendance_percent': 95}
    assert compute_final_grade(record, weights) is None

    print("✓ test_compute_final_grade passed")


def test_letter_grade():
    """Test letter grade conversion."""
    grade_scale = {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 0}

    assert letter_grade(95, grade_scale) == 'A'
    assert letter_grade(85, grade_scale) == 'B'
    assert letter_grade(75, grade_scale) == 'C'
    assert letter_grade(65, grade_scale) == 'D'
    assert letter_grade(55, grade_scale) == 'F'
    assert letter_grade(None, grade_scale) == 'N/A'

    print("✓ test_letter_grade passed")


def test_compute_improvement():
    """Test improvement calculation."""
    # Positive improvement
    record = {'midterm': 70, 'final': 84}
    improvement = compute_improvement(record)
    assert improvement == 20.0

    # Negative improvement
    record = {'midterm': 90, 'final': 81}
    improvement = compute_improvement(record)
    assert improvement == -10.0

    # Missing data
    record = {'midterm': None, 'final': 84}
    assert compute_improvement(record) is None

    print("✓ test_compute_improvement passed")


if __name__ == "__main__":
    test_compute_quiz_average()
    test_compute_final_grade()
    test_letter_grade()
    test_compute_improvement()
    print("\n✓ All transform tests passed!")
