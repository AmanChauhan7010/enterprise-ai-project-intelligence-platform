"""
Enterprise AI Project Intelligence Platform --- Entry Point & Hub Landing Portal.
Refined Off-White Light SaaS UI (top horizontal navigation bar, zero left sidebar).
"""
import os
import streamlit as st
import pandas as pd
from utils.logger import get_logger
from utils.theme import render_top_navbar

logger = get_logger(__name__)

st.set_page_config(
    page_title="Platform Intelligence | Enterprise PMO",
    layout="wide",
    initial_sidebar_state="collapsed"
)


@st.cache_resource(show_spinner="Initializing Telemetry Core & XGBoost Models...")
def bootstrap_system() -> bool:
    from utils.data_generator import generate_enterprise_datasets
    from utils.ml_engine import RiskPredictionEngine
    
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    if not os.path.exists("data/projects.csv"):
        generate_enterprise_datasets()
        
    if not os.path.exists("models/xgb_risk_model.joblib"):
        engine = RiskPredictionEngine()
        engine.train_and_persist()
        
    return True


def inject_custom_css():
    css_path = "assets/style.css"
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    inject_custom_css()
    bootstrap_system()
    render_top_navbar()
    
    # Landing Portal Header
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 24px; margin-bottom: 28px;">
        <h1 style="margin: 0; font-size: 28px; color: #0F172A; font-weight: 700; letter-spacing: -0.03em;">Enterprise Transformation Governance</h1>
        <p style="margin: 8px 0 0 0; font-size: 14px; color: #475569; max-width: 900px; line-height: 1.6;">
            Quantitative transformation governance platform modeling 150 enterprise initiatives across AI, Cloud, Data Engineering, and Digital sectors. Features correlated predictive risk telemetry (XGBoost), agile burndown diagnostics, and heuristic decision insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px;'>Diagnostic Governance Modules</div>", unsafe_allow_html=True)
    
    # Navigation Cards
    grid_data = [
        ("Executive Overview", "High-level practice KPIs, financial burn rates, and monthly kickoff trends.", "pages/1_Executive_Dashboard.py"),
        ("Portfolio Inventory", "Searchable data grid filterable by Client, Tech, Manager, Risk, and Status.", "pages/2_Portfolio_View.py"),
        ("Project Inspection Hub", "Granular inspection hub displaying Gantt milestone execution and risk registries.", "pages/3_Project_Details.py"),
        ("Predictive Risk Sim", "Real-time XGBoost What-If simulation parameters and SHAP attribution plots.", "pages/4_Risk_Prediction.py"),
        ("Resource Management", "Practice talent allocation heatmaps, billing rate curves, and bench capacity.", "pages/5_Resource_Management.py"),
        ("Sprint Analytics", "Agile cadence delivery curves, burndown diagnostics, and defect trends.", "pages/6_Sprint_Analytics.py"),
        ("Budget Analytics", "Estimate at Completion (EAC) forecasting and practice cost overrun ledgers.", "pages/7_Budget_Analytics.py"),
        ("Executive Briefing", "Heuristic intelligence synthesis formulating automated remediation directives.", "pages/8_AI_Executive_Insights.py")
    ]
    
    cols = st.columns(4)
    for i, (title, desc, path) in enumerate(grid_data):
        col = cols[i % 4]
        with col:
            st.markdown(f"""
            <div class="industry-panel" style="height: 110px; margin-bottom: 12px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-weight: 700; font-size: 14px; color: #0066CC;">{title}</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 6px; line-height: 1.4;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.page_link(path, label=f"Launch {title.split()[0]} →", width="stretch")
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
