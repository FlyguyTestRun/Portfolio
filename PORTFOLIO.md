# Bryan Shaw
## AI Architect & CTO &nbsp;|&nbsp; Multi-Agent Orchestration &nbsp;·&nbsp; Governed RAG Systems &nbsp;·&nbsp; Enterprise Platform Engineering

**Dallas–Fort Worth, TX** &nbsp;|&nbsp; [BryanJShaw@gmail.com](mailto:BryanJShaw@gmail.com) &nbsp;|&nbsp; 817-653-5656  
[LinkedIn](https://www.linkedin.com/in/bryan-shaw-45a23124/) &nbsp;|&nbsp; [GitHub: FlyguyTestRun](https://github.com/FlyguyTestRun) &nbsp;|&nbsp; [GitHub: Inflexis-ai Org](https://github.com/Inflexis-ai) &nbsp;|&nbsp; [Platform: app.inflexis.ai](https://app.inflexis.ai)

**[Full Detailed Resume →](./resume/Bryan-Shaw-Resume.md)**

---

## Summary

Enterprise AI architect and hands-on platform engineer with **23+ years** of experience shipping production systems across infrastructure, cloud, and advanced AI. Currently serving as **CTO and Founding Partner of Inflexis Technologies**, leading all architecture, engineering, and client delivery for **AIXaaS™** — a multi-tenant AI orchestration operating system built for regulated enterprise. Active across **13 distinct builds spanning 6 industry verticals** — federal, cybersecurity, industrial, education, food service, healthcare, and enterprise facilities management — with six simultaneous live client engagements and seven published case study deployments.

Specializes in end-to-end AI system design: selecting the right RAG architecture for each retrieval problem, routing inference across LLMs by scope and cost, bridging enterprise APIs into governed pipelines without disrupting incumbent systems, and preparing raw enterprise data for vector storage with production-grade quality gates. Automation pipelines at Inflexis are built on **agentic RAG** — where retrieval is governed by multi-step agent reasoning, not a single-pass lookup. Brings a rare combination of executive strategy, product ownership, and deep hands-on engineering: having led cross-functional teams of up to 30, partnered directly with C-suite and legal stakeholders, and collapsed 6–12 month AI implementations into weeks through reusable, governed architecture patterns.

Knows how to partner with revenue management teams to identify and close AI-addressable overhead — not just building AI for AI's sake, but designing systems that reduce operational cost, compress billing cycles, and surface revenue signals that would otherwise stay buried in unstructured data.

**Core focus:** Multi-agent orchestration · Governed RAG pipelines · Compliance automation (25+ frameworks) · Zero-trust AI infrastructure · Human-in-the-loop workflows · Air-gapped enterprise deployments

> **Architecture philosophy:** Governance is not a layer you bolt on after the system works — it is the structural load that makes the system trustworthy. Speed in AI delivery is a byproduct of governance built correctly from the beginning: reusable compliance patterns, modular agent architecture, pre-validated retrieval pipelines, and deterministic enforcement already running in production before a new client engagement begins. A platform that can be safely demonstrated in 72 hours isn't fast because shortcuts were taken — it's fast because the foundation was built to carry weight.

---

## AI Architecture Expertise — Technical Decision Framework

The decisions that determine whether an AI system succeeds or fails are made before the first line of model code is written. The following frameworks govern every architecture decision in AIXaaS™ production deployments.

---

### RAG Architecture — Selection Framework

Knowing which retrieval-augmented generation pattern to deploy is the difference between an AI system that surfaces accurate, trusted answers and one that confidently hallucinates. Each pattern has a specific best-fit condition. Deploying the wrong one is a design failure, not a model failure.

| RAG Pattern | Core Mechanic | Best Deployment Context | AIXaaS™ Production Use |
|------------|--------------|------------------------|------------------------|
| **Naive RAG** | Single-pass retrieve → generate | Prototyping, small curated corpora, low-stakes Q&A | Deprecated in production; sandbox/pilot only |
| **Advanced RAG** | Query rewriting + cross-encoder reranking + HyDE | General enterprise Q&A where accuracy justifies latency cost | Standard upgrade over Naive in all client onboarding |
| **Hybrid RAG** | Vector semantic + BM25 keyword + fallback tier | Enterprise production — mixed technical/natural language, large corpora | **Production standard across all 13 builds** — 3-tier: Pinecone → pgvector → keyword |
| **Modular RAG** | Composable retrieval modules (web, DB, document store, API) | Multi-source knowledge: CMMS + structured DB + document corpus simultaneously | Corrigo/BNSF integration; AIXaaS data foundation layer |
| **Graph RAG** | Entity-relationship graph traversal + vector retrieval | Complex domain knowledge with interconnected entities: compliance, legal, supply chain | Government contractor knowledge graph; compliance framework mapping |
| **Agentic RAG** | Agent-planned multi-step retrieval — agent reasons about what to retrieve, when, and in what sequence | **Automation pipelines** where retrieval requires planning before querying; multi-step workflows | **Core AIXaaS™ pattern** — all production automation pipelines; foundation of the 5-agent MAO architecture |
| **Corrective RAG (CRAG)** | Evaluate retrieval quality before generation; correct or discard bad retrievals | Production safety in regulated environments; zero tolerance for hallucination on clinical/legal output | Healthcare and government deployments where bad retrieval is a compliance event |
| **Self-RAG** | Model decides whether retrieval is needed before querying | Mixed-complexity query volumes; cost optimization at scale | AIXaaS token optimization routing; simple queries bypass retrieval entirely |
| **Speculative RAG** | Fast draft with lightweight model + retrieval-grounded verification with frontier model | High-throughput, latency-sensitive pipelines needing draft-then-verify quality control | Under evaluation in AIXaaS sandbox for high-volume classification |

**The selection principle applied to every engagement:**
> *What is the corpus structure — flat documents, entity graph, or multi-source? What is the latency budget? What is the cost of a bad retrieval — low-stakes or clinical/legal decision? What is the query distribution — simple lookup or multi-step reasoning? These four questions determine the RAG pattern before a single vector index is built.*

---

### LLM Selection — Scope-Driven Routing

AI systems that call the most powerful model for every task are not intelligent — they are expensive. The AIXaaS™ cost-aware routing layer selects the LLM tier based on task complexity, data sensitivity, and latency requirements. The 31% token efficiency improvement in production comes from routing decisions, not model tuning.

| Task Tier | Model Class | Production Examples | Routing Criteria |
|----------|------------|--------------------|-----------------|
| **Complex reasoning** | Frontier (Opus-tier) | Claude Opus 4.x, GPT-4o | Governance decisions, multi-document synthesis, long-context analysis, compliance interpretation across frameworks, adversarial review |
| **Production inference** | Production (Sonnet-tier) | Claude Sonnet 4.x, GPT-4o mini | Standard agentic tasks, structured output generation, document analysis — **AIXaaS™ default inference tier** |
| **High-volume, low-latency** | Lightweight (Haiku-tier) | Claude Haiku 4.x, Gemini Flash 2.x | Triage classification, entity extraction, routing decisions, PII pre-scan, high-volume summarization |
| **Air-gapped / data-sovereign** | On-premise | Llama 3.x, Mistral, Phi-3 | HIPAA PHI processing, FedRAMP air-gapped environments, data-sovereignty, offline clinical deployments |
| **Specialized tasks** | Domain-specific | Whisper (transcription), LLaVA (vision), CodeLlama (code) | Meeting intelligence transcription, document image extraction, code generation agents |

**Multi-provider architecture:** AIXaaS™ runs across 6 LLM providers simultaneously — Anthropic, OpenAI, AWS Bedrock, Azure OpenAI, Google, and local Ollama — with automatic failover and cost-optimized routing. No single-provider lock-in; provider decisions are reversible without re-architecting.

---

### API Bridging & System Integration Patterns

Enterprise AI does not replace existing systems — it integrates with them. The ability to bridge disparate enterprise APIs into a governed AI pipeline without disrupting incumbent operations is where most enterprise AI implementations succeed or fail.

**Patterns deployed in production:**

- **OAuth 2.0 / OIDC identity federation** — bridging multiple enterprise identity systems into a single authorized AI agent context; deployed across every AIXaaS engagement (Azure Entra ID + application-level OIDC)
- **REST + webhook event streaming** — real-time event processing; Corrigo Enterprise API at 18.5M work orders/year scale; Stripe payment events; HubSpot CRM pipeline triggers
- **HL7 FHIR R4 + SMART on FHIR** — healthcare EHR integration (Veradigm TouchWorks); SMART on FHIR OAuth authorization for AI overlay without replacing clinical systems
- **X12 EDI bridging** — insurance billing data ingestion into governed AI pipelines (healthcare RCM use cases)
- **CMMS/ERP overlay architecture** — AI agent layer that reads and writes to enterprise systems via their native APIs while maintaining governance and audit trail — without replacing the underlying platform
- **Multi-system MAO orchestration** — AI as the integration middleware; agents receive events from System A, apply governed reasoning, and take coordinated actions in Systems B, C, and D via their respective APIs
- **Legacy system integration** — structured overlay adds AI intelligence to existing platforms via their current API surface, eliminating the need for platform replacement projects

> *The best integration is the one that doesn't require the enterprise to change anything they already own. The AI layer integrates into the existing API surface, enforces governance on top of it, and delivers capability without a migration project.*

---

### Data Migration & Vector DB Readiness

The quality of a RAG system is determined at the data preparation stage, not at inference time. A vector database populated with malformed, duplicated, stale, or improperly chunked content will produce confident-sounding wrong answers regardless of which retrieval pattern or model sits on top of it.

**The AIXaaS™ data readiness pipeline — applied before any vector index is created:**

1. **Corpus audit** — inventory all data sources; classify by type (structured/unstructured/semi-structured), freshness, completeness, and sensitivity (PII/PHI classification before any data moves)
2. **Quality gates** — documents that fail completeness, format, or sensitivity checks are rejected before chunking; not ingested with flags, not silently dropped
3. **Chunking strategy selection** per content type:
   - *Fixed-size:* fast, uniform; for dense technical documentation with consistent structure
   - *Semantic:* sentence-boundary aware; for narrative content, clinical notes, case studies
   - *Hierarchical:* preserves document structure (section → subsection → paragraph); for legal, compliance frameworks, SOPs
4. **Metadata enrichment before embedding** — every chunk tagged with source system, document type, domain, freshness timestamp, sensitivity classification, and confidence score before it is embedded
5. **Deduplication and versioning** — semantic dedup prevents stale retrieval competing with current data; version-controlled embeddings for full auditability
6. **Embedding model selection** — general-purpose for broad enterprise content; domain-specific models for specialized corpora (medical, legal, financial); embedding drift monitoring after model updates
7. **Vector index architecture selection:**
   - *HNSW:* approximate nearest neighbor, fast query, higher memory — AIXaaS™ production default via Pinecone/Qdrant
   - *IVF:* inverted file with compression — for memory-constrained or large-scale deployments
   - *Flat:* exact search — small, curated, critical corpora only (compliance rule sets)
8. **Training-serving consistency** — production retrieval must match the retrieval context used during evaluation; skew between training and serving is the number one cause of RAG performance degradation at scale
9. **3-tier fallback validation** — all three retrieval tiers confirmed coherent before any client data goes live

---

## Executive Impact

| Outcome | Result |
|---------|--------|
| Implementation timeline reduction | 6–12 months → **weeks** |
| Operational efficiency improvement | **35–50%** across engagements |
| Time-to-value acceleration | **60–70%** faster |
| Regulatory frameworks automated | **25+** (HIPAA, GDPR, SOX, CMMC, FERPA, FedRAMP, DORA...) |
| Token efficiency improvement | **31%** over baseline (900 vs. 1,311 tokens) via scope-driven LLM routing |
| Reusable architecture payoff | Governed platform in production → new client demonstrations assembled, not rebuilt |
| Simultaneous live engagements | **6 industries** in active production |
| Total distinct builds tracked | **13** across 6 industry verticals |
| Team leadership scale | Up to **30 engineers & architects** |

---

## Inflexis Technologies — CTO & Founding Partner

**June 2024 – Present** | Dallas–Fort Worth, TX

> **GitHub Org:** [github.com/Inflexis-ai](https://github.com/Inflexis-ai) &nbsp;·&nbsp; **Platform:** [app.inflexis.ai](https://app.inflexis.ai) &nbsp;·&nbsp; **Docs:** [aixaas-docs](https://github.com/Inflexis-ai/aixaas-docs) &nbsp;·&nbsp; **API Examples:** [mao-examples](https://github.com/Inflexis-ai/mao-examples)

Inflexis Technologies is an AI platform company. I am the CTO and Founding Partner — owning all platform architecture, engineering roadmap, cloud infrastructure, and client technical delivery. We build **AIXaaS™** (AI-as-a-Service), a production-grade, multi-tenant AI orchestration operating system that standardizes and automates complex enterprise AI execution, with deterministic governance built in from the ground up.

### AIXaaS™ Product Suite

| Product | Description | Status |
|---------|-------------|--------|
| **MAO Platform** | Core AIXaaS™ engine — Multi-Agent Orchestration; 10-layer agentic architecture, governed RAG, 5 specialized agents, full audit trail | Production |
| **Axiom** | AIXaaS™ product line — active platform development | In Development |
| **Atlas** | AIXaaS™ product line — active platform development | In Development |
| **Sentinel** | AIXaaS™ product line — active platform development | In Development |
| **Business Communication Intelligence** | AI-powered email and meeting intelligence — transcript analysis, SPICED-scored meeting summaries, pipeline signal extraction from company communications | Active Development |

### Platform Architecture Highlights

- **10-layer architecture:** ingestion → compliance scan → retrieval → orchestration → agent execution → observability → governance → approval gates → output → audit trail
- **Compliance engine:** 25+ regulatory frameworks (HIPAA, GDPR, SOX, CMMC, FERPA, FedRAMP, DORA, PCI-DSS) — deterministic zero-token enforcement, no LLM inference overhead on compliance decisions
- **5 specialized agents:** Dispatcher, Data Ingest, Query Executor, Feedback/ADR, Compliance Validator
- **3-tier hybrid vector storage:** keyword fallback + semantic + cloud (Pinecone / pgvector / OpenSearch) with automatic tier failover
- **Universal ingestion pipeline:** 20+ file formats — PDF, DOCX, audio, video, structured data, web
- **Multi-cloud:** Azure Container Apps (production) + AWS Bedrock-compatible architecture
- **Identity & access:** Entra ID SSO, 8-role RBAC, IAM/ABAC tenant isolation, zero-trust architecture
- **Air-gapped deployment:** offline LLM support via Ollama, local vector stores, no external API dependencies for regulated environments
- **Tech Stack Analyzer:** AI-powered intake tool that maps a client’s existing platform to AIXaaS™ integration patterns and consolidation opportunities — integrated into the AI Intel intelligence dashboard; the engine behind published work like *The Placement Problem*
- **MCP Server integration:** 8 tools exposed for Claude Desktop and AI agent connections
- **Observability:** Application Insights, budget guardrails, loop-cap enforcement, evaluation pipelines, cost-aware routing across 6 LLM providers
- **Semantic caching:** 30–60% cost reduction; 100% deterministic rate on analytical queries

### Active Development Workspace

| Repository | Access | Description | Last Active |
|------------|--------|-------------|-------------|
| [InflexisTechnologies](https://github.com/Inflexis-ai/InflexisTechnologies) | Private | Main platform repo — AIXaaS™ OS, Axiom, Atlas, Sentinel | May 2026 |
| [mao-platform](https://github.com/Inflexis-ai/mao-platform) | Private | Core MAO engine — proprietary Python platform | May 2026 |
| [AIXaaS](https://github.com/Inflexis-ai/AIXaaS) | Private | Platform portal, pipeline, and architecture | May 2026 |
| [Messaging-Meeting-Intelligence](https://github.com/Inflexis-ai/Messaging-Meeting-Intelligence) | Private | Business communication intelligence — email + meeting transcript analysis, SPICED scoring, pipeline signals | May 2026 |
| [team-workspace](https://github.com/Inflexis-ai/team-workspace) | Private | Team collaboration — marketing, revenue, design; AI Intel collector (weekly briefings, benchmarks, RAG research); 11-workstream MLOps platform architecture | May 2026 |
| [aixaas-docs](https://github.com/Inflexis-ai/aixaas-docs) | **Public** | AIXaaS™ platform documentation | Apr 2026 |
| [mao-examples](https://github.com/Inflexis-ai/mao-examples) | **Public** | Python + Jupyter REST API integration examples | May 2026 |

### What MAO Replaces or Consolidates

| Category | Tools Replaced / Consolidated |
|----------|-------------------------------|
| CRM Intelligence | Salesforce Einstein, HubSpot AI, AgentForce, Creatio |
| Document & Knowledge Management | SharePoint AI, Notion AI, Guru, Confluence |
| Workflow Automation | Zapier, Power Automate, Make, AWS Step Functions flows |
| Business Intelligence | Power BI Copilot, Tableau GPT, Sisense |
| Customer Support AI | Intercom AI, Zendesk AI, ServiceNow |
| Compliance & Risk | Manual GRC workflows, Bedrock Guardrails |
| Field & Industrial | OT/SCADA data interpreters, industrial telemetry assistants |
| Meeting Intelligence | Teams Copilot, Otter.ai — SPICED-scored transcription and delivery |

---

## Active Builds & Published Case Studies

**13 distinct builds across 6 industry verticals — client names withheld per confidentiality agreements.** Six are active architecture engagements in current production; seven are completed deployments written up as published case studies.

---

### Enterprise Facilities Management AI — Fortune-class Transportation Campus
**Industry:** Enterprise / Facilities Management / Logistics &nbsp;|&nbsp; **Role:** AI Systems Architect

Designed and prototyped a 5-layer Multi-Agent Orchestration system integrating with the **Corrigo enterprise CMMS platform** (Corrigo Enterprise REST API, OAuth 2.0, webhooks) for a Fortune-class transportation campus. The architecture converts the full facilities management workflow — from work order intake to asset lifecycle analysis — into a governed, AI-orchestrated pipeline.

**System Architecture:**

| Layer | Components |
|-------|------------|
| **Input Sources (5)** | Corrigo web portal, Corrigo mobile app, email/phone dispatch, IoT sensors & BAS alerts, PM schedule auto-triggers |
| **MAO Orchestrator** | Central coordinator managing agent state, task routing, and inter-agent communication via Corrigo REST API + webhooks |
| **AI Agents (5)** | Triage Agent (NLP work order classification by trade, priority, SLA tier) · Dispatch Optimizer (tech vs. vendor, skill match, proximity, backlog, cost) · SLA Escalation Agent (proactive breach prevention via webhook monitoring) · PM Compliance Agent (schedule adherence, overdue alerts, recurring WO pre-fill) · Quality & Analytics Agent (repeat failure patterns, vendor scoring, repair vs. replace) |
| **Action Layer (5)** | Work order CRUD via Corrigo REST API · Vendor dispatch via CorrigoPro Network (60K+ service pros, 130+ trades) · Notifications & alerts · Auto-reporting dashboards · Asset lifecycle insights |
| **Metric Outcomes** | ↓ Work order cycle time · ↑ SLA compliance rate · ↓ Cost per work order · ↑ PM completion rate · ↑ Occupant CSAT |

**RAG pattern:** Modular RAG — multi-source retrieval across structured work order data, asset records, vendor performance history, and PM schedules simultaneously. Agentic RAG governs the dispatch optimization layer where the agent reasons across multiple data sources before making assignment decisions.

**Repository:** [flyguytestrun/jll-bnsf-corrigo](https://github.com/FlyguyTestRun/JLL-BNSF-Corrigo) (includes interactive DAG visualization built in React)

---

### Inflexis Enterprise MLOps Platform — 11-Workstream Architecture
**Industry:** Enterprise / AI Infrastructure &nbsp;|&nbsp; **Role:** Lead Architect

Complete design and architecture of a 12-week enterprise MLOps platform spanning 11 workstreams. Multi-industry parameterization: single codebase, industry-specific configs — adds a new industry vertical in <1 day vs. months of recoding.

| Workstream | Function |
|-----------|----------|
| WS1: Feature Engineering | Data ingestion, feature store with time-travel, multi-industry parameterization |
| WS2: Model Training | Experiment tracking, model registry, validation gates |
| WS3: Inference Engine | Model serving, <100ms p99 latency, 1000+ req/sec |
| WS4: Monitoring | Drift detection <1 hour, automated alerting |
| WS5: Retraining | Auto-triggered retraining, <4 hour end-to-end, <5 min rollback |
| WS6: CI/CD | Canary deployments, 24-48 hour monitoring, 100% automated testing |
| WS7: Multi-Tenant | Complete data isolation, <1 day to add industry |
| WS8: RAG Knowledge | Intelligence layer, context for agents |
| WS9: Agents + ABAC | Agent orchestration with Attribute-Based Access Control |
| WS10: Cost/Scaling | <10% cost vs. naïve approach, budget guardrails |
| WS11: Portfolio | Public showcase, investor/recruiter documentation |

**Security model:** ABAC (Attribute-Based Access Control) — every agent action is authenticated, authorized, approved (if high-impact), audit-logged, then executed or denied with reason. More granular than RBAC; supports fine-grained scoping for multi-tenant agent environments.

---

### Business Communication Intelligence Platform
**Industry:** Enterprise / Business Operations &nbsp;|&nbsp; **Role:** Architect & Builder

AI-powered intelligence system processing company business communications — email threads and meeting transcripts — to surface patterns, pipeline signals, and actionable intelligence.

- **SPICED-scored meeting analysis:** Situation, Pain, Impact, Critical Event, Decision — every sales and strategy meeting scored and summarized automatically
- **Email intelligence pipeline:** governed ingestion of business email corpus; RAG-powered retrieval over communication history for context-aware analysis
- **Integration with AI Intel dashboard:** communication signals feed into the weekly AI intelligence briefing and Tech Stack Analyzer, creating a unified intelligence loop
- **Agentic RAG foundation:** the automation pipeline uses agentic RAG — the agent plans what to retrieve from email/meeting history before composing summaries, ensuring context relevance rather than naive keyword retrieval
- **PHI/PII governance:** all communications governed before any LLM processing — sensitivity classification enforced at ingestion

**Status:** Active development | **Repo:** [Messaging-Meeting-Intelligence](https://github.com/Inflexis-ai/Messaging-Meeting-Intelligence) (private)

---

### Automotive Safety Intelligence Platform
**Industry:** Industrial / Automotive Safety &nbsp;|&nbsp; **Role:** Lead AI Architect

AI-driven threat detection and real-time monitoring for safety-critical OT systems. Multi-agent pipeline with deterministic compliance enforcement (zero-token guardrail layer), air-gapped deployment, and hardware license-lock IP protection. Containerized orchestration via REST API contract.

---

### Zero-Trust Security Intelligence Platform
**Industry:** Enterprise Cybersecurity &nbsp;|&nbsp; **Role:** Platform Architect

Autonomous threat classification and policy enforcement over a proprietary threat intelligence corpus. Hybrid vector + keyword RAG with reranking and citation grounding. IAM/ABAC access controls and full audit trail — scoped for commercial enterprise and DOD deployment.

---

### Government Contractor Workflow Intelligence Platform
**Industry:** Federal / GovTech &nbsp;|&nbsp; **Role:** Lead AI Architect

Integrated calling system with AI-assisted call intelligence, transcript analysis, and summary agents. RAG-powered contract and procurement retrieval with citation grounding. Human-in-the-loop approval gates, durable execution model, and FAR/DFARS compliance alignment.

---

### Restaurant Chain AI Operations Platform
**Industry:** Food Service / Restaurant Technology &nbsp;|&nbsp; **Role:** Full-Stack AI Architect

Real-time inventory management, competitive pricing intelligence, and demand forecasting with native POS integration across multiple locations. Active pricing agent with margin guardrails and external signal processing.

---

### K-12 District AI Architecture Program
**Industry:** Education / EdTech &nbsp;|&nbsp; **Role:** AI Strategy Architect

State-wide ISD AI architecture roadmap spanning multiple districts. Student data governance framework, FERPA/CIPA compliance controls, and phased multi-district adoption sequencing. Delivered stakeholder briefings and architecture documentation to district leadership.

---

### Published Case Study Builds

Seven additional deployments completed and published as anonymized case studies — spanning healthcare, food service, SMB, and sports/media verticals:

| Case Study | Industry | Build Focus |
|-----------|----------|-------------|
| **EdMandate** | Education / EdTech | Multi-district AI architecture, FERPA/CIPA-governed |
| **FedShark** | Federal / GovTech | GovCon contract intelligence, FAR/DFARS compliance |
| **Frenos** | Food Service / Restaurant | POS-integrated AI operations, pricing intelligence |
| **Solo Trades** | SMB / Field Operations | AI workflows for small-to-mid field service businesses |
| **Therapeutic AI Companion** | Healthcare / Mental Health | RAG-powered journaling and guided therapeutic support; HIPAA-governed |
| **Scalable F&B Franchise AI Architecture** | Food Service / Hospitality | AI infrastructure design for a scalable franchise startup — inventory intelligence, demand forecasting, and operational workflow automation architected for multi-location franchise expansion. Role: AI Architect & systems designer. |
| **Athlete Legacy & AI Persona** | Sports / Personal Brand | AI persona architecture and legacy content management |

---

## Thought Leadership & Published Work

Writing and research published through Inflexis Technologies at [inflexis.ai](https://inflexis.ai). Articles draw directly from live platform development, client engagement patterns, and weekly AI intelligence gathered in the Inflexis team workspace. The **Tech Stack Analyzer** — a tool built into the AIXaaS™ AI Intel dashboard — powers much of the analysis behind these articles by mapping enterprise technology landscapes to AIXaaS integration patterns.

### Recent Editorial Articles

| Article | Theme |
|---------|-------|
| **The Harness Is Load-Bearing** | Governance infrastructure is structural — not optional overhead. The compliance layer, audit trail, and enforcement model are what allow AI systems to move fast safely. |
| **The Placement Problem** | Enterprise AI isn’t failing because companies lack access to models — it’s failing because they haven’t solved *where* AI belongs in their workflow architecture and *how* it connects to what they already own. |
| **What Is AIXaaS?** | Platform overview: how the AIXaaS™ orchestration OS works, why it’s different from point solutions, and what governed multi-agent AI actually looks like in production. |
| **The Human Dividend: What AI Deployment Actually Returns** | Making the case that properly deployed, governed AI returns measurable human value — not just cost reduction, but expanded capability, reduced cognitive load, and better decisions at every level. |
| **AI Governance Software Cost in 2026** | Real cost analysis of what enterprise AI governance actually runs — infrastructure, compliance tooling, observability, and operational overhead — versus the cost of not governing. |
| **HIPAA Compliance and AI Data Governance in 2026** | Practical guidance on building AI systems that handle protected health information under current regulatory requirements, with deterministic enforcement patterns. |
| **Enterprise AI and the Silo Problem** *(co-authored)* | Why enterprise AI systems hallucinate and fail: departments are siloed, platforms don’t talk to each other, and AI gets queried against fragmented data it can’t reconcile. The integration layer — not the model — is where enterprise AI succeeds or collapses. |

---

## AI Intel Collector — Weekly Industry Intelligence & Automated Pipeline

Active in the private [Inflexis team workspace](https://github.com/Inflexis-ai/team-workspace), the AI Intel system tracks the enterprise AI landscape on a rolling weekly cadence — and is itself an example of the agentic RAG pipeline design philosophy at work.

**How the pipeline works:**
The AI Intel collector mines a structured feed of vetted AI industry sources (`ai-intel/sources.json`) on a weekly cycle. The resulting intelligence — model releases, regulatory developments, benchmark results, platform shifts, competitive signals — flows into the **Tech Stack Analyzer** tool within the AIXaaS™ dashboard. The Tech Stack Analyzer applies agentic RAG: the agent reasons across the incoming intelligence against the client’s current technology environment to surface integration opportunities, consolidation candidates, and risk alerts.

This is not a news aggregator. It is an **agentic intelligence pipeline** where retrieval, analysis, and output are all governed and purposeful:

- **Weekly briefings** (Apr–May 2026): market signals, model releases, competitive shifts, governance developments
- **Platform benchmarks:** head-to-head performance comparisons across AI platforms and deployment patterns, run against live sandbox metrics
- **RAG evaluation research:** ongoing work on retrieval quality, reranking approaches, and grounding patterns — directly informs AIXaaS™ production RAG selection decisions
- **Tech Stack Analyzer:** architecture evaluation engine fed by AI Intel; maps enterprise technology landscapes to AIXaaS integration patterns; the analysis behind published articles like *The Placement Problem*
- **Sources:** structured feed of vetted AI industry sources tracked in `ai-intel/sources.json` (benchmarks, best-practices, weekly, dashboard sub-modules)

---

## Personal Portfolio Projects

### Advanced AI Tooling & Configuration

Production-hardened AI configuration system built over 10+ months of devops testing, daily use building real products. Specialized routing system, conservative tokenization and controlled orchestration to subagents, hooks, skills, and MCP integrations — developed and refined while building Inflexis production systems. Achieves 2–10x workflow efficiency through systematic command organization, hierarchical configuration, and agent-to-agent orchestration patterns.

**Technologies:** Claude Code CLI, MCP servers, agentic orchestration, automation hooks

---

### [AI Practitioner Guild](https://github.com/FlyguyTestRun/AI-practitioner-guild)

Open collaboration workspace for AIXaaS and CoreSkills4AI practitioners — architecture guides, workflow templates, and production-grade AI engineering patterns. Bridges training-level knowledge with real-world production deployment.

---

### [ISD Systems Showcase](https://github.com/FlyguyTestRun/ISD-Showcase)

Enterprise infrastructure design for K-12 district environments — identity management (Azure AD / Entra ID / AD DS), network segmentation (CIPA/FERPA aligned), and PowerShell automation at scale.

**Technologies:** PowerShell, Azure AD, Entra ID, Intune MDM, AD DS, DHCP/DNS, VLAN segmentation, Veeam, Dell iDRAC

---

### [CoreSkills4AI Training Platform](https://github.com/FlyguyTestRun/CoreSkills4AI)

25+ production-ready AI and infrastructure training modules covering Docker microservices, RAG systems, agentic AI engineering, safe AI guardrails, and enterprise automation — built from real production patterns, not toy examples. Includes application frontend UI/UX.

**Technologies:** Docker, Python (FastAPI), PowerShell, PostgreSQL, Redis, Grafana

---

## Career Timeline

| Period | Role | Organization |
|--------|------|--------------|
| **June 2024 – Present** | AI/ML OS Architecture & CTO | Inflexis Technologies, DFW |
| **June 2013 – June 2024** | Principal Systems Architect & Consultant | Trial IT Services, LLC, Dallas |
| **2008 – 2013** | IT Systems Lead | E&F Legal Production, DFW |

**Trial IT Services — 11 years:** Owned architecture and delivery of enterprise infrastructure, cloud, and security systems across regulated industries. Designed hybrid cloud environments across Azure, AWS, GCP, and on-prem. Implemented zero-trust security frameworks, IAM policies, DevSecOps-aligned pipelines, and Python/PowerShell automation frameworks. Served as primary technical advisor to executive stakeholders across legal, construction, and professional services clients.

**E&F Legal Production — 5 years:** Built high-performance trial infrastructure and workflow automation systems. Designed a psychological assessment platform for jury analysis that reduced preparation time by 90% and enabled real-time pattern recognition and personality profiling — turning manual jury selection research into an API-driven automation pipeline for trial teams nationwide.

---

## Core Technical Capabilities

| Domain | Capabilities |
|--------|--------------|
| **Agentic AI & Orchestration** | Multi-agent DAG pipelines, human-in-the-loop, durable workflows (pause/resume), Bedrock Agents, tool/function calling, MCP architectures, dynamic agent routing |
| **RAG Architecture & Selection** | Naive, Advanced, Hybrid, Modular, Graph, Agentic, Corrective (CRAG), Self-RAG, Speculative RAG — pattern selection by corpus structure, latency budget, retrieval risk, and query complexity |
| **LLM Selection & Routing** | Scope-driven routing across 6 providers; Opus/Frontier-tier for complex reasoning; Sonnet/Production-tier for standard inference; Haiku/Lightweight for high-volume triage; on-premise (Llama, Mistral) for air-gapped; domain-specific models (Whisper, LLaVA, CodeLlama) for specialized tasks |
| **API Bridging & Integration** | OAuth 2.0 / OIDC, REST + webhooks, HL7 FHIR R4, SMART on FHIR, X12 EDI, CMMS/ERP overlay architecture, multi-system MAO orchestration, legacy system integration without platform replacement |
| **Data Migration & Vector Readiness** | Corpus audit, quality gates, chunking strategy selection (fixed/semantic/hierarchical), metadata enrichment, deduplication/versioning, embedding model selection, HNSW/IVF/flat index architecture, training-serving consistency, 3-tier failover validation |
| **Cloud — Azure** | Container Apps, Entra ID, Key Vault, App Insights, ACR, Azure Files, Azure SQL |
| **Cloud — AWS** | Bedrock (Agents, Knowledge Bases, Guardrails, Flows), Lambda, Step Functions, EventBridge, S3, Aurora, OpenSearch, DynamoDB, ECS/EKS |
| **Governance & Compliance** | 25+ frameworks, zero-token PII detection, IAM/ABAC, zero-trust, audit trails, ADR change control, air-gapped deployment |
| **Development** | Python (FastAPI, async) · PowerShell · REST APIs · GitHub Actions CI/CD · Docker · React |
| **Vector Databases** | Pinecone, Qdrant, pgvector, OpenSearch, local semantic fallback |
| **Observability** | Application Insights, Grafana/Prometheus, evaluation pipelines, budget guardrails, A/B testing, semantic caching |
| **Revenue & Operations AI** | Revenue cycle AI, RCM billing pipeline automation, employer billing workflow design, demand forecasting, overhead reduction through agentic automation, SPICED-scored pipeline intelligence |

---

## Education

**Engineering & Business** | University of Texas at Arlington | December 2010  
*Relevant coursework: Computer Science, Data Management, Project Management, Structural Analysis, Engineering Principles*

---

## Full Detailed Resume

**[Bryan Shaw — Full Resume with Complete Experience & Engagement Details →](./resume/Bryan-Shaw-Resume.md)**

---

## Contact

| | |
|---|---|
| **Email** | [BryanJShaw@gmail.com](mailto:BryanJShaw@gmail.com) |
| **Phone** | 817-653-5656 |
| **LinkedIn** | [linkedin.com/in/bryan-shaw-45a23124](https://www.linkedin.com/in/bryan-shaw-45a23124/) |
| **GitHub Personal** | [github.com/FlyguyTestRun](https://github.com/FlyguyTestRun) |
| **GitHub Org** | [github.com/Inflexis-ai](https://github.com/Inflexis-ai) |
| **Platform** | [app.inflexis.ai](https://app.inflexis.ai) |
| **Platform Docs** | [github.com/Inflexis-ai/aixaas-docs](https://github.com/Inflexis-ai/aixaas-docs) |

---

*Updated: May 2026*
