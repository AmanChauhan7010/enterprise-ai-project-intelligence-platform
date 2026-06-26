"""
Budget Analytics --- Financial Governance, EAC Forecasting, Department Spend Ratios, and Overrun Variance.
Refined Off-White Light SaaS corporate UI.
"""
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.logger import get_logger
from utils.theme import COLORS, get_plotly_layout, render_kpi_card_html, render_top_navbar

logger = get_logger(__name__)

st.set_page_config(page_title="Financial Governance | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def load_data():
    if not os.path.exists("data/projects.csv"):
        from utils.data_generator import generate_enterprise_datasets
        generate_enterprise_datasets()
    return pd.read_csv("data/projects.csv")


def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px;">
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Financial Governance & CapEx Burn</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Estimate at Completion (EAC) forecasting, practice burn ledgers, and cost overrun exposures.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    render_top_navbar()
    df = load_data()
    render_header()

    prog_ratio = df["Progress"] / 100.0
    df["Forecast_EAC"] = np.where(prog_ratio > 0.05, df["Actual_Cost"] / prog_ratio, df["Budget"])
    df["Cost_Overrun"] = df["Forecast_EAC"] - df["Budget"]

    tot_budget = df["Budget"].sum()
    tot_actual = df["Actual_Cost"].sum()
    tot_forecast = df["Forecast_EAC"].sum()
    tot_overrun = df[df["Cost_Overrun"] > 0]["Cost_Overrun"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_kpi_card_html("BAC Committed Budget", f"${tot_budget:,.0f}", "Baseline CapEx"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card_html("Actual Spend to Date", f"${tot_actual:,.0f}", f"{tot_actual/tot_budget*100:.1f}% burn"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card_html("EAC Forecast Spend", f"${tot_forecast:,.0f}", f"${tot_forecast-tot_budget:,.0f} net var"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card_html("Total Projected Overrun", f"${tot_overrun:,.0f}", "Financial exposure", delta_color="inverse"), unsafe_allow_html=True)

    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        dept_fin = df.groupby("Department")[["Budget", "Actual_Cost", "Forecast_EAC"]].sum().reset_index()
        
        fig_dept = go.Figure()
        fig_dept.add_trace(go.Bar(x=dept_fin["Department"], y=dept_fin["Budget"]/1e6, name="BAC ($M)", marker_color=COLORS["primary"], width=0.25))
        fig_dept.add_trace(go.Bar(x=dept_fin["Department"], y=dept_fin["Actual_Cost"]/1e6, name="Actual ($M)", marker_color=COLORS["info"], width=0.25))
        fig_dept.add_trace(go.Bar(x=dept_fin["Department"], y=dept_fin["Forecast_EAC"]/1e6, name="EAC ($M)", marker_color=COLORS["warning"], width=0.25))
        layout_d = get_plotly_layout("Financial Variance by Practice ($M)", height=360)
        fig_dept.update_layout(**layout_d, barmode="group")
        st.plotly_chart(fig_dept, width="stretch")

    with col2:
        fig_pie = px.pie(
            df,
            names="Department",
            values="Actual_Cost",
            hole=0.55,
            color_discrete_sequence=[COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["info"]]
        )
        layout_p = get_plotly_layout("Actual Spend Share Breakdown", height=360)
        fig_pie.update_layout(**layout_p)
        st.plotly_chart(fig_pie, width="stretch")

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    col3, col4 = st.columns([6, 4])

    with col3:
        top_overruns = df[df["Cost_Overrun"] > 1000].sort_values(by="Cost_Overrun", ascending=False).head(10)
        
        fig_bar = px.bar(
            top_overruns,
            x="Cost_Overrun",
            y="Project_Name",
            orientation="h",
            color="Department",
            text_auto="$.2s",
            labels={"Cost_Overrun": "Overrun ($)", "Project_Name": "Initiative"}
        )
        fig_bar.update_traces(width=0.5)
        layout_b = get_plotly_layout("Top Initiatives by Overrun Variance Exposure", height=360)
        fig_bar.update_layout(**layout_b)
        fig_bar.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_bar, width="stretch")

    with col4:
        st.markdown("<div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;'>High Overrun Risk Ledger (> $25k var)</div>", unsafe_allow_html=True)
        high_var = df[df["Cost_Overrun"] > 25000][["Project_ID", "Project_Name", "Budget", "Forecast_EAC"]]
        high_var["Forecast_EAC"] = high_var["Forecast_EAC"].round(0)
        st.dataframe(high_var, width="stretch", hide_index=True, height=310)


if __name__ == "__main__":
    main()
