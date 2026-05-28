# VP, Artificial Intelligence — First 90 Days
## Bryan Shaw | Concentra | Addison, TX

> *This plan is designed to be presented in a final-round interview as a demonstration of strategic thinking, healthcare AI knowledge, and executive readiness. It is built on what is publicly known about Concentra — it will be refined with internal data once in the role.*

---

## Governing Philosophy for This Role

**Governance first. Pilots second. Scale third.**

AI deployed without governance in a clinical environment is not a productivity tool — it's a liability. The first 90 days establish the framework that makes every subsequent AI initiative trustworthy, defensible, and scalable. Pilots demonstrate value. Governance makes them repeatable. The goal at 90 days is not the most AI — it is the right foundation.

---

## Phase 1: Discovery & Landscape (Days 1–30)

### Objective
Develop a complete, honest picture of Concentra's AI readiness, data infrastructure, clinical workflows, regulatory posture, and organizational appetite for AI — before making any strategy recommendations.

### Stakeholder Meetings (First 30 Days)

| Stakeholder | Meeting Focus |
|-------------|---------------|
| CMO / Chief Medical Officer | Clinical workflow understanding; patient safety philosophy; AI risk appetite in clinical settings |
| CIO / CTO | Current technology stack; data architecture; existing AI initiatives; integration constraints |
| CDO / Data Organization | Data quality; data governance maturity; data access and consent frameworks |
| Chief Compliance Officer | HIPAA program maturity; current audit processes; AI regulatory risk concerns |
| COO | Operational efficiency priorities; workflow bottlenecks; employer relationship management |
| Revenue Cycle Leadership | Billing system architecture; coding accuracy challenges; denial management processes |
| Workforce Management Leadership | Scheduling systems; staffing model; workforce analytics current state |
| Clinical Operations Leaders (center level) | Day-in-the-life clinical workflow; current pain points; technology friction |
| Legal Counsel | AI liability posture; vendor BAA requirements; FDA SaMD risk appetite |
| HR / People Leadership | Workforce AI concerns; change management culture; training program infrastructure |

### Discovery Activities

**Technology Audit**
- Inventory all current AI tools, vendors, and experiments (include shadow IT)
- Map Concentra's data flow: EHR → billing → employer reporting → scheduling → analytics
- Identify data quality and governance gaps that would block AI deployment
- Assess current AI observability and monitoring capabilities
- Review existing vendor AI contracts and BAA agreements

**Clinical Workflow Immersion**
- Spend at least 2 days in Concentra clinical centers observing patient journey
- Map the occupational health encounter: intake → examination → treatment/testing → employer reporting → follow-up
- Identify where AI would augment clinical judgment vs. where it would introduce risk
- Understand the employer-employee-payer data relationship specific to occupational health

**Regulatory Landscape Assessment**
- Audit current HIPAA AI compliance posture against deployment patterns
- Review FDA AI/ML-based Software as a Medical Device guidance for applicability to planned use cases
- Map state-level AI legislation relevant to Concentra's geographic footprint
- Identify any existing FDA clearances or 510(k) submissions related to clinical software
- Review workers' compensation data regulations by key state markets

**AI Market Intelligence**
- Evaluate AI vendor landscape specific to occupational health (Epic AI capabilities, specialty AI vendors)
- Benchmark Concentra's AI maturity against healthcare AI leaders
- Identify 3–5 high-fit AI vendors for initial relationship development

### Phase 1 Deliverable
**AI Readiness Assessment Report** (presented to executive team at Day 30)
- Current state of Concentra's AI posture (honest RAG status)
- Data infrastructure gaps and remediation priorities
- Regulatory risk areas requiring immediate attention
- Top 10 AI use case candidates (unranked at this stage)
- Recommended organizational structure for the AI team

---

## Phase 2: Governance Framework & Portfolio Strategy (Days 31–60)

### Objective
Establish the governance infrastructure and prioritized AI portfolio before any pilot launches. Nothing goes to production without passing through the governance framework.

### AI Governance Framework — Design

**Enterprise AI Governance Policy**
- Define Concentra's AI principles: patient safety first, explainability required, human-in-the-loop for high-risk decisions, HIPAA compliance non-negotiable
- Establish AI risk classification system:
  - **Level 1 (Low Risk):** Administrative AI with no PHI, no clinical decisions (scheduling optimization, operational analytics)
  - **Level 2 (Moderate Risk):** AI with PHI access or operational impact (revenue cycle AI, employer reporting automation)
  - **Level 3 (High Risk):** AI touching clinical decision-making (injury severity, return-to-work recommendations, diagnostic support)
