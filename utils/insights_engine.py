"""
AI Executive Insights Rule-Based Engine.
Analyzes portfolio datasets to generate executive summaries, risk alerts, financial concerns, 
resource bottlenecks, and strategic recommendations. Designed with strict abstraction boundaries 
for future drop-in LLM replacement.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseInsightsEngine(ABC):
    """
    Abstract interface for AI Insights Generation.
    Allows swapping rule-based heuristics for GenAI LLM models (OpenAI/Gemini) later.
    """
    @abstractmethod
    def generate_insights(self, df_projects: pd.DataFrame, df_employees: pd.DataFrame, df_sprints: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes enterprise datasets and returns structured executive insights.
        """
        pass


class RuleBasedInsightsEngine(BaseInsightsEngine):
    """
    Deterministic enterprise heuristic engine simulating AI consulting intelligence.
    """
    def generate_insights(self, df_projects: pd.DataFrame, df_employees: pd.DataFrame, df_sprints: pd.DataFrame) -> Dict[str, Any]:
        logger.info("Executing rule-based AI intelligence engine scanning portfolio anomalies...")
        
        total_projects = len(df_projects)
        active_projects = len(df_projects[df_projects["Status"] == "Active"])
        delayed_projects = len(df_projects[df_projects["Status"] == "Delayed"])
        completed_projects = len(df_projects[df_projects["Status"] == "Completed"])
        
        total_budget = df_projects["Budget"].sum()
        total_cost = df_projects["Actual_Cost"].sum()
        avg_health = df_projects["Health_Score"].mean()
        
        delayed_pct = (delayed_projects / total_projects * 100) if total_projects > 0 else 0
        
        # 1. Weekly Summary
        summary = (
            f"The Enterprise PMO Portfolio currently monitors {total_projects} digital transformation initiatives "
            f"with an aggregate committed budget of ${total_budget:,.0f}. Overall portfolio health stands at "
            f"{avg_health:.1f}/100. While {completed_projects} projects have successfully delivered, {delayed_projects} initiatives "
            f"({delayed_pct:.1f}%) are experiencing schedule slippage or cost headwinds requiring executive intervention."
        )
        
        # 2. High-risk Projects
        high_risk_df = df_projects[(df_projects["Risk"] == "High") | (df_projects["Health_Score"] < 60)].copy()
        high_risk_list = []
        for _, row in high_risk_df.iterrows():
            drivers = []
            if row["Status"] == "Delayed":
                drivers.append(f"Behind schedule ({row['Remaining_Days']} remaining days)")
            if row["Open_Bugs"] > 10:
                drivers.append(f"High defect backlog ({row['Open_Bugs']} bugs)")
            if row["Actual_Cost"] > row["Budget"]:
                drivers.append(f"Cost overrun (+${row['Actual_Cost'] - row['Budget']:,.0f})")
                
            high_risk_list.append({
                "id": row["Project_ID"],
                "name": row["Project_Name"],
                "manager": row["Manager"],
                "health": row["Health_Score"],
                "drivers": ", ".join(drivers) if drivers else "Compound governance friction"
            })
            
        # 3. Budget Concerns
        overrun_df = df_projects[df_projects["Actual_Cost"] > df_projects["Budget"]].copy()
        budget_concerns = []
        total_overrun_exposure = 0.0
        for _, row in overrun_df.iterrows():
            variance = row["Actual_Cost"] - row["Budget"]
            total_overrun_exposure += variance
            budget_concerns.append({
                "name": row["Project_Name"],
                "dept": row["Department"],
                "budget": row["Budget"],
                "actual": row["Actual_Cost"],
                "overrun": variance
            })
            
        # 4. Resource Bottlenecks
        bottlenecks = []
        if not df_projects.empty and "Team_Utilization" in df_projects.columns:
            overworked_depts = df_projects.groupby("Department")["Team_Utilization"].mean().reset_index()
            for _, row in overworked_depts.iterrows():
                if row["Team_Utilization"] > 88.0:
                    bottlenecks.append({
                        "department": row["Department"],
                        "utilization": round(row["Team_Utilization"], 1),
                        "alert": f"Critical talent saturation ({row['Team_Utilization']:.1f}% avg load). High burnout & delivery risk."
                    })
                    
        # 5. Executive Recommendations
        recommendations = []
        if delayed_projects > 0:
            recommendations.append(
                f"Mandate weekly steering syncs for the {delayed_projects} delayed initiatives to unblock cross-functional dependencies."
            )
        if total_overrun_exposure > 0:
            recommendations.append(
                f"Execute immediate financial audit on highlighted budget concerns to contain ${total_overrun_exposure:,.0f} aggregate cost variance."
            )
        if len(high_risk_list) > 0:
            top_risk = high_risk_list[0]["name"]
            recommendations.append(
                f"Deploy specialized QA and Cloud DevOps tiger team to stabilize `{top_risk}`."
            )
        if len(bottlenecks) > 0:
            recommendations.append(
                "Pause new planned project kickoffs in saturated departments to protect active sprint burndown trajectories."
            )
        if not recommendations:
            recommendations.append("Portfolio governance metrics align with nominal enterprise delivery thresholds. Maintain standard sprint cadences.")

        return {
            "summary": summary,
            "high_risk_projects": high_risk_list,
            "budget_concerns": {
                "list": budget_concerns,
                "total_exposure": total_overrun_exposure
            },
            "resource_bottlenecks": bottlenecks,
            "recommendations": recommendations
        }


def get_insights_engine() -> BaseInsightsEngine:
    """
    Factory function returning active insights engine.
    """
    return RuleBasedInsightsEngine()
