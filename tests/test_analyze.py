"""
Unit tests for analyze module.
"""
from src.analyze import (compute_stats, compute_percentile, find_outliers,
                         grade_distribution, identify_at_risk)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_compute_stats():
    """Test statistics computation."""
    values = [70, 75, 80, 85, 90, 95, 100]
    stats = compute_stats(values)

    assert stats['count'] == 7
    assert stats['mean'] == 85.0
    assert stats['median'] == 85.0
    assert stats['min'] == 70.0
    assert stats['max'] == 100.0

    # Empty list
    stats = compute_stats([])
    assert stats['mean'] is None

    print("✓ test_compute_stats passed")


def test_compute_percentile():
    """Test percentile calculation."""
    values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    p25 = compute_percentile(values, 25)
    assert 25 <= p25 <= 35

    p50 = compute_percentile(values, 50)
    assert 50 <= p50 <= 60

    p75 = compute_percentile(values, 75)
    assert 70 <= p75 <= 80

    # Empty list
    assert compute_percentile([], 50) is None

    print("✓ test_compute_percentile passed")


def test_find_outliers():
    """Test outlier detection."""
    # Normal distribution with outliers
    values = [50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 95, 10]
    outliers = find_outliers(values, method='iqr')

    assert len(outliers) > 0
    assert 95 in outliers or 10 in outliers

    # No outliers
    values = [50, 52, 54, 56, 58, 60, 62, 64, 66, 68]
    outliers = find_outliers(values, method='iqr')
    assert len(outliers) == 0

    print("✓ test_find_outliers passed")


def test_grade_distribution():
    """Test grade distribution."""
    records = [
        {'letter_grade': 'A'},
        {'letter_grade': 'A'},
        {'letter_grade': 'B'},
        {'letter_grade': 'C'},
        {'letter_grade': 'F'},
    ]

    dist = grade_distribution(records)
    assert dist['A'] == 2
    assert dist['B'] == 1
    assert dist['C'] == 1
    assert dist['D'] == 0
    assert dist['F'] == 1

    print("✓ test_grade_distribution passed")


def test_identify_at_risk():
    """Test at-risk identification."""
    records = [
        {'student_id': '1', 'final_grade': 55},
        {'student_id': '2', 'final_grade': 75},
        {'student_id': '3', 'final_grade': 58},
        {'student_id': '4', 'final_grade': 85},
    ]

    at_risk = identify_at_risk(records, threshold=60)
    assert len(at_risk) == 2
    assert at_risk[0]['student_id'] == '1'
    assert at_risk[1]['student_id'] == '3'

    print("✓ test_identify_at_risk passed")


if __name__ == "__main__":
    test_compute_stats()
    test_compute_percentile()
    test_find_outliers()
    test_grade_distribution()
    test_identify_at_risk()
    print("\n✓ All analyze tests passed!")
