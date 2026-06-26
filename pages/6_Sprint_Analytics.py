"""
Sprint Analytics --- Burndown Execution Trajectories, Velocity Consistency, and Quality Trends.
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

st.set_page_config(page_title="Sprint Diagnostics | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def load_data():
    if not os.path.exists("data/sprints.csv"):
        from utils.data_generator import generate_enterprise_datasets
        generate_enterprise_datasets()
    return pd.read_csv("data/sprints.csv"), pd.read_csv("data/projects.csv")


def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px;">
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Agile Delivery Telemetry</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Cadence burndown diagnostics across 900 sprint records, velocity stability curves, and defect arrival ledgers.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    render_top_navbar()
    df_s, df_p = load_data()
    render_header()

    proj_map = dict(zip(df_p["Project_ID"], df_p["Project_Name"]))
    filter_opts = ["Global Practice Aggregate"] + [f"{pid} - {name}" for pid, name in proj_map.items() if pid in df_s["Project_ID"].values]
    
    sel_proj = st.selectbox("Filter Cadence Scope", options=filter_opts)

    sub_df = df_s.copy()
    if sel_proj != "Global Practice Aggregate":
        target_id = sel_proj.split(" - ")[0]
        sub_df = sub_df[sub_df["Project_ID"] == target_id]

    if sub_df.empty:
        st.warning("No sprint telemetry logged for selected scope.")
        return

    tot_planned = sub_df["Planned_Story_Points"].sum()
    tot_completed = sub_df["Completed_Story_Points"].sum()
    comp_rate = (tot_completed / tot_planned * 100) if tot_planned > 0 else 0
    avg_vel = sub_df["Velocity"].mean()
    tot_bugs_open = sub_df["Open_Defects_Accumulated"].sum()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card_html("Delivered Story Points", f"{tot_completed:,.0f}", f"of {tot_planned:,.0f} planned"), unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card_html("Cadence Completion Yield", f"{comp_rate:.1f}%", "Target >85%"), unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card_html("Average Velocity", f"{avg_vel:.1f} pts", "Capacity index"), unsafe_allow_html=True)
    with k4:
        st.markdown(render_kpi_card_html("Accumulated Defect Friction", f"{tot_bugs_open}", "Quality headwind", delta_color="inverse"), unsafe_allow_html=True)

    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        burn_df = sub_df.groupby("Sprint_Number")[["Planned_Story_Points", "Completed_Story_Points"]].mean().reset_index()
        
        fig_burn = go.Figure()
        fig_burn.add_trace(go.Bar(x=burn_df["Sprint_Number"], y=burn_df["Planned_Story_Points"], name="Planned Points", marker_color=COLORS["muted"], width=0.35))
        fig_burn.add_trace(go.Bar(x=burn_df["Sprint_Number"], y=burn_df["Completed_Story_Points"], name="Completed Points", marker_color=COLORS["primary"], width=0.35))
        layout = get_plotly_layout("Sprint Burndown Trajectory", height=340)
        fig_burn.update_layout(**layout, barmode="group")
        st.plotly_chart(fig_burn, width="stretch")

    with c2:
        vel_df = sub_df.groupby("Sprint_Number")["Velocity"].mean().reset_index()
        
        fig_vel = px.line(vel_df, x="Sprint_Number", y="Velocity", markers=True)
        fig_vel.update_traces(line_color=COLORS["success"], line_width=3, marker_size=7)
        layout_v = get_plotly_layout("Velocity Stability Trajectory", height=340)
        fig_vel.update_layout(**layout_v)
        st.plotly_chart(fig_vel, width="stretch")

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        bug_df = sub_df.groupby("Sprint_Number")[["Bugs_Raised", "Bugs_Resolved"]].sum().reset_index()
        
        fig_bug = go.Figure()
        fig_bug.add_trace(go.Scatter(x=bug_df["Sprint_Number"], y=bug_df["Bugs_Raised"], name="Bugs Raised", mode="lines+markers", line=dict(color=COLORS["danger"], width=2.5), fill="tozeroy", fillcolor="rgba(220, 38, 38, 0.08)"))
        fig_bug.add_trace(go.Scatter(x=bug_df["Sprint_Number"], y=bug_df["Bugs_Resolved"], name="Bugs Resolved", mode="lines+markers", line=dict(color=COLORS["info"], width=2.5), fill="tonexty", fillcolor="rgba(2, 132, 199, 0.08)"))
        layout_b = get_plotly_layout("Defect Arrival vs Resolution Curve", height=340)
        fig_bug.update_layout(**layout_b)
        st.plotly_chart(fig_bug, width="stretch")

    with c4:
        fig_hist = px.histogram(
            sub_df,
            x="Completion_Rate_Pct",
            nbins=12,
            color_discrete_sequence=[COLORS["secondary"]],
            labels={"Completion_Rate_Pct": "Completion Yield (%)", "count": "Frequency"}
        )
        layout_h = get_plotly_layout("Completion Yield Frequency", height=340)
        fig_hist.update_layout(**layout_h)
        st.plotly_chart(fig_hist, width="stretch")


if __name__ == "__main__":
    main()