- Define review and approval process per risk level
- Establish AI incident response process (what happens when an AI system behaves unexpectedly)

**Responsible AI Standards**
- Bias detection requirements before deployment: demographic testing across patient population segments
- Explainability requirements: every AI recommendation surface must include a confidence indicator and the data it drew from
- Model validation framework: pre-production performance thresholds by use case
- Ongoing monitoring: automated performance tracking with alerting when model drift is detected
- Human-in-the-loop gates: mandatory for all Level 3 (high-risk) AI decisions

**AI Vendor Governance Standards**
- BAA requirement for all vendors with PHI access (non-negotiable)
- Data retention and training data policy requirements
- Vendor audit rights and transparency requirements
- Concentration risk limits (no critical AI function dependent on a single vendor)

**AI Portfolio Governance**
- Quarterly portfolio review with executive team
- AI performance scorecard (clinical outcomes, operational efficiency, financial ROI, risk status)
- AI budget governance: cost-per-initiative tracking and ROI realization monitoring

### AI Portfolio — Prioritized Use Case List

*Based on discovery findings, ranked by impact × data-readiness ÷ regulatory-risk*

**Wave 1 — Launch in Months 2–4 (Low Risk, High Value)**

| Use Case | Value | Why Now |
|----------|-------|----------|
| **Employer reporting automation** | Reduces manual reporting time; improves accuracy; stronger employer relationships | Administrative AI, no clinical decisions, Level 1 risk, fast time-to-value |
| **Revenue cycle AI** | Claim accuracy improvement, denial rate reduction, coding assistance | Level 2 risk; high financial ROI; doesn't touch clinical decisions directly |
| **Scheduling optimization** | Staff utilization efficiency; patient wait time reduction; center capacity optimization | Level 1 risk; operational data is typically clean and accessible |
| **Predictive operational analytics** | Center-level demand forecasting; surge preparation; staffing model optimization | Level 1 risk; uses operational, not clinical, data |

**Wave 2 — Launch in Months 4–8 (Moderate Risk, Strategic Value)**

| Use Case | Value | Governance Requirement |
|----------|-------|-----------------------|
| **Patient experience AI** | Satisfaction score improvement; personalized follow-up; employer feedback loops | PHI access requires HIPAA governance framework in place |
| **Referral management optimization** | Right-care, right-time recommendations; reducing unnecessary specialist referrals | Requires clinical input validation; Level 2 governance |
| **Workforce optimization** | AI-assisted return-to-work timeline recommendations for employers | Level 2 risk; clinical data involved; employer privacy obligations |
| **Drug testing program intelligence** | Compliance rate analytics; employer program optimization | Regulatory sensitivity requires careful governance design |

**Wave 3 — Plan in Year 1, Launch in Year 2 (Strategic AI at Clinical Depth)**

| Use Case | Value | Why This Timeline |
|----------|-------|-------------------|
| **Injury pattern prediction** | Employer-specific injury risk analytics; prevention recommendations | Requires 12+ months of governed data collection |
| **Clinical decision support** | Diagnostic assistance; treatment pathway recommendations | Level 3 risk; requires FDA regulatory review; clinical champion development |
| **AI-powered employer health intelligence** | Population health analytics for employer clients | Requires clean longitudinal data; high strategic value |

### AI Team — Organizational Design

```
VP, Artificial Intelligence
│
├── AI Strategy & Portfolio Management
│     AI Portfolio Manager
│     AI Business Analysts (2)
│
├── AI Engineering
│     Senior ML Engineer (Lead)
│     ML Engineers (2–3)
│     AI Platform Engineer
│     Data Scientist (1–2)
│
├── AI Governance & Responsible AI
│     AI Governance Lead (hybrid: technical + policy)
│     AI Risk & Compliance Analyst
│
└── AI Adoption & Literacy
      AI Change Management Lead
      Clinical AI Champions (embedded, not direct reports)
```

**Hiring Priority (sequence):**
1. AI Governance Lead (enables safe pilot launch)
2. Senior ML Engineer (builds technical capability)
3. AI Portfolio Manager (enables portfolio management at scale)
4. Clinical AI Champions (drives clinical adoption)

