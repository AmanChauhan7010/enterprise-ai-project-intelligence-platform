"""
Project Details Hub --- Deep-Dive Telemetry, Gantt Milestones, Dependencies, Sprints, and Team Roster.
Refined Off-White Light SaaS corporate UI.
"""
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.logger import get_logger
from utils.theme import COLORS, RISK_COLOR_MAP, get_plotly_layout, render_top_navbar

logger = get_logger(__name__)

st.set_page_config(page_title="Project Inspection | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def load_all_datasets():
    if not os.path.exists("data/projects.csv"):
        from utils.data_generator import generate_enterprise_datasets
        generate_enterprise_datasets()
    return (
        pd.read_csv("data/projects.csv"),
        pd.read_csv("data/employees.csv"),
        pd.read_csv("data/sprints.csv"),
        pd.read_csv("data/meetings.csv")
    )


def render_milestones_gantt(project_row: pd.Series):
    start_dt = pd.to_datetime(project_row["Start_Date"])
    end_dt = pd.to_datetime(project_row["End_Date"])
    total_duration = (end_dt - start_dt).days
    if total_duration <= 0:
        total_duration = 60
        
    milestones = [
        ("Phase 1: Discovery & Architecture Baseline", 0.0, 0.18),
        ("Phase 2: Core Platform Mesh Setup", 0.15, 0.38),
        ("Phase 3: Iterative Solution Engineering", 0.35, 0.72),
        ("Phase 4: Security Audit & Integration Testing", 0.65, 0.88),
        ("Phase 5: User Acceptance Signoff & Cutover", 0.82, 1.0)
    ]
    
    gantt_data = []
    for m_name, s_pct, e_pct in milestones:
        m_start = start_dt + pd.Timedelta(days=int(total_duration * s_pct))
        m_end = start_dt + pd.Timedelta(days=int(total_duration * e_pct))
        progress_pct = project_row["Progress"]
        
        req_pct = e_pct * 100
        if progress_pct >= req_pct:
            state = "Completed"
        elif progress_pct >= s_pct * 100:
            state = "In Execution"
        else:
            state = "Pending Scheduled"
            
        gantt_data.append({
            "Milestone Window": m_name,
            "Start Date": m_start,
            "Target Date": m_end,
            "Execution State": state
        })
        
    df_g = pd.DataFrame(gantt_data)
    
    fig = px.timeline(
        df_g, 
        x_start="Start Date", 
        x_end="Target Date", 
        y="Milestone Window", 
        color="Execution State",
        color_discrete_map={"Completed": COLORS["success"], "In Execution": COLORS["primary"], "Pending Scheduled": COLORS["muted"]}
    )
    fig.update_yaxes(autorange="reversed")
    layout = get_plotly_layout("Milestone Execution Gantt Trajectory", height=320)
    fig.update_layout(**layout)
    st.plotly_chart(fig, width="stretch")


def main():
    render_top_navbar()
    df_p, df_e, df_s, _ = load_all_datasets()
    
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px;">
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Initiative Diagnostic Inspection Hub</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Granular drilldown examining financial variance, Gantt trajectories, risk registers, and assigned rosters.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    options = df_p["Project_ID"] + " - " + df_p["Project_Name"]
    selected_str = st.selectbox("Select Target Transformation Initiative", options=options)
    
    if not selected_str:
        return
        
    sel_id = selected_str.split(" - ")[0]
    p_row = df_p[df_p["Project_ID"] == sel_id].iloc[0]
    
    status_lower = p_row['Status'].lower()
    risk_color = RISK_COLOR_MAP.get(p_row['Risk'], '#64748B')
    
    st.markdown(f"""
    <div class="industry-panel" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #0066CC; font-weight: 700; font-size: 13px; font-family: 'JetBrains Mono', monospace;">[{p_row['Project_ID']}] &nbsp; {p_row['Department']}</span>
                <h2 style="margin: 6px 0 8px 0; color: #0F172A; font-size: 20px;">{p_row['Project_Name']}</h2>
                <div style="color: #475569; font-size: 12px;">
                    Client Entity: <strong style="color: #1E293B;">{p_row['Client']}</strong> &nbsp;|&nbsp; 
                    Technology: <strong style="color: #1E293B;">{p_row['Technology']}</strong> &nbsp;|&nbsp; 
                    Director: <strong style="color: #1E293B;">{p_row['Manager']}</strong>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="margin-bottom: 8px;">
                    <span class="status-pill pill-{status_lower}">{p_row['Status']}</span> &nbsp;
                    <span style="display:inline-block; padding: 2px 8px; font-size:11px; font-weight:700; border-radius:4px; background-color:{risk_color}15; color:{risk_color}; border:1px solid {risk_color}44; font-family:'JetBrains Mono', monospace;">RISK: {p_row['Risk']}</span>
                </div>
                <div style="font-size: 26px; font-weight: 700; color: {COLORS['success'] if p_row['Health_Score']>=75 else COLORS['warning']}; font-family: 'Inter', sans-serif;">
                    {p_row['Health_Score']} <span style="font-size: 12px; font-weight: 600; color: #64748B;">/ 100 HEALTH INDEX</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs(["Schedule & Gantt", "Financial Variance", "Dependencies & Risks", "Committed Roster", "Agile Telemetry"])
    
    with t1:
        render_milestones_gantt(p_row)
        st.caption(f"Operational Window: {p_row['Start_Date']} to {p_row['End_Date']} ({p_row['Remaining_Days']} remaining business days).")

    with t2:
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            st.metric("Committed Baseline (BAC)", f"${p_row['Budget']:,.0f}")
        with c_b2:
            st.metric("Actual Spend to Date", f"${p_row['Actual_Cost']:,.0f}", delta=f"{p_row['Actual_Cost'] - p_row['Budget']:,.0f} var" if p_row['Actual_Cost']>p_row['Budget'] else "aligned")
        with c_b3:
            burn_pct = (p_row['Actual_Cost'] / p_row['Budget'] * 100) if p_row['Budget']>0 else 0
            st.metric("CapEx Burn Ratio", f"{burn_pct:.1f}%")
            
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=p_row["Actual_Cost"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Spend Burn vs Baseline Authorization", "font": {"size": 13, "color": "#334155"}},
            gauge={
                "axis": {"range": [None, p_row["Budget"] * 1.5], "tickcolor": "#334155"},
                "bar": {"color": COLORS["danger"] if burn_pct>100 else COLORS["primary"]},
                "bgcolor": "#F1F5F9",
                "threshold": {"line": {"color": COLORS["warning"], "width": 3}, "thickness": 0.8, "value": p_row["Budget"]}
            }
        ))
        layout = get_plotly_layout(height=280)
        fig_gauge.update_layout(**layout)
        st.plotly_chart(fig_gauge, width="stretch")

    with t3:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("<div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;'>Upstream / Downstream Dependencies</div>", unsafe_allow_html=True)
            deps = [
                {"Architecture Component": "Core Data Lakehouse Pipeline Mesh", "Practice Owner": "Data Eng", "Verification State": "Nominal"},
                {"Architecture Component": "Zero-Trust Single Sign-On Gateway", "Practice Owner": "Cybersecurity", "Verification State": "Slippage Risk" if p_row["Status"]=="Delayed" else "Nominal"},
                {"Architecture Component": "Multi-Region Terraform Landing Zone", "Practice Owner": "Cloud Ops", "Verification State": "Nominal"}
            ]
            st.dataframe(pd.DataFrame(deps), width="stretch", hide_index=True)
            
        with col_d2:
            st.markdown("<div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;'>Risk Register & Mitigation Protocols</div>", unsafe_allow_html=True)
            risks = [
                {"Risk Attribute": f"Accumulated Defect Backlog ({p_row['Open_Bugs']})", "Severity": "High" if p_row['Open_Bugs']>10 else "Low", "Remediation Action": "Formal QA defect triage."},
                {"Risk Attribute": "Engineering Bandwidth Saturation", "Severity": "Medium", "Remediation Action": "Rebalancing department capacity."}
            ]
            st.dataframe(pd.DataFrame(risks), width="stretch", hide_index=True)

    with t4:
        st.markdown(f"<div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;'>Committed Talent Roster ({p_row['Team_Size']} headcount allocated)</div>", unsafe_allow_html=True)
        sub_e = df_e[df_e["Assigned_Project_ID"] == sel_id]
        if not sub_e.empty:
            st.dataframe(
                sub_e[["Employee_ID", "Name", "Role", "Allocation_Pct", "Hourly_Rate_USD"]],
                width="stretch",
                hide_index=True
            )
        else:
            st.warning("No individual engineer records currently mapped to this initiative ID.")

    with t5:
        st.markdown("<div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;'>Historical Sprint Execution Trajectories</div>", unsafe_allow_html=True)
        sub_s = df_s[df_s["Project_ID"] == sel_id]
        if not sub_s.empty:
            fig_sprint = go.Figure()
            fig_sprint.add_trace(go.Bar(x=sub_s["Sprint_Number"], y=sub_s["Planned_Story_Points"], name="Planned Points", marker_color=COLORS["muted"]))
            fig_sprint.add_trace(go.Bar(x=sub_s["Sprint_Number"], y=sub_s["Completed_Story_Points"], name="Delivered Points", marker_color=COLORS["primary"]))
            fig_sprint.add_trace(go.Scatter(x=sub_s["Sprint_Number"], y=sub_s["Velocity"], name="Velocity", mode="lines+markers", yaxis="y2", line=dict(color=COLORS["success"], width=2.5)))
            layout_s = get_plotly_layout("Story Point Burndown vs Velocity Stability", height=360)
            layout_s["yaxis2"] = dict(title="Velocity (pts)", overlaying="y", side="right", showgrid=False)
            fig_sprint.update_layout(**layout_s, barmode="group")
            st.plotly_chart(fig_sprint, width="stretch")
        else:
            st.info("Agile burndown telemetry is not logged for non-sprint initiatives.")


if __name__ == "__main__":
    main()
