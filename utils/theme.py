"""
Centralized Theme and UI Visual Standards --- Off-White Light SaaS Aesthetic.
Provides light corporate colors, high-contrast Plotly layouts, white metric cards, and horizontal top navbar.
"""
from typing import Any, Dict
import streamlit as st

# Industry Light SaaS Palette
COLORS = {
    "primary": "#0066CC",       # Crisp Corporate Blue
    "secondary": "#2563EB",     # Royal Blue
    "background": "#F8FAFC",    # Off-White Neutral
    "card_bg": "#FFFFFF",       # Pure White Container
    "text": "#0F172A",          # Slate Obsidian Text
    "muted": "#64748B",         # Neutral Muted Grey
    "border": "#E2E8F0",        # Crisp Card Border
    
    # Functional Indicators (Clean Light Mode Contrast)
    "success": "#16A34A",       # Emerald Green
    "warning": "#D97706",       # Amber
    "danger": "#DC2626",        # Crimson Red
    "info": "#0284C7",          # Sky Blue
    
    # Practice Sectors
    "dept_ai": "#4F46E5",       # Indigo
    "dept_cloud": "#0284C7",    # Sky Slate
    "dept_data": "#059669",     # Emerald Slate
    "dept_digital": "#D97706"   # Amber Slate
}

STATUS_COLOR_MAP = {
    "Active": COLORS["info"],
    "Delayed": COLORS["warning"],
    "Completed": COLORS["success"],
    "Planned": COLORS["muted"]
}

RISK_COLOR_MAP = {
    "Low": COLORS["success"],
    "Medium": COLORS["warning"],
    "High": COLORS["danger"]
}


def get_plotly_layout(title: str = "", height: int = 360) -> Dict[str, Any]:
    """
    Returns high-density crisp light-theme Plotly layout configuration.
    """
    layout = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#334155", family="Inter, -apple-system, sans-serif", size=12),
        height=height,
        margin=dict(l=30, r=30, t=45 if title else 20, b=30),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, linecolor="#CBD5E1"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, linecolor="#CBD5E1"),
        legend=dict(bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="#E2E8F0", borderwidth=1, font=dict(size=11, color="#334155"))
    )
    
    if title:
        layout["title"] = dict(
            text=title, 
            font=dict(size=14, color="#0F172A", family="Inter, sans-serif", weight="bold"),
            x=0.0,
            xanchor="left"
        )
        
    return layout


def render_kpi_card_html(label: str, value: str, delta: str = "", delta_color: str = "normal") -> str:
    """
    Generates HTML string for a pure white industry SaaS metric card.
    """
    color = COLORS["muted"]
    if delta:
        if delta.startswith("+") or delta.startswith("▲"):
            color = COLORS["success"] if delta_color != "inverse" else COLORS["danger"]
        elif delta.startswith("-") or delta.startswith("▼"):
            color = COLORS["danger"] if delta_color != "inverse" else COLORS["success"]
            
    delta_html = f'<span style="color: {color}; font-size: 11px; font-weight: 600; font-family: \'JetBrains Mono\', monospace;">{delta}</span>' if delta else ''
    
    return f"""
    <div class="metric-container">
        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <div style="color: #64748B; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">{label}</div>
            {delta_html}
        </div>
        <div style="color: #0F172A; font-size: 24px; font-weight: 700; margin-top: 4px; font-family: 'Inter', sans-serif;">{value}</div>
    </div>
    """


def render_top_navbar():
    """
    Renders centralized horizontal top navigation links across all screens.
    Replaces left sidebar menu.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #E2E8F0;">
        <div style="font-weight: 700; font-size: 16px; color: #0F172A; letter-spacing: -0.02em;">
            <span style="color: #0066CC;">PROJECT INTELLIGENCE</span> &nbsp;<span style="color: #94A3B8; font-weight: 400;">| Enterprise PMO Suite</span>
        </div>
        <div style="font-size: 11px; font-family: 'JetBrains Mono', monospace; color: #64748B;">
            <span style="color: #16A34A;">●</span> XGBoost Telemetry Online (150 Projects)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(9)
    nav_items = [
        ("app.py", "Hub Landing"),
        ("pages/1_Executive_Dashboard.py", "Overview"),
        ("pages/2_Portfolio_View.py", "Portfolio"),
        ("pages/3_Project_Details.py", "Inspection"),
        ("pages/4_Risk_Prediction.py", "Risk Sim"),
        ("pages/5_Resource_Management.py", "Resources"),
        ("pages/6_Sprint_Analytics.py", "Sprints"),
        ("pages/7_Budget_Analytics.py", "Financials"),
        ("pages/8_AI_Executive_Insights.py", "Briefing"),
    ]
    
    for col, (path, label) in zip(cols, nav_items):
        with col:
            st.page_link(path, label=label, width="stretch")
            
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
