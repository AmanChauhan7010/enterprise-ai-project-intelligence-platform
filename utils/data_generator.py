"""
Correlated Synthetic Enterprise Dataset Generator.
Generates realistic consulting PMO datasets with strict mathematical and business logic correlations.
Targets precise dataset sizes: Projects=150, Employees=560, Sprints=900, Meetings=3800.
"""
import os
import random
from typing import Tuple
import pandas as pd
import numpy as np
from faker import Faker
from utils.health_scorer import compute_project_health, categorize_health
from utils.logger import get_logger

logger = get_logger(__name__)
fake = Faker()

DEPARTMENTS = [
    "AI & Automation",
    "Cloud Infrastructure",
    "Data Engineering",
    "Digital Transformation"
]

TECH_STACK_MAP = {
    "AI & Automation": ["PyTorch & LLM Engine", "Computer Vision Platform", "Agentic AI Orchestrator", "GenAI Enterprise Assistant", "Predictive Analytics Core"],
    "Cloud Infrastructure": ["AWS EKS Multi-Region", "Azure Landing Zone Core", "Multi-Cloud Terraform Mesh", "GCP Vertex Cloud Ops", "Serverless Event Grid"],
    "Data Engineering": ["Databricks Lakehouse Core", "Snowflake Realtime ETL", "Apache Kafka Streaming", "dbt Analytics Mesh", "Airflow Governance Sync"],
    "Digital Transformation": ["Next.js Micro-Frontend", "React Native Omni-App", "Salesforce Enterprise Sync", "SAP S/4HANA Core Modernization", "API Gateway Zero-Trust"]
}

MANAGERS = [
    "Sarah Jenkins (Director)", "Marcus Vance (Sr. Manager)", "Elena Rostova (Principal Lead)", 
    "David Kim (Delivery VP)", "Priya Patel (PMO Lead)", "Arthur Pendelton (Director)", 
    "Rachel Green (Sr. Manager)", "Liam O'Connor (Principal Architect)",
    "Jonathan Sterling (Practice Lead)", "Michelle Chang (Director)", "Alexander Wright (VP Delivery)",
    "Sophia Al-Mansoor (Sr. Manager)", "Benjamin Hayes (Principal Architect)"
]

CLIENTS = [
    "Apex Financial Group", "Global Health Biosciences", "Horizon Retail Enterprises", 
    "Vanguard Logistics International", "Sterling Telecom Corp", "Nexus Renewable Energy", 
    "Pinnacle Mutual Insurance", "Quantum Aerospace Dynamics", "Centurion Capital Partners",
    "Prism Media International", "Oceana Global Shipping", "Hyperion Semiconductor Corp"
]