### Phase 2 Deliverable
**AI Strategy & Governance Presentation** (to executive team at Day 60)
- AI governance framework overview and adoption timeline
- Prioritized AI portfolio with Wave 1 launch plan
- AI team structure and hiring plan
- ROI projections for Wave 1 use cases
- Key risk areas and mitigation plan

---

## Phase 3: First Pilots & Board Readiness (Days 61–90)

### Objective
Launch 1–2 Wave 1 AI pilots with proper governance, measure early outcomes, and prepare the board-level AI strategy presentation.

### Pilot Launch Plan

**Pilot 1: Revenue Cycle AI (Target: Day 70)**
- Partner with revenue cycle leadership to define specific pain points (denials, coding accuracy, prior auth)
- Select AI vendor or internal build approach based on discovery findings
- Deploy with full governance: bias testing, audit logging, human review on flagged outputs
- Define success metrics: denial rate change, coding accuracy change, time-to-clean-claim reduction
- Establish weekly monitoring cadence with revenue cycle leadership

**Pilot 2: Employer Reporting Automation (Target: Day 75)**
- Identify top 10 most time-intensive employer reporting workflows
- Design AI-assisted automation with human review of every output before submission
- Measure: time-per-report reduction, accuracy rate, employer satisfaction change
- Document process changes required to scale

### AI Literacy — First Cohort Launch

**Executive AI Literacy Briefing (Day 65)**
- 2-hour working session with executive leadership team
- Agenda: what AI can do, what it can't, how Concentra will govern it, how to read AI performance reports
- Goal: executives leave with enough AI literacy to ask the right questions, not just approve projects

**Clinical AI Literacy — Phase 1 (Day 80)**
- 25-person pilot cohort (clinical staff from 2–3 centers)
- 4-module curriculum: what AI is, where it's being used at Concentra, how to report concerns, how to interpret AI-assisted tools
- Collect feedback to refine curriculum before broader rollout

### Board Presentation — Draft (Day 85)

**Draft structure for board AI strategy presentation:**

1. **The AI Opportunity for Concentra** (5 min) — market context, competitor positioning, what Concentra can achieve
2. **Our AI Strategy** (10 min) — the three-wave portfolio, governance-first approach, 3-year vision
3. **Governance & Risk Management** (10 min) — how we protect patients, stay HIPAA-compliant, and manage AI risk
4. **Current State & Pilot Results** (5 min) — what we've launched, early metrics, what we've learned
5. **Investment & ROI** (5 min) — team build plan, technology investment, projected returns
6. **Q&A** (10 min)

---

## 90-Day Success Metrics

| Milestone | Target Date | Success Indicator |
|-----------|-------------|-------------------|
| Stakeholder discovery complete | Day 30 | All key executives met; AI readiness report delivered |
| AI governance framework drafted | Day 45 | Policy in legal/compliance review |
| AI portfolio prioritized | Day 50 | Executive team alignment on Wave 1 use cases |
| AI team hiring plan approved | Day 55 | Budget approved; first 3 JDs posted |
| Wave 1 pilot 1 launched | Day 70 | Revenue cycle AI running with governance in place |
| Wave 1 pilot 2 launched | Day 75 | Employer reporting AI running with human review |
| Executive AI literacy briefing complete | Day 65 | 90%+ attendance; follow-on questions received |
| Clinical AI literacy pilot launched | Day 80 | 25 staff through first cohort |
| Board presentation draft delivered to CEO | Day 85 | Approved for board agenda |
| 90-day report to executive team | Day 90 | Pilot early metrics; governance adoption status; hiring progress |

---

## What This Plan Is Not

**This is not a "deploy 10 AI tools in 90 days" plan.** That approach produces technical debt, governance gaps, and clinical staff distrust that takes 2 years to repair.

**This is a foundation plan.** Every decision made in the first 90 days determines whether Concentra's AI program is trustworthy at year 3 or struggling to explain failures at year 2. The governance framework built in Phase 2 is the asset that makes every subsequent AI initiative faster, safer, and more defensible.

The right outcome at 90 days is not impressive volume — it's the confidence, across clinical, operational, and executive leadership, that AI at Concentra is being built the right way.

---

*Bryan Shaw | VP, Artificial Intelligence Candidate | Concentra | May 2026*
*BryanJShaw@gmail.com | 817-653-5656*
