"""
Risk Prediction Portal --- Real-Time XGBoost Inference & What-If PMO Governance Simulator.
Refined Off-White Light SaaS corporate UI.
"""
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.logger import get_logger
from utils.theme import COLORS, RISK_COLOR_MAP, get_plotly_layout, render_top_navbar
from utils.ml_engine import RiskPredictionEngine

logger = get_logger(__name__)

st.set_page_config(page_title="Risk Prediction | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_resource
def get_ml_engine() -> RiskPredictionEngine:
    engine = RiskPredictionEngine()
    engine.load_model()
    return engine


def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px;">
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Predictive Quantitative Risk Inference</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Real-time XGBoost classification simulating delivery parameters and global SHAP feature attribution.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    render_top_navbar()
    render_header()
    engine = get_ml_engine()
    
    col_sim, col_res = st.columns([4, 6])
    
    with col_sim:
        st.markdown("""
        <div class="industry-panel" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 14px; color: #0066CC; margin-bottom: 4px;">Simulation Parameter Controls</div>
            <p style="font-size: 12px; color: #64748B; margin: 0; line-height: 1.5;">Adjust operational levers below to test portfolio resilience under financial and delivery turbulence.</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress = st.slider("Milestone Progress (%)", min_value=0.0, max_value=100.0, value=55.0, step=5.0)
        remaining_days = st.slider("Remaining Schedule Buffer (Days)", min_value=-45, max_value=180, value=30, step=5)
        open_bugs = st.slider("Active Defect Backlog", min_value=0, max_value=35, value=6, step=1)
        velocity = st.slider("Sprint Delivery Velocity (pts)", min_value=5.0, max_value=60.0, value=32.0, step=1.0)
        budget = st.number_input("Approved Baseline Authorization ($)", min_value=50000, max_value=2000000, value=450000, step=25000)
        actual_cost = st.number_input("Cumulative Actual Spend ($)", min_value=0, max_value=3000000, value=320000, step=25000)
        team_size = st.slider("Assigned Roster Headcount", min_value=3, max_value=25, value=8, step=1)

    input_profile = {
        "Budget": float(budget),
        "Actual_Cost": float(actual_cost),
        "Progress": float(progress),
        "Sprint_Velocity": float(velocity),
        "Team_Size": float(team_size),
        "Open_Bugs": float(open_bugs),
        "Remaining_Days": float(remaining_days)
    }

    pred_label, probs_dict, df_imp = engine.predict(input_profile)

    with col_res:
        risk_color = RISK_COLOR_MAP.get(pred_label, COLORS["muted"])
        
        st.markdown(f"""
        <div style="
            background-color: #FFFFFF;
            border-left: 6px solid {risk_color};
            border-top: 1px solid #E2E8F0;
            border-right: 1px solid #E2E8F0;
            border-bottom: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);
        ">
            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #64748B; font-weight: 600; font-family: 'JetBrains Mono', monospace;">XGBoost Quantitative Assessment</div>
            <div style="font-size: 28px; font-weight: 700; color: {risk_color}; margin: 8px 0; font-family: 'Inter', sans-serif;">{pred_label.upper()} GOVERNANCE RISK</div>
            <div style="font-size: 13px; color: #334155;">
                Classification Confidence: <strong style="color: {risk_color}; font-family: 'JetBrains Mono', monospace;">{probs_dict[pred_label]*100:.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        df_probs = pd.DataFrame({
            "Risk Category": list(probs_dict.keys()),
            "Probability": list(probs_dict.values())
        })
        
        fig_prob = px.bar(
            df_probs,
            x="Probability",
            y="Risk Category",
            orientation="h",
            color="Risk Category",
            color_discrete_map=RISK_COLOR_MAP,
            text_auto=".1%"
        )
        fig_prob.update_traces(width=0.45)
        layout_p = get_plotly_layout("Inference Class Probabilities", height=200)
        layout_p["xaxis"] = dict(range=[0, 1], showgrid=True, gridcolor="#F1F5F9")
        fig_prob.update_layout(**layout_p, showlegend=False)
        st.plotly_chart(fig_prob, width="stretch")

        fig_imp = px.bar(
            df_imp,
            x="Importance",
            y="Feature",
            orientation="h",
            color_discrete_sequence=[COLORS["primary"]]
        )
        fig_imp.update_traces(width=0.55)
        layout_i = get_plotly_layout("Global Feature Attribution (SHAP Proxy)", height=320)
        fig_imp.update_layout(**layout_i)
        fig_imp.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_imp, width="stretch")


if __name__ == "__main__":
    main()
