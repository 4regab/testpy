"""
Test runner for Academic Analytics Lite
"""
from tests import test_transform, test_analyze
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules

print("="*60)
print("RUNNING UNIT TESTS")
print("="*60)

print("\n--- Transform Module Tests ---")
try:
    test_transform.test_compute_quiz_average()
    test_transform.test_compute_final_grade()
    test_transform.test_letter_grade()
    test_transform.test_compute_improvement()
    print("✓ All transform tests passed!")
except Exception as e:
    print(f"✗ Transform tests failed: {e}")

print("\n--- Analyze Module Tests ---")
try:
    test_analyze.test_compute_stats()
    test_analyze.test_compute_percentile()
    test_analyze.test_find_outliers()
    test_analyze.test_grade_distribution()
    test_analyze.test_identify_at_risk()
    print("✓ All analyze tests passed!")
except Exception as e:
    print(f"✗ Analyze tests failed: {e}")

print("\n" + "="*60)
print("TEST SUITE COMPLETE")
print("="*60)
