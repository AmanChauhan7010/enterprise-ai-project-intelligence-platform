"""
Unit Tests for Project Health Calculation Engine.
"""
import pytest
from utils.health_scorer import compute_project_health, categorize_health


def test_nominal_completed_project():
    record = {
        "Status": "Completed",
        "Progress": 100.0,
        "Remaining_Days": 0,
        "Budget": 100000,
        "Actual_Cost": 98000,
        "Open_Bugs": 0,
        "Sprint_Velocity": 45.0,
        "Team_Utilization": 82.0
    }
    score = compute_project_health(record)
    assert 90 <= score <= 100
    assert categorize_health(score) == "Excellent"


def test_critical_delayed_project():
    record = {
        "Status": "Delayed",
        "Progress": 20.0,
        "Remaining_Days": -15,
        "Budget": 200000,
        "Actual_Cost": 350000, # Severe overrun
        "Open_Bugs": 22,
        "Sprint_Velocity": 12.0,
        "Team_Utilization": 98.0
    }
    score = compute_project_health(record)
    assert score < 60
    assert categorize_health(score) == "Critical"
