"""
Portfolio View --- Interactive Searchable Table with Multi-Dimensional Filtering & Export.
Refined Off-White Light SaaS corporate UI.
"""
import os
import io
import streamlit as st
import pandas as pd
from utils.logger import get_logger
from utils.theme import render_top_navbar

logger = get_logger(__name__)

st.set_page_config(page_title="Portfolio Inventory | PMO Intelligence", layout="wide", initial_sidebar_state="collapsed")


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
        <h1 style="margin: 0; font-size: 24px; color: #0F172A; font-weight: 700;">Portfolio Inventory Ledger</h1>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Comprehensive corporate repository with quantitative filtering across 150 practice initiatives.
        </p>
    </div>
    """, unsafe_allow_html=True)


def convert_df_to_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Portfolio")
    return output.getvalue()


def main():
    render_top_navbar()
    df = load_data()
    render_header()
    
    with st.expander("Diagnostic Filtering & Search Parameters", expanded=True):
        search_query = st.text_input("Query String (Matches ID, Initiative Name, or Client Entity)", placeholder="e.g. PRJ-1045 or Apex or Databricks")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            clients = st.multiselect("Client Entity", options=sorted(df["Client"].unique()), default=[])
        with c2:
            technologies = st.multiselect("Technology Mesh", options=sorted(df["Technology"].unique()), default=[])
        with c3:
            managers = st.multiselect("Practice Director", options=sorted(df["Manager"].unique()), default=[])
        with c4:
            risks = st.multiselect("Risk Profile", options=["Low", "Medium", "High"], default=[])
        with c5:
            statuses = st.multiselect("Operational State", options=["Active", "Delayed", "Completed", "Planned"], default=[])

    filtered_df = df.copy()
    
    if search_query:
        query_lower = search_query.lower()
        filtered_df = filtered_df[
            filtered_df["Project_ID"].str.lower().str.contains(query_lower) |
            filtered_df["Project_Name"].str.lower().str.contains(query_lower) |
            filtered_df["Client"].str.lower().str.contains(query_lower)
        ]
        
    if clients:
        filtered_df = filtered_df[filtered_df["Client"].isin(clients)]
    if technologies:
        filtered_df = filtered_df[filtered_df["Technology"].isin(technologies)]
    if managers:
        filtered_df = filtered_df[filtered_df["Manager"].isin(managers)]
    if risks:
        filtered_df = filtered_df[filtered_df["Risk"].isin(risks)]
    if statuses:
        filtered_df = filtered_df[filtered_df["Status"].isin(statuses)]

    st.markdown("<div style='margin: 16px 0 8px 0; font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;'>Filtered Telemetry Index</div>", unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Initiatives Mapped", f"{len(filtered_df)}")
    with kpi2:
        st.metric("Aggregate Budget", f"${filtered_df['Budget'].sum()/1e6:.2f}M")
    with kpi3:
        st.metric("Actual Spend", f"${filtered_df['Actual_Cost'].sum()/1e6:.2f}M")
    with kpi4:
        avg_h = filtered_df['Health_Score'].mean() if not filtered_df.empty else 0
        st.metric("Weighted Health", f"{avg_h:.1f}")

    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
    
    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True,
        height=520,
        column_config={
            "Project_ID": st.column_config.TextColumn("ID", width="small"),
            "Project_Name": st.column_config.TextColumn("Initiative Title", width="medium"),
            "Department": st.column_config.TextColumn("Practice Sector", width="small"),
            "Budget": st.column_config.NumberColumn("Baseline ($)", format="$%d"),
            "Actual_Cost": st.column_config.NumberColumn("Spend ($)", format="$%d"),
            "Progress": st.column_config.ProgressColumn("Milestone (%)", format="%.1f%%", min_value=0, max_value=100),
            "Health_Score": st.column_config.NumberColumn("Index", format="%d")
        }
    )

    st.markdown("---")
    col_dl1, col_dl2, _ = st.columns([1.5, 1.5, 7])
    
    with col_dl1:
        csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV Ledger",
            data=csv_bytes,
            file_name="pmo_portfolio_export.csv",
            mime="text/csv",
            width="stretch"
        )
        
    with col_dl2:
        excel_bytes = convert_df_to_excel(filtered_df)
        st.download_button(
            label="Export Excel Workbook",
            data=excel_bytes,
            file_name="pmo_portfolio_export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch"
        )


if __name__ == "__main__":
    main()
