"""
Resource Management --- Headcount Distribution, Department Utilization, Billing Intensity, and Saturation Benches.
Refined Off-White Light SaaS corporate UI.
"""
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.logger import get_logger
from utils.theme import COLORS, get_plotly_layout, render_kpi_card_html, render_top_navbar

logger = get_logger(__name__)

st.set_page_config(page_title="Resource Analytics | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def load_data() -> pd.DataFrame:
    path = "data/employees.csv"
    if not os.path.exists(path):
        from utils.data_generator import generate_enterprise_datasets
        generate_enterprise_datasets()
    return pd.read_csv(path)


def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px;">
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Talent Allocation & Practice Bandwidth</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Headcount mapping across 560 practice engineers, departmental billing intensity, and bench capacity analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    render_top_navbar()
    df = load_data()
    render_header()

    tot_emp = len(df)
    avg_alloc = df["Allocation_Pct"].mean()
    avg_rate = df["Hourly_Rate_USD"].mean()
    over_alloc = len(df[df["Allocation_Pct"] >= 100])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_kpi_card_html("Total Headcount", f"{tot_emp}", "Consulting roster"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card_html("Practice Utilization", f"{avg_alloc:.1f}%", "Target >80%"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card_html("Fully Committed Staff", f"{over_alloc}", f"{over_alloc/tot_emp*100:.1f}% saturated"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card_html("Average Billing Rate", f"${avg_rate:.0f}/hr", "Commercial yield"), unsafe_allow_html=True)

    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        dept_counts = df["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Headcount"]
        
        fig_donut = px.pie(
            dept_counts,
            names="Department",
            values="Headcount",
            hole=0.55,
            color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["info"], COLORS["success"]]
        )
        layout_d = get_plotly_layout("Headcount Distribution by Sector", height=340)
        fig_donut.update_layout(**layout_d)
        st.plotly_chart(fig_donut, width="stretch")

    with col2:
        dept_util = df.groupby("Department")[["Allocation_Pct", "Availability_Pct"]].mean().reset_index()
        
        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(x=dept_util["Department"], y=dept_util["Allocation_Pct"], name="Allocated %", marker_color=COLORS["primary"], width=0.4))
        fig_stack.add_trace(go.Bar(x=dept_util["Department"], y=dept_util["Availability_Pct"], name="Bench Capacity %", marker_color=COLORS["muted"], width=0.4))
        layout_s = get_plotly_layout("Average Utilization vs Bench Capacity", height=340)
        fig_stack.update_layout(**layout_s, barmode="stack")
        st.plotly_chart(fig_stack, width="stretch")

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    col3, col4 = st.columns([6, 4])

    with col3:
        role_rates = df.groupby("Role")["Hourly_Rate_USD"].mean().sort_values(ascending=False).reset_index()
        
        fig_rate = px.bar(
            role_rates,
            x="Hourly_Rate_USD",
            y="Role",
            orientation="h",
            color_discrete_sequence=[COLORS["secondary"]],
            text_auto="$.0f"
        )
        fig_rate.update_traces(width=0.55)
        layout_r = get_plotly_layout("Billing Yield by Engineering Role ($/hr)", height=360)
        fig_rate.update_layout(**layout_r)
        fig_rate.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_rate, width="stretch")

    with col4:
        st.markdown("<div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;'>Saturated Headcount Roster (100% Alloc)</div>", unsafe_allow_html=True)
        sat_df = df[df["Allocation_Pct"] >= 100][["Employee_ID", "Name", "Role", "Department"]]
        st.dataframe(sat_df, width="stretch", hide_index=True, height=310)


if __name__ == "__main__":
    main()
