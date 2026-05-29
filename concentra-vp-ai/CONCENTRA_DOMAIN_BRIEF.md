# Concentra Domain Brief
## EHR Integration · Revenue Cycle AI · Occupational Health · Healthcare Data Standards
### Concentra VP, Artificial Intelligence — Gap Closure Reference

> **How to use this document:** Read each section once before the interview. Each section ends with
> bridge language you can use verbatim or adapt. This document covers the four identified preparation
> gaps: EHR integration (Gap 1), Revenue Cycle AI (Gap 2), Occupational Health domain (Gap 3), and
> Healthcare Data Standards (Gap 4), plus the Master's degree offset and key competitive intelligence.

---

## SECTION 1 — EHR/EMR: CONCENTRA'S SYSTEM + INTEGRATION STRATEGY

### Concentra's Actual EHR: Allscripts TouchWorks (now Veradigm)

- **Selected:** 2012, initially for 310+ Concentra Medical Centers
- **Expanded partnership:** confirmed 2016
- **Current deployment:** across 520+ centers in 44 states
- **Brand note:** Allscripts rebranded as **Veradigm** in 2023 — same platform, new corporate name
- **Cloud infrastructure:** AWS (confirmed via Concentra mobile app development)

> When you hear "EHR" at Concentra, it is **Veradigm TouchWorks.** Not Epic, not Cerner.
> TouchWorks is purpose-built for ambulatory/outpatient settings — exactly the clinical model
> Concentra operates across 520+ walk-in centers.

### Why Bryan's CMMS/CRM Integration Depth Transfers Directly

| CRM/CMMS Pattern Bryan Has Built | EHR/EMR Equivalent | Transfer Effort |
|----------------------------------|---------------------|-----------------|
| Governed API access layer | SMART on FHIR API + governed gateway | Low — same architecture |
| Role-based data segmentation (RBAC) | Clinical RBAC over PHI vs. employer vs. billing data | Low — same pattern |
| Event-driven workflow triggers | HL7 ADT/ORU/SIU messages triggering AI workflows | Medium — new format, same pattern |
| Governed RAG over structured enterprise data | Governed RAG over clinical notes, labs, assessments | Low — same architecture |
| PHI classification + zero-token enforcement | Clinical PHI classification (higher sensitivity tier) | Low — extend existing framework |
| Audit trail for every data access | HIPAA audit log for every PHI touch | None — already built |
| Multi-tenant data isolation | Patient/employer data isolation in occupational health | Low — same pattern |
| Third-party data feed integration pipelines | Lab results, pharmacy, imaging inbound to EHR | Medium — new formats, same design |

**What is actually new:** HL7 v2.x message format structure, FHIR R4 resource model, SMART on FHIR
authorization flow, clinical data model conventions (ICD-10, CPT, LOINC — covered in Section 4).

**What is not new:** The governance architecture, PHI pipeline design, RBAC model, audit requirements,
zero-token enforcement logic.

### Veradigm/TouchWorks — API Capabilities Relevant to AI

- Veradigm Developer Program: REST APIs for clinical data access
- HL7 v2.x messaging: operational workflow integration (scheduling triggers, lab result delivery, billing events)
- FHIR R4 endpoints: modern API access to patient and clinical resource data
- Extension point model: third-party AI overlays are supported — the architecture exists to add AI
  without ripping out the EHR

### 60-Day EHR Integration Bridge Plan

**Week 1–2 (Discovery)**
- Obtain Veradigm API documentation from clinical informatics team
- Map current data flows: what exits the EHR, where it goes, what governance exists today
- Identify AI insertion points: intake → assessment → clinical decision → documentation → coding → discharge
- Interview clinical informatics team on data quality, structured vs. unstructured split, current API usage

**Week 3–4 (Architecture Design)**
- Design governed AI data access layer over TouchWorks
- Map PHI classification to existing governance patterns — extend for clinical data types
- Identify which AI use cases require FHIR R4 vs. HL7 v2.x operational messaging
- Define the AI insertion points — where does AI add value without disrupting clinical workflow

