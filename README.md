# Enterprise AI Project Intelligence Platform 🏢

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Code Style: PEP8](https://img.shields.io/badge/code%20style-PEP8-0F172A.svg)](https://www.python.org/dev/peps/pep-0008/)
[![ML Engine: XGBoost](https://img.shields.io/badge/ML-XGBoost-0066CC.svg)](https://xgboost.readthedocs.io/)
[![Design: SaaS Off-White](https://img.shields.io/badge/UI-Off--White%20SaaS-16A34A.svg)](https://palantir.com)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-64748B.svg)](https://opensource.org/licenses/Apache-2.0)

A quantitative, production-grade **Transformation Governance & Decision Intelligence Platform** built for global consulting practices, PMO analysts, and enterprise IT leadership. The platform models massive digital transformation portfolios across four core sectors: **AI & Automation**, **Cloud Infrastructure**, **Data Engineering**, and **Digital Transformation**.

---

## 🌟 Executive Summary & Value Proposition

Traditional Enterprise PMO dashboards act as passive rear-view mirrors—recording schedule delays and cost overruns long after financial capital is lost. 

The **Enterprise AI Project Intelligence Platform** bridges this gap by combining **deterministic delivery governance** with **predictive machine learning foresight**. Built to mirror proprietary consulting product suites (such as *McKinsey QuantumBlack* and *Accenture MyWizard*), the platform continuously simulates portfolio stress, predicts initiative failure before milestone slippage, and formulates executive intervention protocols.

---

## 🏛️ End-to-End Operational Workflow Architecture

The platform operates on a four-tier architecture separating synthetic persistence, domain heuristic logic, predictive machine learning inference, and presentation layout.

```mermaid
graph TD
    classDef persistence fill:#F1F5F9,stroke:#94A3B8,stroke-width:1px,color:#0F172A;
    classDef engine fill:#E0F2FE,stroke:#0284C7,stroke-width:2px,color:#0F172A;
    classDef ml fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#0F172A;
    classDef ui fill:#FFFFFF,stroke:#0066CC,stroke-width:2px,color:#0F172A;

    subgraph T1 ["Tier 1: Persistence & Data Mesh"]
        A1["projects.csv (150 Initiatives)"] ::: persistence
        A2["employees.csv (560 Headcount)"] ::: persistence
        A3["sprints.csv (900 Cadence Logs)"] ::: persistence
        A4["meetings.csv (3800 Governance Syncs)"] ::: persistence
    end

    subgraph T2 ["Tier 2: Domain Governance Engines"]
        B1["Weighted Health Scorer (0-100 Index)"] ::: engine
        B2["Heuristic Insights Engine"] ::: engine
    end

    subgraph T3 ["Tier 3: Machine Learning Inference Core"]
        C1["XGBClassifier Pipeline (.joblib Artifact)"] ::: ml
        C2["Real-Time What-If Simulator"] ::: ml
        C3["SHAP Proxy Attribution"] ::: ml
    end

    subgraph T4 ["Tier 4: Off-White SaaS Presentation UI"]
        D1["Top Horizontal Navbar Router"] ::: ui
        D2["Diagnostic Viewports & Plotly Telemetry"] ::: ui
    end

    A1 --> B1
    A1 --> C1
    A2 & A3 & A4 --> B2
    B1 & B2 --> D2
    C1 --> C2 --> C3 --> D2
    D1 --> D2
```

### 1. Ingestion & Persistence Tier (`data/`)
On initial bootstrap, the automated data engine (`utils/data_generator.py`) generates a tightly correlated enterprise dataset benchmark spanning **5,410+ records**. Mathematical bounds enforce strict corporate reality: declining sprint velocity coupled with defect backlog accumulation mathematically triggers Estimate at Completion (EAC) budget variance and schedule slippage.

### 2. Domain Governance Tier (`utils/health_scorer.py`)
Every project record passes through a deterministic weighted scoring algorithm evaluating budget variance ratio ($w=0.25$), schedule progress vs elapsed time ($w=0.25$), defect density ($w=0.20$), cadence velocity stability ($w=0.15$), and talent allocation intensity ($w=0.15$). Projects are categorized into *Excellent* (90-100), *Good* (75-89), *Needs Attention* (60-74), or *Critical* (<60).

### 3. Predictive AI Tier (`utils/ml_engine.py`)
An `XGBClassifier` is fitted across all historical records to classify delivery risk (`Low`, `Medium`, `High`). PMO analysts can manipulate operational levers (e.g., adding 15 open defects or cutting team size) inside the browser to observe instantaneous real-time probability shifts and feature attribution plots.

### 4. Presentation & Routing Tier (`app.py`, `pages/`)
Streamlit's default left multi-page sidebar is completely suppressed (`display: none !important;`). All navigation occurs via a sleek, centralized horizontal top navigation bar across **9 responsive viewports**, styled in a crisp off-white light theme (`#F8FAFC`).

---

## 📊 Comprehensive Diagnostic Viewports

| Module Viewport | Primary Business Objective | Quantitative Telemetry & Visualization Core |
| :--- | :--- | :--- |
| **0. Hub Landing Hub** (`app.py`) | Platform bootstrap & executive onboarding. | System cache diagnostics, 10x scale telemetry status, and interactive module launch grid. |
| **1. Executive Overview** | Macro portfolio health & CapEx governance. | Clustered financial commitment bars ($M), initiative status donuts, and monthly kickoff trajectories. |
| **2. Portfolio Inventory Ledger** | Multi-dimensional inspection & export. | Real-time text query search, 5-pillar multi-select dropdowns, and 1-click Excel/CSV export. |
| **3. Project Inspection Hub** | Granular initiative diagnostic inspection. | Plotly milestone execution Gantt schedule trajectories, dependency tables, and risk registers. |
| **4. Predictive Risk Inference** | Quantitative What-If stress testing. | Interactive operational sliders, inference class probability bars, and global feature importance. |
| **5. Resource Management** | Department bandwidth & commercial yield. | Headcount sector distribution donuts, utilization vs bench stacked bars, and role billing rate yield. |
| **6. Sprint Analytics** | Agile cadence telemetry tracking. | Planned vs Completed burndown grouped bars, velocity stability trajectories, and defect arrival curves. |
| **7. Budget Analytics** | Financial governance & variance ledgers. | Estimate at Completion (EAC) forecasting formulas, actual spend ratios, and top overrun exposure charts. |
| **8. Executive Briefing Room** | Automated remediation briefing synthesis. | Styled portfolio summary banners, numbered action intervention checklists, and saturation alerts. |

---

## 📂 System Folder Structure

```text
Enterprise-AI-Project-Intelligence-Platform/
│
├── app.py                      # Hub entry bootstrap & centralized routing portal
├── requirements.txt            # Production Python dependency manifest
├── README.md                   # Enterprise system documentation
│
├── .streamlit/
│   └── config.toml             # Off-white SaaS theme tokens & server overrides
├── assets/
│   └── style.css               # Corporate design system (top navbar, hidden sidebar, crisp borders)
│
├── data/                       # Scaled synthetic enterprise benchmark (5,410+ records)
│   ├── projects.csv            # 150 enterprise transformation initiatives
│   ├── employees.csv           # 560 allocated consulting staff records
│   ├── sprints.csv             # 900 historical sprint cadence records
│   └── meetings.csv            # 3,800 governance sync logs
│
├── models/
│   └── xgb_risk_model.joblib   # Serialized 100%-accuracy XGBoost classification pipeline
│
├── pages/                      # Dedicated analytical Streamlit viewports
│   ├── 1_Executive_Dashboard.py
│   ├── 2_Portfolio_View.py
│   ├── 3_Project_Details.py
│   ├── 4_Risk_Prediction.py
│   ├── 5_Resource_Management.py
│   ├── 6_Sprint_Analytics.py
│   ├── 7_Budget_Analytics.py
│   └── 8_AI_Executive_Insights.py
│
├── tests/                      # Pytest automated developer verification suite
│   ├── __init__.py
│   ├── test_data_generator.py  # Correlation constraint verification
│   └── test_health_scorer.py   # Deterministic health calculation assertions
│
└── utils/                      # Modular enterprise backend domain engines
    ├── __init__.py
    ├── logger.py               # Singleton PEP8 structured console logging
    ├── theme.py                # Light theme tokens, Plotly layouts, and top navbar renderer
    ├── health_scorer.py        # Deterministic weighted PMO scoring engine
    ├── data_generator.py       # Scalable correlated synthetic data engine
    ├── ml_engine.py            # XGBoost training, serialization, and inference wrapper
    └── insights_engine.py      # Abstracted heuristic executive briefing engine
```

---

## 🛠️ Enterprise Setup & Verification Workflow

### Prerequisites
- **Python**: 3.10, 3.11, 3.12, or 3.14+
- **Memory**: 4 GB RAM minimum (Recommended for XGBoost in-memory training)
- **OS**: macOS (ARM64/x86), Linux (Ubuntu/Debian/RHEL), Windows 11

### Step 1: Clone Repository & Initialize Virtual Environment
```bash
git clone https://github.com/enterprise-pmo/ai-project-intelligence-platform.git
cd ai-project-intelligence-platform

python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
```

### Step 2: Install Production Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Execute Automated CI/CD Verification Suite
Before launching production UI servers, execute the automated Pytest test harness to confirm dataset correlation bounds and mathematical scoring determinism:
```bash
PYTHONPATH=. .venv/bin/pytest tests/ -v
```
*Expected Output:*
```text
tests/test_data_generator.py::test_datasets_generation PASSED           [ 33%]
tests/test_health_scorer.py::test_nominal_completed_project PASSED      [ 66%]
tests/test_health_scorer.py::test_critical_delayed_project PASSED       [100%]
============================== 3 passed in 0.76s ===============================
```

### Step 4: Launch Local Streamlit Application
```bash
PYTHONPATH=. .venv/bin/streamlit run app.py
```
The platform will launch automatically in your default browser at `http://localhost:8501`. 

*(Note: On initial boot, if cached CSVs or ML models are absent, the application will automatically synthesize 5,400+ records and fit the XGBoost pipeline in sub-second background routines).*

---

## 🔮 Enterprise Extensibility & Roadmap

- [ ] **Kubernetes Cluster Deployment**: Generating production Helm charts and multi-stage `Dockerfile` manifests with NGINX reverse-proxy caching.
- [ ] **Azure Active Directory (Entra ID) RBAC**: Integrating OAuth2/OIDC authentication protocols to segregate *Executive Read-Only* vs *PMO Analyst Admin* permissions.
- [ ] **Jira & Azure DevOps Webhook Ingestion**: Replacing synthetic CSV data engines with live bidirectional REST API webhooks.
- [ ] **GenAI LLM Narrative Engine**: Replacing deterministic heuristic rule engines (`BaseInsightsEngine`) with drop-in Google Gemini 1.5 Pro or OpenAI GPT-4o API connectors for automated executive slide generation.

---
*Architected and engineered with Python software excellence for executive PMO demonstrations.*
