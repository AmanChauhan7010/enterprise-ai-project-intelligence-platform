"""
Project Health Scorer Engine.
Computes deterministic weighted health score (0-100) and assigns governance categories.
"""
from typing import Dict, Tuple, Union
import pandas as pd
import numpy as np


def compute_project_health(row: Union[pd.Series, Dict]) -> int:
    """
    Computes a weighted project health score out of 100.
    
    Weights:
        - Schedule Adherence (25%)
        - Budget Efficiency (20%)
        - Progress Adherence (20%)
        - Bug Quality (15%)
        - Sprint Velocity (10%)
        - Team Utilization (10%)
        
    Args:
        row (Union[pd.Series, Dict]): Project record containing key metrics.
        
    Returns:
        int: Bounded health score between 0 and 100.
    """
    # 1. Progress (20%) - direct progress score
    progress = float(row.get("Progress", 50))
    score_progress = min(max(progress, 0.0), 100.0)
    
    # 2. Schedule Adherence (25%)
    # If Status is Delayed, severe penalty. Otherwise scale based on Remaining Days and Progress.
    status = str(row.get("Status", "Active"))
    remaining_days = float(row.get("Remaining_Days", 30))
    if status == "Completed":
        score_schedule = 100.0
    elif status == "Delayed":
        score_schedule = max(30.0, 70.0 - (100 - progress) * 0.5)
    else:
        # Active or Planned
        if remaining_days > 15:
            score_schedule = 95.0
        elif remaining_days > 0:
            score_schedule = 80.0
        else:
            score_schedule = 40.0
            
    # 3. Budget Efficiency (20%)
    budget = float(row.get("Budget", 100000))
    actual_cost = float(row.get("Actual_Cost", 50000))
    if budget > 0:
        utilization_ratio = (actual_cost / budget)
        expected_ratio = (progress / 100.0)
        # If cost is well aligned with progress
        overrun = utilization_ratio - expected_ratio
        if overrun <= 0.05:
            score_budget = 100.0
        elif overrun <= 0.15:
            score_budget = 80.0
        elif overrun <= 0.30:
            score_budget = 60.0
        else:
            score_budget = max(20.0, 100.0 - overrun * 150.0)
    else:
        score_budget = 80.0
        
    # 4. Bug Quality (15%)
    open_bugs = float(row.get("Open_Bugs", 2))
    score_bugs = max(0.0, 100.0 - (open_bugs * 7.5))
    
    # 5. Velocity (10%)
    velocity = float(row.get("Sprint_Velocity", 30))
    # Typical velocity 20-50 is healthy
    score_velocity = min(100.0, max(40.0, (velocity / 40.0) * 100.0))
    
    # 6. Team Utilization (10%)
    team_size = float(row.get("Team_Size", 5))
    # Simulate team utilization proxy based on team size and progress
    util = float(row.get("Team_Utilization", 82.0))
    if 75.0 <= util <= 88.0:
        score_util = 100.0
    elif 65.0 <= util < 75.0 or 88.0 < util <= 95.0:
        score_util = 80.0
    else:
        score_util = 50.0
        
    # Weighted calculation
    total_score = (
        0.25 * score_schedule +
        0.20 * score_budget +
        0.20 * score_progress +
        0.15 * score_bugs +
        0.10 * score_velocity +
        0.10 * score_util
    )
    
    return int(round(min(max(total_score, 0), 100)))


def categorize_health(score: int) -> str:
    """
    Categorizes health score into enterprise PMO governance brackets.
    
    Args:
        score (int): Health score 0-100.
        
    Returns:
        str: Category label ('Excellent', 'Good', 'Needs Attention', 'Critical').
    """
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Needs Attention"
    else:
        return "Critical"