**Month 2 (First Pilot)**
- Deploy governed data pipeline: TouchWorks → AI inference layer
- Pilot: clinical documentation assistance — auto-suggest ICD-10/CPT codes from clinical notes
- Instrument for coding accuracy lift, denial rate delta, and clinical workflow time impact
- Baseline denial rate pre-AI; measure 60-day improvement

### EHR Gap — Interview Bridge Language

> *"Concentra runs Veradigm TouchWorks — I've mapped it in detail. The integration pattern for AI
> over an EHR is architecturally identical to what I've built over enterprise CRM and CMMS systems:
> a governed API access layer, role-based data segmentation, event-driven workflow triggers, and
> PHI classification enforced before any inference call. The specific format differences — HL7
> messaging, FHIR resources — I've studied and have a clear 60-day plan to operationalize with
> your clinical informatics team. The governance architecture does not change; the data formats do.
> That is a 60-day problem, not a strategic gap."*

---

## SECTION 2 — REVENUE CYCLE AI STRATEGY

### The Occupational Health Three-Party Billing Model

Concentra's RCM is fundamentally different from standard healthcare billing. Three billing streams
run simultaneously, each with its own rules, forms, compliance requirements, and AI opportunities:

```
EMPLOYER ────────────── Direct contracts; pays for preventive + mandatory services
    |
CONCENTRA ──────────── Delivers care; manages three billing streams simultaneously
    |
WORKERS' COMP CARRIER ─ Pays claims for work-related injury treatment
    |
EMPLOYEE/PATIENT ────── Receives care; cost-share for non-occupational urgent care
```

| Billing Stream | Volume Driver | AI Opportunity |
|----------------|---------------|----------------|
| **Employer Direct** | DOT physicals, drug testing, preventive protocols, wellness | Invoice automation, protocol compliance, demand forecasting |
| **Workers' Comp Claims** | Work-related injuries | Claims lifecycle AI, auth tracking, denial prediction, RTW prediction |
| **Patient/Standard Insurance** | Non-occupational urgent care | Eligibility + auth automation, remittance matching |

### Bryan + Inflexis RCM Context

Bryan has been working directly with Kelly (CRO, Inflexis Technologies) to develop revenue cycle AI
strategy as part of Inflexis's healthcare practice. The multi-tenant billing governance architecture
in AIXaaS™ — deterministic compliance enforcement, billing data isolation, audit trails — maps
directly to the three-party billing complexity Concentra operates.

**Frame for interview:**
> *"Revenue cycle in occupational health is a three-party orchestration problem — employer contract
> rules, workers' comp carrier requirements, and clinical coding accuracy have to align or revenue
> leaks from all three seams simultaneously. I've been developing RCM AI strategy as part of our
> healthcare practice at Inflexis, including hands-on work with our Chief Revenue Officer on how AI
> closes gaps in complex billing environments. My first 60 days at Concentra would start by mapping
> where your denial rate and underpayment rate sit against industry benchmarks — that tells you
> exactly where AI delivers dollar one."*

### RCM Domain Map — AI Use Cases

**A. Clinical Documentation → Coding Accuracy (Highest ROI, Fastest to Launch)**
- Auto-suggest ICD-10/CPT codes from clinical notes in real time — reduces coder effort and error
- State-specific workers' comp fee schedule enforcement at time of coding — 50 different state rules
- OSHA recordability determination at point of care — auto-populate OSHA 300 log entry
- **Benchmark impact:** 15–25% reduction in first-pass claim denials; 30–40% reduction in manual coding time

**B. Workers' Comp Claims Lifecycle**

| Claim Stage | AI Application | Business Value |
|-------------|----------------|----------------|
| First Notice of Loss (FNOL) | Extract injury data from clinical notes; verify employer coverage | Faster initiation, fewer missing fields |
| Prior Authorization | Track auth requirements by carrier; escalate expiring auths before care | Eliminates auth-related denials |
| Claims Submission | Bill scrubbing — fee schedule errors, missing fields caught before submission | Reduce clean claim rejections |
| Adjudication Support | Flag underpayments vs. state fee schedule; auto-generate appeals for known patterns | Recover underpaid revenue |
| Return-to-Work Prediction | ML model on RTW timeline by injury type, treatment protocol, patient factors | Employer planning; reduce unnecessary extensions |
| Claim Closure | Flag ready-to-close claims; alert on statistical outliers | Reduce claim leakage and fraud |

