# Bryan Shaw — AI Architect & CTO

**Multi-Agent AI Orchestration | Governed RAG Pipelines | Amazon Bedrock & Claude | Enterprise GenAI Architecture**

**Location:** Dallas–Fort Worth, TX
**Contact:** [BryanJShaw@gmail.com](mailto:BryanJShaw@gmail.com) | 817-653-5656
**LinkedIn:** [linkedin.com/in/bryan-shaw-45a23124](https://www.linkedin.com/in/bryan-shaw-45a23124/)
**GitHub:** [github.com/FlyguyTestRun](https://github.com/FlyguyTestRun/)

---

## Resume 📄 **[View Full Resume](./resume/Bryan-Shaw-Resume.md)**

---

**Professional Summary:**
AI Architect and Platform Engineer with 22+ years of enterprise technology experience. Currently serving as CTO & Founding Partner of an AI platform company — designing, building, and shipping production-grade multi-agent orchestration systems, governed RAG pipelines, compliance automation engines, and agentic AI workflows across cloud-native and air-gapped environments. Hands-on with Amazon Bedrock (Agents, Knowledge Bases, Guardrails), Claude family models, and multi-cloud architecture. Active across six simultaneous client engagements spanning federal, cybersecurity, food service, education, automotive safety, and enterprise SaaS. Recognized for architectural clarity, disciplined execution, and the ability to move from concept to production-deployed system under pressure — including investor-grade MVP delivery in 72 hours.

**Core Competencies:**
- Multi-Agent Orchestration, Agentic AI & Human-in-the-Loop Workflows
- Amazon Bedrock (Agents, Knowledge Bases, Guardrails, Flows) & Claude Model Architecture
- RAG Systems — Hybrid/Vector Retrieval, Chunking, Reranking, Grounding & Citation
- AWS (Lambda, Step Functions, EventBridge, S3, OpenSearch, DynamoDB, ECS/EKS, Aurora)
- Azure (Container Apps, Entra ID, Key Vault, App Insights, ACR)
- Enterprise GenAI Reference Architectures & Reusable Framework Design
- Compliance Automation, AI Governance & Guardrails (IAM/ABAC, KMS, PII Protection)
- LLM Orchestration — Cloud-native, Hybrid, and Offline/Air-Gapped Deployments
- Python (FastAPI, async), PowerShell & Infrastructure-as-Code
- Observability, Evaluation Pipelines, Cost Metrics & Reliability Frameworks

---

## Inflexis — AI Platform Company (CTO & Founding Partner)

> **GitHub Org:** [github.com/Inflexis-ai](https://github.com/Inflexis-ai) | **Platform:** [app.inflexis.ai](https://app.inflexis.ai)
> **Docs:** [Inflexis-ai/aixaas-docs](https://github.com/Inflexis-ai/aixaas-docs) | **API Examples:** [Inflexis-ai/mao-examples](https://github.com/Inflexis-ai/mao-examples)

**Multi-Agent AI Orchestration Platform (AIXaaS™)** | 2025 – Present

Leading all architecture and engineering for a production-grade, multi-tenant AI orchestration platform deployed on Azure and AWS. The platform delivers governed retrieval-augmented generation, zero-token compliance detection across 23 regulatory frameworks, multi-agent workflow orchestration, human-in-the-loop approval gates, and enterprise identity integrations — designed to be platform-agnostic and Bedrock-compatible.

**Platform highlights:**
- 10-layer multi-agent architecture with full audit trail and ADR change control
- 3-tier hybrid vector storage (keyword + semantic + cloud) — compatible with OpenSearch and pgvector patterns
- Zero-token compliance engine with deterministic pattern-matching across 23 regulatory frameworks (HIPAA, GDPR, SOX, CMMC, DORA, FedRAMP, and 17 others) — equivalent to Bedrock Guardrails enforcement model
- Multi-cloud deployment: Azure Container Apps (production) + AWS Bedrock-compatible architecture
- Entra ID SSO + 8-role RBAC; IAM/ABAC-pattern governance across all tenants
- Universal file ingestion pipeline (20+ formats: PDF, DOCX, audio, video, web, structured data)
- Durable workflow orchestration with human-in-the-loop approval gates — Step Functions-equivalent execution model
- 5 specialized agents: Dispatcher, Data Ingest, Query Executor, Feedback/ADR, Compliance Validator
- 31% token efficiency improvement over baseline (900 tokens vs 1,311); 100% deterministic rate for analytical queries
- Cost-aware model routing across 6 LLM providers; semantic caching (30–60% cost reduction)
- Application Insights observability, budget guardrails, loop-cap enforcement, and evaluation pipelines
- Offline/air-gapped deployment architecture for regulated and government environments
- MCP Server integration — 8 tools exposed for Claude Desktop and AI agent connections

---

### The Enterprise AI Problem We Solve

Most enterprises aren't failing at AI because they lack access to the technology — they're failing because they're accumulating *more* AI tools without a coherent strategy to govern, connect, or extract value from them.

The organizations successfully riding the AI wave share one thing: they stopped treating AI as a collection of individual tools and started treating it as a **governed orchestration layer** — an intelligent nervous system that sits on top of what they already own and makes it smarter.

**What MAO replaces or consolidates:**

| Category | Commonly Replaced / Consolidated |
|---|---|
| CRM Intelligence | Salesforce Einstein, HubSpot AI, Creatio, AgentForce |
| Document & Knowledge Mgmt | SharePoint AI, Notion AI, Guru, Confluence |
| Workflow Automation | Zapier, Power Automate, Make, AWS Step Functions flows |
| Business Intelligence | Power BI Copilot, Tableau GPT, Sisense |
| Customer Support AI | Intercom AI, Zendesk AI, ServiceNow |
| Compliance & Risk | Manual review workflows, GRC platforms, Bedrock Guardrails |
| Field & Industrial | OT/SCADA data interpreters, industrial telemetry assistants |
| Meeting Intelligence | Teams Copilot, Otter.ai — SPICED-scored transcription and delivery |

**Integration architecture — platform-agnostic by design:**

MAO connects to existing systems via REST API, webhooks, and structured data pipelines — then adds the intelligence layer those platforms are missing: governed RAG retrieval, multi-agent reasoning, compliance validation, and explainable audit trails.

Current integration targets in active development:
- **Microsoft 365 + SharePoint** — Document intelligence, email summarization, meeting recording analysis on any platform
- **Salesforce / HubSpot / Creatio** — CRM data enrichment, lead intelligence, account briefing agents
- **ERP / Financial Systems** — P&L analysis, variance reporting, pricing intelligence agents
- **CMMS / Field Operations** — Maintenance history querying, work order intelligence, predictive maintenance briefings
- **OT / Industrial Telemetry** — Sensor data ingestion, anomaly narration, incident summary agents
- **POS / Transactional Systems** — Sales pattern analysis, demand forecasting, customer behavior intelligence
- **Custom Internal Systems** — Any system with an API or data export can be onboarded as a MAO knowledge source

**The vision for enterprise leadership:**

The C-suite question is no longer *"Should we do AI?"* — it's *"How do we govern it, trust it, and make it work with everything we've already built?"* MAO was architected specifically to answer that question. Every response is traceable to a source. Every agent action is logged in an ADR. Every compliance flag is deterministic — not probabilistic. And every deployment is configurable to the client's risk tolerance.

---

## Featured Client Engagements

Six active architecture engagements — anonymized per client confidentiality agreements.

---

### Enterprise Workflow Integration Platform — Fortune-class Rail & Commercial Facilities
**Industry: Enterprise / Logistics | Role: Lead AI Architect**

Multi-agent orchestration and governance layer built on top of an enterprise CMMS workflow platform (Corrigo) for a major rail and facilities client. Structured knowledge retrieval over work order history, asset records, and operational data.

- MAO orchestration layer connected to Corrigo API contract — governed RAG over structured work order and asset data
- Multi-agent workflow: ingest → compliance scan → semantic query → structured response with source citations
- ADR-based change control; all agent instruction changes version-controlled and reviewable

---

### Automotive Safety Intelligence Platform
**Industry: Industrial / Automotive Safety | Role: Lead AI Architect**

AI-driven threat detection and real-time monitoring architecture for safety-critical operational technology (OT) systems. Multi-agent pipeline with deterministic compliance enforcement and air-gapped deployment design.

- Multi-agent reasoning over industrial telemetry and adversarial threat corpus
- Deterministic guardrail layer — zero-token compliance without LLM inference overhead
- Containerized orchestration via REST API contract; hardware license-lock IP protection
- Offline/air-gapped deployment for regulated automotive environment

---

### Zero-Trust Security Intelligence Platform
**Industry: Enterprise Cybersecurity | Role: Platform Architect**

Enterprise cybersecurity AI with autonomous threat classification, policy enforcement, and governed RAG over proprietary threat intelligence corpus.

- Hybrid vector + keyword retrieval with reranking and citation grounding
- IAM/ABAC-pattern access controls, PII protection, and full audit trail per retrieval
- Scoped for commercial enterprise and government/DOD deployment scenarios

---

### Government Contractor Workflow Intelligence Platform
**Industry: Federal / GovTech | Role: Lead AI Architect**

Integrated communication, contract intelligence, and workflow automation for a federal government contracting operation.

- Integrated calling system with AI-assisted call intelligence and summary agents
- RAG-powered contract and procurement document retrieval with citation grounding
- Human-in-the-loop approval gates; durable execution model for regulated workflow steps
- Federal compliance alignment: FAR/DFARS, audit logging, data governance

---

### Restaurant Chain AI Operations Platform
**Industry: Food Service / Restaurant Technology | Role: Full-Stack AI Architect**

Real-time inventory management, active price monitoring, and demand forecasting for a multi-location restaurant chain with native POS integration.

- Native POS API integration — real-time transaction data ingestion across multiple locations
- Active pricing intelligence agent with competitive monitoring and margin guardrails
- Demand forecasting pipeline using historical transaction patterns and external signals

---

### K-12 District AI Architecture Program
**Industry: Education / EdTech | Role: AI Strategy Architect**

State-wide school district AI architecture roadmap spanning multiple ISDs. Student data governance, FERPA/CIPA compliance controls, and phased district adoption framework.

---

### Enterprise AI Knowledge Platform — 72-Hour MVP
**Industry: Enterprise SaaS | Role: CTO / Lead Architect**

Investor-grade AI knowledge platform MVP built and demonstrated in 72 hours for venture capital evaluation. Multi-agent knowledge retrieval, RAG-powered Q&A, and structured output pipelines from zero to live demo.

---

## Portfolio Projects

### [everything-claude-code](https://github.com/FlyguyTestRun/everything-claude-code)
**Complete Claude Code Configuration Collection — Anthropic Hackathon Winner**

Battle-tested Claude Code configuration system built over 10+ months of intensive daily production use building real AI products. Published as a resource for the broader AI engineering community.

- 30+ slash commands, specialized subagents, hooks, skills, and MCP integrations
- Achieves 2–10x productivity gains through systematic command organization and hierarchical configuration
- **Recognized by Anthropic** — configurations published after winning an Anthropic hackathon
- Used by AI engineers and developers worldwide for Claude Code workflow optimization

**Technologies:** Claude Code, MCP servers, agent orchestration, automation hooks

---

### [AI Practitioner Guild](https://github.com/FlyguyTestRun/AI-practitioner-guild)
**Collaborative AI Engineering Community Hub**

Open collaboration workspace for AIXaaS and CoreSkills4AI practitioners — shared resources, architectural patterns, and hands-on AI engineering workflows.

- Collaborative environment for AI practitioners building with production-grade patterns
- Architecture guides, workflow templates, and best-practice references
- Bridges training-level knowledge with real-world production deployment

---

### [ISD Systems Showcase](https://github.com/FlyguyTestRun/ISD-Showcase)
**K-12 Identity Management, Network Segmentation, and Infrastructure Automation**

Enterprise infrastructure design for large educational district environments. Covers identity management, network segmentation, compliance frameworks (CIPA/FERPA), and automation at scale — directly applicable to the K-12 AI Architecture engagements above.

- Identity management workflows: Azure AD, Entra ID, AD DS (dominant stack in most ISDs)
- PowerShell automation for large-scale identity provisioning and device enrollment
- Secure, segmented network topologies aligned to CIPA/FERPA compliance frameworks
- Infrastructure health monitoring, reporting, and alerting dashboards

**Technologies:** PowerShell, Azure AD, Active Directory, Entra ID, Intune MDM, DHCP, DNS, VLAN segmentation, Veeam, Dell iDRAC

---

### [CoreSkills4AI Training Platform](https://github.com/FlyguyTestRun/CoreSkills4AI)
**25+ Production-Ready AI & Infrastructure Training Modules**

Comprehensive training platform spanning enterprise AI architecture, DevOps, and infrastructure. Modules are built from real production patterns — not toy examples.

1. Docker Microservices — 6-container architecture with observability
2. RAG Systems & Vector Databases — production-grade semantic retrieval
3. Agentic AI Engineering — PIV workflow with Claude
4. Building Safe AI Guardrails — deterministic compliance patterns
5. PowerShell Enterprise Automation
6. Entra ID, ADDS, Intune MDM/MAM management
7. Salesforce AgentForce training and integrations
8. Docker Labs — advanced debugging and optimization
9. Semantic Embedding & Vector Databases
10. Systems design and engineering practices

**My scope:** Built advanced coding modules in Python, REST, PowerShell, and Java. Designed and built the application frontend UI/UX.

**Technologies:** Docker, Python (FastAPI), PowerShell, PostgreSQL, Redis, Grafana

---

## Technical Expertise

**Agentic AI & Orchestration:**
- Multi-agent orchestration (DAG pipelines, planning, memory, autonomous and supervised workflows)
- Human-in-the-loop patterns — approval gates, durable execution, pause/resume
- Amazon Bedrock (Agents, Knowledge Bases, Guardrails, Flows) — architecture and deployment patterns
- Claude family models — prompt schema design, adapter patterns, model optimization
- Custom orchestration frameworks built from first principles (LangChain/LangGraph-equivalent)
- Tool/function calling, MCP-based tool architectures, dynamic agent routing

**RAG & Knowledge Systems:**
- End-to-end RAG pipeline design: ingestion, chunking, embedding, indexing, reranking, grounding
- Hybrid/vector retrieval — OpenSearch, pgvector, Pinecone, Qdrant, local semantic fallback
- Citation grounding, source attribution, trust-scored knowledge bases
- Semantic caching, metadata-driven retrieval, enterprise knowledge modeling

**Cloud & Infrastructure:**
- **AWS:** Bedrock, Lambda, Step Functions, EventBridge, S3, Aurora, OpenSearch, DynamoDB, ECS/EKS
- **Azure:** Container Apps, Entra ID, Key Vault, App Insights, ACR, Azure Files
- Docker, containerization, GitHub Actions CI/CD
- Microsoft 365, Active Directory, Intune, Autopilot, VMware, Hyper-V
- Offline/air-gapped deployment for regulated environments

**Governance, Security & Observability:**
- AI guardrails — deterministic compliance, zero-token PII detection, Bedrock Guardrails patterns
- IAM/ABAC-pattern access control, KMS patterns, private networking, zero-trust architecture
- Observability and evaluation pipelines — tracing, cost metrics, A/B testing, fallback strategies
- Compliance automation: HIPAA, GDPR, SOX, CMMC, FERPA, FedRAMP, DORA, and 16 others

**Development:**
- Python (FastAPI, async patterns) — primary language
- PowerShell — enterprise automation and infrastructure-as-code
- REST API design, webhook integration, structured data pipelines

---

## Certifications

- **AZ-104** — Azure Administrator Associate
- **MD-102** — Endpoint Administrator
- **AZ-800/801** — Windows Server Hybrid Administrator *(in progress)*
- **AWS Solutions Architect** — studying; architecture-level proficiency validated through production multi-cloud deployments

---

## Contact

**Email:** BryanJShaw@gmail.com
**Phone:** 817-653-5656
**LinkedIn:** [linkedin.com/in/bryan-shaw-45a23124](https://www.linkedin.com/in/bryan-shaw-45a23124/)
**GitHub Personal:** [github.com/FlyguyTestRun](https://github.com/FlyguyTestRun/)
**GitHub Company:** [github.com/Inflexis-ai](https://github.com/Inflexis-ai)

---

*Portfolio last updated: March 2026*