def generate_enterprise_datasets(
    num_projects: int = 150,
    target_employees: int = 560,
    target_sprints: int = 900,
    target_meetings: int = 3800,
    seed: int = 42,
    output_dir: str = "data"
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Generates correlated enterprise PMO datasets and persists them to CSV.
    Guarantees exact target counts for enterprise scalability benchmarking.
    """
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)
    
    logger.info(f"Simulating {num_projects} enterprise projects with correlated metrics...")
    
    projects_data = []
    
    for i in range(1, num_projects + 1):
        proj_id = f"PRJ-{1000 + i}"
        dept = random.choice(DEPARTMENTS)
        tech = random.choice(TECH_STACK_MAP[dept])
        client = random.choice(CLIENTS)
        manager = random.choice(MANAGERS)
        
        # Determine Project Archetype
        rand_val = random.random()
        if rand_val < 0.20:
            archetype = "completed"
        elif rand_val < 0.35:
            archetype = "planned"
        elif rand_val < 0.72:
            archetype = "healthy_active"
        else:
            archetype = "struggling_delayed"
            
        budget = round(random.uniform(150000, 1450000), -2)
        team_size = random.randint(4, 16)
        
        if archetype == "completed":
            status = "Completed"
            progress = 100.0
            actual_cost = round(budget * random.uniform(0.92, 1.04), -2)
            open_bugs = 0
            sprint_velocity = round(random.uniform(34, 55), 1)
            remaining_days = 0
            risk_level = "Low"
            team_util = round(random.uniform(78, 86), 1)
            start_date = fake.date_between(start_date="-240d", end_date="-90d")
            end_date = fake.date_between(start_date="-45d", end_date="-5d")
            
        elif archetype == "planned":
            status = "Planned"
            progress = 0.0
            actual_cost = 0.0
            open_bugs = 0
            sprint_velocity = round(random.uniform(28, 42), 1)
            remaining_days = random.randint(60, 220)
            risk_level = "Low"
            team_util = 0.0
            start_date = fake.date_between(start_date="+15d", end_date="+60d")
            end_date = fake.date_between(start_date="+120d", end_date="+280d")
            
        elif archetype == "healthy_active":
            status = "Active"
            progress = round(random.uniform(32.0, 89.0), 1)
            actual_cost = round(budget * (progress / 100.0) * random.uniform(0.95, 1.06), -2)
            open_bugs = random.randint(0, 4)
            sprint_velocity = round(random.uniform(32, 50), 1)
            remaining_days = random.randint(25, 140)
            risk_level = "Low" if open_bugs <= 2 else "Medium"
            team_util = round(random.uniform(77, 87), 1)
            start_date = fake.date_between(start_date="-150d", end_date="-25d")
            end_date = fake.date_between(start_date="+25d", end_date="+160d")
            
        else: # struggling_delayed
            status = "Delayed"
            progress = round(random.uniform(15.0, 60.0), 1)
            actual_cost = round(budget * (progress / 100.0) * random.uniform(1.35, 1.80), -2)
            open_bugs = random.randint(9, 28)
            sprint_velocity = round(random.uniform(12, 24), 1)
            remaining_days = random.randint(-30, 12)
            risk_level = "High" if open_bugs > 14 or actual_cost > budget else "Medium"
            team_util = round(random.uniform(93, 99.5), 1)
            start_date = fake.date_between(start_date="-180d", end_date="-50d")
            end_date = fake.date_between(start_date="-20d", end_date="+15d")

        proj_record = {
            "Project_ID": proj_id,
            "Project_Name": f"{client.split()[0]} {tech.split()[0]} Transformation",
            "Client": client,
            "Department": dept,
            "Technology": tech,
            "Manager": manager,
            "Status": status,
            "Risk": risk_level,
            "Budget": budget,
            "Actual_Cost": actual_cost,
            "Progress": progress,
            "Sprint_Velocity": sprint_velocity,
            "Team_Size": team_size,
            "Open_Bugs": open_bugs,
            "Remaining_Days": remaining_days,
            "Team_Utilization": team_util,
            "Start_Date": str(start_date),
            "End_Date": str(end_date)
        }
        
        health_score = compute_project_health(proj_record)
        proj_record["Health_Score"] = health_score
        proj_record["Health_Category"] = categorize_health(health_score)
        
        projects_data.append(proj_record)
        
    df_projects = pd.DataFrame(projects_data)
    
    # 2. Generate Exactly 560 Employees
    logger.info(f"Generating exactly {target_employees} employee allocation records...")
    roles = [
        "Principal Enterprise Architect", "Senior Data Scientist", "Senior Python Engineer", 
        "Lead ML Engineer", "Senior DevOps Engineer", "PMO Consultant", "QA Automation Lead", 
        "Full Stack UI/UX Lead", "Cloud Solutions Architect", "Data Engineer",
        "Analytics Engineer", "Site Reliability Engineer", "Security Architect"
    ]
    
    employees_data = []
    emp_id_counter = 5001
    
    # Cycle through projects to distribute exactly target_employees
    while len(employees_data) < target_employees:
        for p in projects_data:
            if len(employees_data) >= target_employees:
                break
            role = random.choice(roles)
            alloc = random.choice([50, 75, 100]) if p["Status"] != "Planned" else 25
            avail = 100 - alloc
            rate = random.choice([115, 135, 155, 175, 195, 225, 250])
            
            employees_data.append({
                "Employee_ID": f"EMP-{emp_id_counter}",
                "Name": fake.name(),
                "Role": role,
                "Department": p["Department"],
                "Assigned_Project_ID": p["Project_ID"],
                "Assigned_Project_Name": p["Project_Name"],
                "Allocation_Pct": alloc,
                "Availability_Pct": avail,
                "Hourly_Rate_USD": rate
            })
            emp_id_counter += 1
            
    df_employees = pd.DataFrame(employees_data)
    
    # 3. Generate Exactly 900 Sprint Records
    logger.info(f"Generating exactly {target_sprints} sprint burndown records...")
    sprints_data = []
    sprint_id_counter = 1
    eligible_projects = [p for p in projects_data if p["Status"] != "Planned"]
    
    while len(sprints_data) < target_sprints:
        for p in eligible_projects:
            if len(sprints_data) >= target_sprints:
                break
            
            # Determine current sprint number for this project
            existing_count = sum(1 for s in sprints_data if s["Project_ID"] == p["Project_ID"])
            s_num = existing_count + 1
            
            planned_pts = random.randint(35, 65)
            
            if p["Status"] == "Completed":
                completed_pts = planned_pts + random.randint(-2, 4)
                bugs_raised = random.randint(1, 3)
                bugs_res = bugs_raised
                vel = p["Sprint_Velocity"] + random.uniform(-2, 3)
            elif p["Status"] == "Active":
                completed_pts = max(12, planned_pts + random.randint(-5, 2))
                bugs_raised = random.randint(1, 4)
                bugs_res = max(0, bugs_raised - random.randint(0, 1))
                vel = p["Sprint_Velocity"] + random.uniform(-3, 3)
            else: # Delayed
                decay = s_num * 2.5
                completed_pts = max(10, int(planned_pts - decay - random.randint(2, 6)))
                bugs_raised = random.randint(4, 9)
                bugs_res = max(1, bugs_raised - random.randint(2, 4))
                vel = max(10.0, p["Sprint_Velocity"] - (s_num * 1.2))
                
            completion_rate = round((completed_pts / planned_pts) * 100, 1) if planned_pts > 0 else 0.0
            
            sprints_data.append({
                "Sprint_ID": f"SPT-{sprint_id_counter:04d}",
                "Project_ID": p["Project_ID"],
                "Sprint_Number": f"Sprint {s_num}",
                "Planned_Story_Points": planned_pts,
                "Completed_Story_Points": completed_pts,
                "Completion_Rate_Pct": completion_rate,
                "Velocity": round(vel, 1),
                "Bugs_Raised": bugs_raised,
                "Bugs_Resolved": bugs_res,
                "Open_Defects_Accumulated": max(0, bugs_raised - bugs_res)
            })
            sprint_id_counter += 1
            
    df_sprints = pd.DataFrame(sprints_data)
    
    # 4. Generate Exactly 3800 Meeting Logs
    logger.info(f"Generating exactly {target_meetings} governance meeting logs...")
    meeting_types = ["Sprint Review & Demo", "Steering Committee Sync", "Architecture Review Board", "Risk & Mitigation Board", "Financial Burn Review", "Security Audit Sync"]
    meetings_data = []
    mtg_id_counter = 10001
    
    while len(meetings_data) < target_meetings:
        for p in eligible_projects:
            if len(meetings_data) >= target_meetings:
                break
            m_type = random.choice(meeting_types)
            open_actions = random.randint(1, 6) if p["Status"] == "Delayed" else random.randint(0, 2)
            
            meetings_data.append({
                "Meeting_ID": f"MTG-{mtg_id_counter}",
                "Project_ID": p["Project_ID"],
                "Meeting_Date": str(fake.date_between(start_date="-120d", end_date="today")),
                "Meeting_Type": m_type,
                "Attendees_Count": random.randint(4, 14),
                "Key_Decisions_Logged": fake.sentence(nb_words=9),
                "Open_Action_Items": open_actions
            })
            mtg_id_counter += 1
            
    df_meetings = pd.DataFrame(meetings_data)
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        df_projects.to_csv(f"{output_dir}/projects.csv", index=False)
        df_employees.to_csv(f"{output_dir}/employees.csv", index=False)
        df_sprints.to_csv(f"{output_dir}/sprints.csv", index=False)
        df_meetings.to_csv(f"{output_dir}/meetings.csv", index=False)
    
    logger.info(f"Generated successfully: Projects={len(df_projects)}, Employees={len(df_employees)}, Sprints={len(df_sprints)}, Meetings={len(df_meetings)}.")
    return df_projects, df_employees, df_sprints, df_meetings


if __name__ == "__main__":
    generate_enterprise_datasets()