**C. Employer Billing Cycle Automation**
- Protocol management AI: enforce service bundles per employer at point of service and billing
  (e.g., "all new hires: DOT physical + 10-panel drug screen + baseline audiogram")
- Invoice automation: aggregate services per employer per billing period with full line-item detail
- Demand forecasting: predict service volume by employer/location/season for staffing and supply optimization
- Employer health analytics portal: AI-generated population health insights — HIPAA-compliant,
  de-identified — differentiates Concentra and drives employer retention

**D. DOT Compliance Revenue Stream**
- CDL driver certification tracking: predict renewal windows across entire employer CDL driver population
- FMCSA Clearinghouse integration: automate query submissions and reporting; alert employers to violations
- DOT physical completion workflow: auto-generate and route Medical Examiner Certificates; reduce credentialing delay

**E. Drug & Alcohol Testing Revenue**
- Digital chain of custody automation: eliminate manual COC compliance errors on the revenue-bearing event
- Lab result integration: auto-trigger billing event on confirmed result receipt — zero manual initiation
- Positive result workflow: HIPAA-governed employer notification per DOT and non-DOT rules, fully audited
- MRO workflow support: surface result context and protocol steps for faster MRO review cycle

**F. Standard Insurance / Non-Occupational Urgent Care**
- Pre-authorization automation: check eligibility and auth requirements before care is delivered
- Remittance processing: auto-reconcile EOBs against claims; flag underpayments for human review
- Denial management: pattern analysis to identify systemic submission errors and drive resubmission strategy

### RCM AI Priority Sequence

| Priority | Initiative | Why First | Target Launch |
|----------|------------|-----------|---------------|
| 1 | Documentation → coding accuracy | Fastest ROI; immediate denial reduction | Day 60–90 |
| 2 | Authorization tracking | Revenue leakage prevention | Day 60–90 |
| 3 | Denial pattern analysis + appeals | Recovers already-lost revenue | Day 90–180 |
| 4 | Employer billing automation | Client retention + operational efficiency | Day 90–180 |
| 5 | Employer health analytics portal | Differentiation; drives employer renewal | Day 180–365 |
| 6 | Workers' comp RTW prediction | High value; needs data runway | Day 180–365 |
| 7 | DOT scheduling intelligence | Subscription-model revenue for employer clients | Year 2 |

---

## SECTION 3 — OCCUPATIONAL HEALTH DOMAIN KNOWLEDGE

### Concentra's Service Line Map

Knowing these service lines before the interview is the difference between answering
"how would you prioritize AI across our portfolio?" with specificity vs. generality.

**Service Line 1: Occupational Medicine**
Pre-employment physicals, DOT physicals, OSHA medical surveillance (hearing, respirator,
chemical exposure), fitness-for-duty evaluations, return-to-work clearances, MRO services.

- AI priorities: scheduling optimization, OSHA recordkeeping automation, RTW timeline
  prediction, employer compliance reporting
- Regulatory overlay: OSHA 29 CFR 1904, DOT 49 CFR Part 40 & Part 391, ADA, state workers' comp

**Service Line 2: Workers' Comp Injury Treatment**
Injury treatment from first visit through rehabilitation and return to work. Concentra
coordinates with employers, insurance carriers, and treating physicians.

- AI priorities: injury triage support, treatment protocol optimization, claim lifecycle
  management, RTW prediction, fraud pattern detection
- Regulatory overlay: 50 different state workers' comp statutes, HIPAA with employer carve-outs, ADA

**Service Line 3: Urgent Care**
Non-occupational walk-in urgent care. Standard insurance + self-pay billing model.

- AI priorities: patient flow prediction, staffing optimization, standard billing automation
- Regulatory overlay: HIPAA, state medical practice acts, standard insurance billing

**Service Line 4: Physical Therapy**
Injury rehabilitation, functional capacity evaluations (FCE), work conditioning programs.

