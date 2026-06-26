"""
Unit Tests for Correlated Synthetic Dataset Generator.
"""
import os
import pandas as pd
from utils.data_generator import generate_enterprise_datasets


def test_datasets_generation():
    df_p, df_e, df_s, df_m = generate_enterprise_datasets(num_projects=15, target_employees=50, target_sprints=80, target_meetings=100, seed=101, output_dir=None)
    
    assert len(df_p) == 15
    assert not df_e.empty
    assert not df_s.empty
    assert not df_m.empty
    
    # Verify correlation constraints
    delayed = df_p[df_p["Status"] == "Delayed"]
    if not delayed.empty:
        # Delayed projects should generally have higher bugs or cost variance
        assert delayed["Open_Bugs"].mean() >= 5
