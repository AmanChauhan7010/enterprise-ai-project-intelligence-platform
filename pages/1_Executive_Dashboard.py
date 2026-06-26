"""
Executive Dashboard --- Macro Portfolio Telemetry & KPIs.
Refined Off-White Light SaaS aesthetic.
"""
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.logger import get_logger
from utils.theme import COLORS, STATUS_COLOR_MAP, RISK_COLOR_MAP, get_plotly_layout, render_kpi_card_html, render_top_navbar

logger = get_logger(__name__)

st.set_page_config(page_title="Executive Overview | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def load_data() -> pd.DataFrame:
    path = "data/projects.csv"
    if not os.path.exists(path):
        from utils.data_generator import generate_enterprise_datasets
        generate_enterprise_datasets()
    return pd.read_csv(path)


def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px;">
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Executive Portfolio Overview</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Macro telemetry of transformation governance, practice financial commitments, and quantitative risk distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_kpis(df: pd.DataFrame):
    total_proj = len(df)
    active_proj = len(df[df["Status"] == "Active"])
    delayed_proj = len(df[df["Status"] == "Delayed"])
    completed_proj = len(df[df["Status"] == "Completed"])
    
    total_budget = df["Budget"].sum()
    total_actual = df["Actual_Cost"].sum()
    budget_util = (total_actual / total_budget * 100) if total_budget > 0 else 0.0
    
    avg_health = df["Health_Score"].mean()
    avg_progress = df["Progress"].mean()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_kpi_card_html("Total Initiatives", f"{total_proj}", "+14% YoY"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card_html("Active Portfolio", f"{active_proj}", f"{active_proj/total_proj*100:.1f}% share"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card_html("Schedule Slippage", f"{delayed_proj}", "Attention Req", delta_color="inverse"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card_html("Delivered Cutover", f"{completed_proj}", "Nominal"), unsafe_allow_html=True)
        
    st.markdown("<div style='margin: 14px 0;'></div>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(render_kpi_card_html("Committed CapEx", f"${total_budget/1e6:.2f}M", "Approved baseline"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_kpi_card_html("Budget Burn Ratio", f"{budget_util:.1f}%", f"${total_actual/1e6:.2f}M spend"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_kpi_card_html("Practice Health Index", f"{avg_health:.1f}", "Weighted PMO avg"), unsafe_allow_html=True)
    with m4:
        st.markdown(render_kpi_card_html("Aggregate Progress", f"{avg_progress:.1f}%", "Milestone completion"), unsafe_allow_html=True)


def render_charts(df: pd.DataFrame):
    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig_status = go.Figure(data=[go.Pie(
            labels=status_counts["Status"],
            values=status_counts["Count"],
            hole=0.6,
            marker=dict(colors=[STATUS_COLOR_MAP.get(s, COLORS["primary"]) for s in status_counts["Status"]], line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent",
            hoverinfo="label+value+percent"
        )])
        layout = get_plotly_layout("Status Breakdown", height=320)
        fig_status.update_layout(**layout)
        st.plotly_chart(fig_status, width="stretch")
        
    with col_chart2:
        risk_counts = df["Risk"].value_counts().reindex(["Low", "Medium", "High"]).reset_index()
        risk_counts.columns = ["Risk", "Count"]
        
        fig_risk = go.Figure(data=[go.Bar(
            x=risk_counts["Risk"],
            y=risk_counts["Count"],
            marker_color=[RISK_COLOR_MAP.get(r, COLORS["muted"]) for r in risk_counts["Risk"]],
            width=0.45,
            text=risk_counts["Count"],
            textposition="auto"
        )])
        layout = get_plotly_layout("XGBoost Risk Classification", height=320)
        fig_risk.update_layout(**layout)
        st.plotly_chart(fig_risk, width="stretch")
        
    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        dept_counts = df["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]
        
        fig_dept = px.bar(
            dept_counts, 
            y="Department", 
            x="Count", 
            orientation="h",
            color_discrete_sequence=[COLORS["primary"]]
        )
        fig_dept.update_traces(width=0.45)
        layout = get_plotly_layout("Practice Sector Allocation", height=340)
        fig_dept.update_layout(**layout)
        st.plotly_chart(fig_dept, width="stretch")
        
    with col_chart4:
        dept_budget = df.groupby("Department")[["Budget", "Actual_Cost"]].sum().reset_index()
        
        fig_budget = go.Figure()
        fig_budget.add_trace(go.Bar(
            x=dept_budget["Department"],
            y=dept_budget["Budget"]/1e6,
            name="Committed ($M)",
            marker_color=COLORS["primary"],
            width=0.3
        ))
        fig_budget.add_trace(go.Bar(
            x=dept_budget["Department"],
            y=dept_budget["Actual_Cost"]/1e6,
            name="Actual Spend ($M)",
            marker_color=COLORS["secondary"],
            width=0.3
        ))
        layout = get_plotly_layout("Financial Commitments by Practice ($M)", height=340)
        fig_budget.update_layout(**layout, barmode="group")
        st.plotly_chart(fig_budget, width="stretch")

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    df["Start_Date"] = pd.to_datetime(df["Start_Date"])
    df_trend = df.set_index("Start_Date").resample("ME")["Project_ID"].count().reset_index()
    df_trend.columns = ["Month", "New_Initiatives"]
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_trend["Month"],
        y=df_trend["New_Initiatives"],
        mode="lines",
        line=dict(color=COLORS["info"], width=2.5),
        fill="tozeroy",
        fillcolor="rgba(2, 132, 199, 0.08)"
    ))
    layout = get_plotly_layout("Monthly Initiative Kickoff Cadence", height=300)
    fig_trend.update_layout(**layout)
    st.plotly_chart(fig_trend, width="stretch")


def main():
    render_top_navbar()
    df = load_data()
    render_header()
    render_kpis(df)
    render_charts(df)


if __name__ == "__main__":
    main()