- AI priorities: treatment plan optimization, functional outcome prediction, discharge readiness prediction
- Regulatory overlay: state PT licensure requirements, workers' comp therapy authorization rules

**Service Line 5: Drug & Alcohol Testing**
Largest occupational drug testing network in the US. DOT and non-DOT testing, chain of custody, MRO.

- AI priorities: COC automation, lab integration, positive result workflow automation,
  FMCSA Clearinghouse integration
- Regulatory overlay: DOT 49 CFR Part 40, SAMHSA certified lab requirements,
  HHS mandatory guidelines, state drug testing laws

**Service Line 6: Employer Services / Onsite Clinics**
On-site clinical services at employer facilities. Wellness programs, health coaching,
chronic condition management.

- AI priorities: population health analytics, condition management support, wellness
  program effectiveness measurement, employer ROI reporting
- Regulatory overlay: HIPAA employer wellness exception, ADA voluntary wellness standards, GINA

### The Occupational Health Regulatory Matrix

| Regulatory Framework | How It Applies at Concentra | AI Implication |
|---------------------|-----------------------------|-----------------|
| **HIPAA** | PHI for patient care — with employer carve-outs for occupational health reporting | AI must know exactly which data flows to employers are permissible and under what conditions |
| **OSHA 29 CFR 1904** | Employer recordkeeping — Concentra generates the data that feeds employer OSHA logs | AI automates recordability determination and log entry at point of care |
| **DOT 49 CFR Part 40** | Drug/alcohol testing procedures — Concentra operates as testing site and C/TPA | AI automates COC, result routing, employer notification |
| **DOT 49 CFR Part 391** | CDL driver physical qualification standards | AI tracks certification, predicts renewal windows, alerts on disqualification |
| **FMCSA Clearinghouse** | Federal CDL drug/alcohol violation database | AI integration for automated queries, reporting, and employer alerts |
| **State Workers' Comp** | 50 different systems — treatment protocols, billing rules, required forms | AI enforces state-specific rules per clinic location dynamically |
| **ADA** | Fitness-for-duty, pre-employment exams, RTW — cannot discriminate on disability | AI clinical outputs require bias testing; licensed clinician retains final authority |
| **GINA** | Genetic information excluded from employer wellness reporting | AI wellness systems must exclude genetic data fields from employer-facing outputs |
| **FDA SaMD Guidance** | Clinical decision support that influences diagnosis or treatment | Design constraint for clinical AI; most occupational health AI stays below the SaMD threshold |

### AI Use Case Portfolio by Wave

**Wave 1 — Day 60–180: Operational AI (Fastest ROI, Lowest Clinical Risk)**
- Documentation → coding accuracy across all service lines
- DOT certification scheduling intelligence
- OSHA recordability determination at point of care
- Drug testing COC automation + billing trigger
- Authorization tracking and escalation

