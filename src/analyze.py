"""
Analytics module for Academic Analytics Lite.
Handles statistical analysis and insights.
"""
from typing import List, Dict, Optional, Tuple
import math


def compute_stats(values: List[float]) -> Dict:
    """
    Compute basic statistics for a list of values.

    Args:
        values: List of numeric values

    Returns:
        Dictionary with mean, median, std, min, max
    """
    if not values:
        return {
            'count': 0,
            'mean': None,
            'median': None,
            'std': None,
            'min': None,
            'max': None
        }

    n = len(values)
    sorted_values = sorted(values)

    # Mean
    mean = sum(values) / n

    # Median
    if n % 2 == 0:
        median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        median = sorted_values[n//2]

    # Standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance)

    return {
        'count': n,
        'mean': round(mean, 2),
        'median': round(median, 2),
        'std': round(std, 2),
        'min': round(min(values), 2),
        'max': round(max(values), 2)
    }


def compute_percentile(values: List[float], percentile: float) -> Optional[float]:
    """
    Compute percentile value.

    Args:
        values: List of numeric values
        percentile: Percentile to compute (0-100)

    Returns:
        Percentile value or None
    """
    if not values:
        return None

    sorted_values = sorted(values)
    n = len(sorted_values)

    # Linear interpolation method
    rank = (percentile / 100) * (n - 1)
    lower = int(rank)
    upper = min(lower + 1, n - 1)
    weight = rank - lower

    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def find_outliers(values: List[float], method: str = 'iqr') -> List[float]:
    """
    Find outliers using IQR method.

    Args:
        values: List of numeric values
        method: Method to use ('iqr' or 'zscore')

    Returns:
        List of outlier values
    """
    if not values or len(values) < 4:
        return []

    if method == 'iqr':
        q1 = compute_percentile(values, 25)
        q3 = compute_percentile(values, 75)

        if q1 is None or q3 is None:
            return []

        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        return [v for v in values if v < lower_bound or v > upper_bound]

    elif method == 'zscore':
        mean = sum(values) / len(values)
        std = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))

        if std == 0:
            return []

        return [v for v in values if abs((v - mean) / std) > 2]

    return []


def grade_distribution(records: List[Dict]) -> Dict[str, int]:
    """
    Compute grade distribution.

    Args:
        records: Array of student records with letter_grade field

    Returns:
        Dictionary mapping letter grades to counts
    """
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0, 'N/A': 0}

    for record in records:
        letter = record.get('letter_grade', 'N/A')
        if letter in distribution:
            distribution[letter] += 1
        else:
            distribution['N/A'] += 1

    return distribution


def identify_at_risk(records: List[Dict], threshold: float) -> List[Dict]:
    """
    Identify at-risk students.

    Args:
        records: Array of student records
        threshold: Grade threshold for at-risk

    Returns:
        Array of at-risk student records
    """
    at_risk = []

    for record in records:
        final_grade = record.get('final_grade')

        if final_grade is not None and final_grade < threshold:
            at_risk.append(record)

    return at_risk


def section_comparison(records: List[Dict]) -> Dict[str, Dict]:
    """
    Compare performance across sections.

    Args:
        records: Array of student records

    Returns:
        Dictionary mapping section to statistics
    """
    sections = {}

    # Group by section
    for record in records:
        section = record.get('section', 'Unknown')

        if section not in sections:
            sections[section] = []

        final_grade = record.get('final_grade')
        if final_grade is not None:
            sections[section].append(final_grade)

    # Compute stats for each section
    section_stats = {}
    for section, grades in sections.items():
        section_stats[section] = compute_stats(grades)

    return section_stats


def top_performers(records: List[Dict], n: int = 10) -> List[Dict]:
    """
    Get top N performing students.

    Args:
        records: Array of student records
        n: Number of top students to return

    Returns:
        Array of top student records
    """
    # Filter records with valid grades
    valid_records = [r for r in records if r.get('final_grade') is not None]

    # Sort by final grade descending
    sorted_records = sorted(
        valid_records, key=lambda x: x['final_grade'], reverse=True)

    return sorted_records[:n]
