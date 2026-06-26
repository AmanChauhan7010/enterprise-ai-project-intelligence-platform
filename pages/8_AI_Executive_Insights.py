"""
Executive Briefing Room --- Heuristic Portfolio Risk Synthesis & Remediation Directives.
Refined Off-White Light SaaS corporate UI.
"""
import os
import streamlit as st
import pandas as pd
from utils.logger import get_logger
from utils.insights_engine import get_insights_engine
from utils.theme import render_top_navbar

logger = get_logger(__name__)

st.set_page_config(page_title="Executive Briefing | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def load_all_datasets():
    if not os.path.exists("data/projects.csv"):
        from utils.data_generator import generate_enterprise_datasets
        generate_enterprise_datasets()
    return (
        pd.read_csv("data/projects.csv"),
        pd.read_csv("data/employees.csv"),
        pd.read_csv("data/sprints.csv")
    )


def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 20px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: baseline;">
        <div>
            <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Executive Portfolio Synthesis</h1>
            <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
                Heuristic risk red flags, commercial variance exposure, and actionable remediation directives.
            </p>
        </div>
        <div>
            <span style="background-color: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; font-family: 'JetBrains Mono', monospace;">
                HEURISTIC ENGINE v1.0
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    render_top_navbar()
    df_p, df_e, df_s = load_all_datasets()
    render_header()

    engine = get_insights_engine()
    insights = engine.generate_insights(df_p, df_e, df_s)

    st.markdown(f"""
    <div class="industry-panel" style="margin-bottom: 28px; border-left: 4px solid #0066CC;">
        <div style="color: #0066CC; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-family: 'JetBrains Mono', monospace;">Governance Briefing</div>
        <div style="font-size: 15px; line-height: 1.6; color: #0F172A;">{insights['summary']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 14px;'>Strategic Governance Interventions</div>", unsafe_allow_html=True)
    
    for i, rec in enumerate(insights["recommendations"], 1):
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; display: flex; align-items: center; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
            <div style="background-color: #EFF6FF; color: #1D4ED8; width: 26px; height: 26px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 12px; margin-right: 14px; font-family: 'JetBrains Mono', monospace; flex-shrink: 0;">{i:02d}</div>
            <div style="font-size: 13px; color: #1E293B; line-height: 1.4;">{rec}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)

    col_risk, col_fin = st.columns(2)

    with col_risk:
        st.markdown("<div style='font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 12px;'>High-Risk Transformation Anomalies</div>", unsafe_allow_html=True)
        high_risks = insights["high_risk_projects"]
        if high_risks:
            for hr in high_risks[:6]:
                with st.expander(f"[{hr['id']}] : {hr['name']} (Index: {hr['health']}/100)", expanded=True):
                    st.markdown(f"**Practice Director**: `{hr['manager']}`")
                    st.markdown(f"**Governance Drivers**:\n- {hr['drivers']}")
        else:
            st.success("No critical high-risk project anomalies detected across active inventories.")

    with col_fin:
        bc = insights["budget_concerns"]
        st.markdown(f"<div style='font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 12px;'>Financial Overrun Ledgers (+${bc['total_exposure']:,.0f} var)</div>", unsafe_allow_html=True)
        if bc["list"]:
            df_bc = pd.DataFrame(bc["list"])
            df_bc["overrun"] = df_bc["overrun"].apply(lambda x: f"+${x:,.0f}")
            df_bc["budget"] = df_bc["budget"].apply(lambda x: f"${x:,.0f}")
            df_bc["actual"] = df_bc["actual"].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(
                df_bc,
                width="stretch",
                hide_index=True,
                column_config={
                    "name": "Initiative",
                    "dept": "Practice",
                    "budget": "Baseline",
                    "actual": "Spend",
                    "overrun": "Variance"
                }
            )
        else:
            st.success("All transformation project spends align within approved financial baseline authorization.")

    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 10px;'>Practice Capacity Saturation Protocols</div>", unsafe_allow_html=True)
    bottlenecks = insights["resource_bottlenecks"]
    if bottlenecks:
        for b in bottlenecks:
            st.warning(f"**{b['department']} Practice Sector**: {b['alert']}")
    else:
        st.info("Departmental resource utilization rates remain balanced across consulting practices.")


if __name__ == "__main__":
    main()