**Wave 2 — Day 180–365: Clinical Support AI**
- RTW timeline prediction (workers' comp + PT)
- Employer health analytics portal
- Denial pattern analysis + appeals automation
- Injury triage support

**Wave 3 — Year 2+: Predictive and Strategic AI**
- Injury prevention analytics for employer clients
- Workers' comp fraud pattern detection
- Workforce scheduling optimization across 520+ centers
- Population health prediction for employer renewal strategy

### Occupational Health Domain — Interview Bridge Language

> *"Occupational health is unique because it serves two principals simultaneously — the employee
> who receives care and the employer who in many cases is paying for it. That dual-service
> relationship creates governance complexity most healthcare AI gets wrong: knowing exactly which
> patient data can flow to the employer, when, and under what HIPAA carve-out, requires precise
> governance architecture — not a general HIPAA policy. On top of that, each of Concentra's
> service lines — DOT physicals, drug testing, workers' comp, PT, onsite employer services —
> carries its own regulatory overlay: OSHA recordkeeping, DOT CFR Part 40, 50 state workers'
> comp systems, FMCSA Clearinghouse. AI that serves Concentra has to be jurisdiction-aware,
> service-line-aware, and employer-contract-aware simultaneously. That is exactly the
> multi-framework governance complexity I have built infrastructure for."*

---

## SECTION 4 — HEALTHCARE DATA STANDARDS: COMPLETE REFERENCE

> A VP AI at a healthcare organization is in every conversation about data interoperability —
> with EHR vendors, insurance carriers, employers, labs, and regulators. This section maps
> every standard you need to speak to confidently. Study it once; reference it as needed.

---

### Clinical Messaging Standards

**HL7 v2.x — The Operational Backbone**

The dominant healthcare messaging standard for real-time operational data exchange. Still the primary
messaging format in most EHR systems including Veradigm TouchWorks. Pipe-delimited text messages
organized by event trigger type.

| Message Type | Trigger | AI Workflow Hook |
|-------------|---------|------------------|
| ADT (Admit/Discharge/Transfer) | Patient arrives, is discharged, or transfers | Initiates AI context prep; patient arrival fires AI workflow |
| ORU (Observation Result) | Lab result or diagnostic result delivered | Triggers clinical decision support and coding suggestion |
| SIU (Scheduling) | Appointment created, modified, or cancelled | Feeds demand forecasting and staffing optimization |
| MDM (Medical Document) | Clinical note created or updated | Triggers coding AI — document completed → ICD-10/CPT suggestion |
| DFT (Detail Financial Transaction) | Billing charge posted | Billing validation AI trigger |
| BAR (Patient Account) | Account created or modified | Revenue cycle AI trigger |

**HL7 FHIR R4 — The Modern API Standard**

RESTful API standard replacing legacy HL7 for new integrations. JSON/XML resource model —
natively compatible with modern AI systems. SMART on FHIR provides OAuth2-based authorization
for third-party applications accessing clinical data.

| FHIR Resource | Contains | AI Use Case |
|---------------|----------|-------------|
| Patient | Demographics, identifiers, contacts | Patient matching, consent verification |
| Encounter | Visit details, provider, location, dates | AI context window for the current visit |
| Observation | Lab results, vitals, clinical assessments | Clinical decision support trigger data |
| Condition | Diagnoses, active problems | ICD-10 coding verification, care gap detection |
| Procedure | Treatments performed | CPT coding, protocol compliance check |
| Claim | Billing claim data | Coding validation, revenue cycle AI |
| DocumentReference | Clinical notes and reports | Unstructured text source for AI extraction |
| ServiceRequest | Lab orders, imaging, referrals | Authorization AI trigger |
| CarePlan | Treatment plan details | RTW planning AI, condition management |

**CDA / C-CDA (Clinical Document Architecture)**
XML-based standard for structured clinical documents — discharge summaries, referral notes,
Continuity of Care Documents (CCD). C-CDA is the US interoperability standard for care
transitions. Relevant when AI processes documents that cross care settings or move between
Concentra and external providers.

---

### Clinical Terminology Standards

| Standard | What It Is | AI Application |
|----------|------------|----------------|
| **ICD-10-CM** | ~70,000 diagnosis codes used for clinical documentation and billing | Auto-suggest diagnosis codes from clinical notes; validate coding accuracy |
| **CPT** | AMA procedure billing codes for all clinical services — required on every professional claim | Auto-suggest procedure codes; prevent unbundling and upcoding errors |
| **HCPCS Level II** | CMS codes for durable medical equipment, drugs, non-physician services | Equipment and drug billing validation |
| **LOINC** | Universal names and codes for lab tests and clinical observations | Standardize lab result interpretation across labs and facilities |
| **SNOMED CT** | Most comprehensive clinical terminology — ~350,000 concepts | Clinical NLP, terminology normalization, decision support matching |
| **RxNorm** | Standard for drug names and clinical drug identifiers | Drug interaction checking, medication reconciliation |
| **NDC (National Drug Code)** | FDA drug identification — manufacturer, product, package | Drug testing result classification, pharmacy billing |

---

### Administrative and Billing Standards

**X12 EDI Transactions — The Insurance Billing Wire Protocol**

Every insurance claim, payment, and eligibility check runs over X12 EDI.
Understanding these is fluency in the revenue cycle conversation:

| X12 Transaction | Purpose | AI Use |
|-----------------|---------|--------|
| **837P (Professional)** | Submit professional claims to insurance carriers | Coding AI validates before 837 submission; catch errors before rejection |
| **835 (Remittance Advice)** | Receive payment explanation and adjustment data | Remittance matching AI; underpayment detection |
| **270/271 (Eligibility)** | Check and receive patient insurance eligibility | Pre-service eligibility AI; auth requirement trigger |
| **276/277 (Claim Status)** | Check and receive claim processing status | Claims tracking automation |
| **278 (Authorization)** | Submit and receive prior authorization decisions | Authorization AI integration; workers' comp auth tracking |

**NPI (National Provider Identifier)**
10-digit unique identifier for every healthcare provider and organization. Required on all claims.
AI application: provider credentialing validation, network adequacy analysis.

---

### Federal Interoperability and Regulatory Standards

**USCDI (United States Core Data for Interoperability)**
ONC-defined minimum dataset for national health information exchange. Required for EHR
certification under 21st Century Cures Act. Defines the data fields guaranteed available
via certified EHR APIs: demographics, clinical notes, lab results, medications,
immunizations, procedures, vital signs.

**SMART on FHIR**
OAuth2/OpenID Connect authorization framework for healthcare applications accessing EHR data.
The technical standard for building governed AI overlays on top of EHR systems like Veradigm.
Every EHR-integrated AI application at Concentra runs through SMART on FHIR for authorization.

**Da Vinci Project (HL7 FHIR Implementation Guides)**
FHIR implementation guides for payer-provider data exchange. Directly relevant for automating
workers' comp prior authorization at Concentra:
- **CRD** (Coverage Requirements Discovery): check auth requirements before care is delivered
- **DTR** (Documentation Templates and Coverage Rules): gather required documentation automatically
- **PAS** (Prior Authorization Support): automated auth request submission to carriers

**21st Century Cures Act / Information Blocking Rule**
Federal law requiring health information sharing; prohibits EHR vendors and health systems
from blocking data access. Creates patient rights to EHR data via APIs. The legal framework
for building any patient-facing AI feature that surfaces clinical data.

---

### Occupational Health–Specific Data Standards

These are specific to Concentra's operational context. No other VP AI candidate from outside
occupational health will know these — knowing them is a differentiator in the room.

| Standard | What It Is | AI Application |
|----------|------------|----------------|
| **OSHA 300/300A/301** | 300 = annual injury/illness log; 301 = individual incident report; 300A = annual summary posted in workplace | At point of care: AI determines OSHA recordability, auto-populates 300 log, alerts employer client |
| **Workers' Comp FROI** | First Report of Injury — state-specific form filed at claim initiation; some states use IAIABC EDI standard | Auto-generate FROI from clinical documentation; enforce state-required fields per clinic location |
| **DOT Medical Examiner Certificate (MEC)** | Physical certification issued to CDL drivers passing DOT physicals; filed with FMCSA National Registry | Auto-generate and route MEC; predict expiration windows across employer CDL fleets |
| **FMCSA Drug & Alcohol Clearinghouse** | Federal database of CDL driver drug/alcohol violations; employers must query before hire and annually | Automate query workflows; alert employers to violations and resulting hiring obligations |
| **SAMHSA/DOT Chain of Custody Form** | Federal form for urine drug specimen collection; required for all DOT testing, strongly recommended for non-DOT | Digital COC automation; compliance error detection; billing event trigger on collection |
| **MRO Reporting Standards** | Positive test results must be reviewed by licensed MRO before employer notification; HIPAA carve-out applies | MRO workflow support; result routing governance; employer notification automation |

---

### Healthcare Data Standards — Interview Bridge Language

> *"I've mapped the full data standard landscape relevant to Concentra — from the HL7 v2.x
> operational messaging in TouchWorks to FHIR R4 for new integrations, X12 EDI transactions
> across the billing cycle, and the occupational health–specific standards most AI architects
> never encounter: OSHA recordkeeping forms, DOT chain of custody, FMCSA Clearinghouse, and
> IAIABC workers' comp FROI requirements. The AI governance architecture I've built is
> data-standard-agnostic — it governs the pipeline regardless of format. Extending it for
> FHIR resources or X12 transactions is a configuration exercise, not an architectural rebuild."*

---

## SECTION 5 — MASTER'S DEGREE OFFSET

### The Honest Frame

The posting says "Master's degree preferred." That is a preference, not a requirement.
Every required qualification is already demonstrated above bar. Own this proactively —
do not wait to be asked.

### What Bryan Has That a Master's Program Teaches You to Plan

| Master's Curriculum Topic | Bryan's Production Equivalent |
|--------------------------|--------------------------------|
| AI/ML theory and methods | 13 production AI deployments across 6 regulated industries |
| Governance and ethics frameworks | 10-layer deterministic AI governance architecture — in active production |
| Healthcare informatics | Active NDA clinical AI deployment + HIPAA production platform + published guidance |
| Research and evidence synthesis | Publicly published thought leadership — knowledge tested in practice, not just claimed |
| Data architecture and modeling | 23 years designing data systems from infrastructure up |
| Organizational change management | Teams of 30+; enterprise adoption programs; CoreSkills4AI platform |
| Applied capstone project | 13 capstones — all in production, all measured |

### Primary Response — If the Degree Comes Up

> *"I don't have a master's degree — I want to be direct about that. What I chose instead was
> to build what a master's program teaches you to plan. The governance framework I would bring
> to Concentra would be graduate curriculum content — and it is production-tested, not theoretical.
> I respect what the preference signals about analytical rigor, and my answer to that signal is
> the track record: 23 years, 13 builds, 6 regulated industries, published thought leadership,
> and an active clinical AI deployment. The rigor is there — it has been tested in production,
> not in a classroom."*

### If the Degree Is a Hard Organizational Requirement

> *"If the organization requires a master's as an HR qualification gate, that is a real constraint
> and I respect it. If the preference is about analytical depth and the strategic thinking this
> role requires, I am confident the production record answers that question more directly than a
> transcript would. I would rather you tell me which it is so we are both clear."*

---

## KEY COMPETITIVE INTEL — JASON COOPER, CHIEF DATA, ANALYTICS & AI OFFICER

### Who He Is and Why He Matters for This Interview

Concentra appointed **Jason Cooper** as **Chief Data, Analytics, and Artificial Intelligence Officer**
on **November 10, 2025** — six months before this interview process.

**His stated mandate:** Ensure Concentra's data strategy and governance, technology enablement,
and insight generation are aligned with enterprise growth priorities.

**His background:** 25+ years leveraging data and technology. Fellow of the American College
of Health Data Management. Active in Society for Information Management. Board member at
Covenant HR. Advisor to .406 Ventures' Data and AI executive council.

**What this means for the VP AI role:**
- Cooper owns the **strategic direction** — data strategy, enterprise priorities, governance alignment
- The VP AI role provides the **execution capability** — AI architecture, engineering, deployment,
  team management
- Cooper comes from a **data analytics background** — Bryan provides the **AI governance
  architecture** depth Cooper's mandate requires to become executable at clinical scale
- Bryan is not competing with Cooper — Bryan is the execution partner Cooper needs

### How to Position This in the Interview

> *"I noticed Jason Cooper's appointment as Chief Data, Analytics, and AI Officer in November —
> that is a strong signal that Concentra is building a structured, senior-led data and AI
> organization, not just doing point-solution pilots. What I bring is complementary to that kind
> of leadership: I build the governance infrastructure that makes AI safe to deploy at scale in
> clinical settings, and I have done it across multiple regulated industries. The value I would
> add to Jason's mandate is straightforward: he sets the strategic direction, I build the
> architecture that makes it executable and auditable. That is the partnership model that turns
> an AI strategy into an AI program."*

### Research Cooper Before the Interview
- LinkedIn profile — understand prior roles and stated leadership priorities
- Covenant HR board — what is his governance philosophy in practice?
- .406 Ventures AI executive council — what companies and theses is he associated with?
- Any Concentra press releases, interviews, or conference appearances since November 2025

---

*Private · Bryan Shaw · May 2026 · BryanJShaw@gmail.com · 817-653-5656*
