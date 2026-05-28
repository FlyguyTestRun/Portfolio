# Interview Preparation — VP, Artificial Intelligence
## Concentra | Job ID: 348092 | Addison, TX

---

## The Narrative Framework

**One sentence you own throughout every interview:**
> *"I've spent the last several years solving the hardest part of enterprise AI — making it trustworthy in regulated environments — and now I want to apply that governance architecture where the stakes are highest: improving health outcomes for America's workforce."*

**Three pillars to reinforce constantly:**
1. **Governance-first** — I don't deploy AI and then add governance. Governance is the load-bearing structure.
2. **Measurable outcomes** — Every AI initiative I've led has produced specific, quantifiable clinical, operational, or financial results.
3. **Healthcare regulatory literacy** — HIPAA isn't a checkbox I've visited. It's baked into production systems I've personally built.

---

## Company Research — What You Need to Know About Concentra

| Topic | Key Facts |
|-------|----------|
| **Company** | Nation's largest occupational health company, 40+ years, dedicated to improving health of America's workforce |
| **Mission** | Exceptional service to employers, exceptional care to their employees |
| **Location** | HQ: Addison, TX (your backyard — DFW local advantage) |
| **Services** | Occupational medicine, urgent care, physical therapy, employer services, drug testing, wellness programs |
| **Scale** | Hundreds of centers nationally, thousands of clinical and administrative staff |
| **Data environment** | EHR systems, employer reporting systems, billing/revenue cycle, scheduling, workforce management |
| **AI opportunity** | Clinical decision support, revenue cycle optimization, workforce scheduling, predictive injury patterns, patient experience, employer analytics |
| **Regulatory landscape** | HIPAA (primary), state workers' comp laws, drug testing regulations, employer privacy obligations, FDA AI/ML guidance for clinical tools |

**Research to do before the interview:**
- Review Concentra's most recent press releases and news (acquisitions, partnerships, technology investments)
- Search for any published AI or digital transformation initiatives from Concentra leadership
- Understand the occupational health regulatory environment (OSHA recordkeeping, employer reporting requirements, workers' comp data flows)
- Review FDA's 2021 AI/ML-Based Software as a Medical Device Action Plan and any 2024-2026 updates
- Study Concentra's current executive leadership team (who will be in the room)

---

## Interview Rounds — Expected Structure

| Round | Likely Participants | Focus |
|-------|--------------------|---------|
| Round 1 | HR / Talent Acquisition | Role fit, compensation, timeline, culture |
| Round 2 | CIO or CTO | Technical AI strategy, governance, platform decisions |
| Round 3 | CMO or Chief Medical Officer | Clinical AI safety, patient outcomes, responsible AI |
| Round 4 | CEO / COO | Strategic vision, ROI, organizational leadership |
| Final | Executive panel + possibly board members | AI strategy presentation |

---

## Question Bank — With Prepared Answers

### Section 1: Strategy & Vision

**Q: Walk me through how you would approach defining Concentra's AI strategy.**

> Start with the business outcome, not the technology. Concentra's mission is to improve the health of America's workforce. AI strategy should be evaluated entirely through that lens. My first 30 days would be discovery — understanding Concentra's clinical workflows, existing data infrastructure, current AI experiments, and the regulatory constraints specific to occupational health. From there, I'd build a prioritized AI portfolio using a four-axis evaluation: clinical/operational impact, data readiness, regulatory risk, and implementation feasibility. The strategy is not about deploying the most AI — it's about deploying the right AI, in the right sequence, with governance built in from the start. In healthcare, a failed AI initiative doesn't just waste money — it can damage patient trust and create liability.

**Q: What does responsible AI mean to you in a healthcare context?**

> Responsible AI in healthcare means that patient safety is the non-negotiable constraint — not a consideration. In practice, that means three things: First, governance is structural — compliance enforcement, PHI handling, and audit trails are built into the architecture before a single patient touches the system, not added after launch. Second, explainability is a requirement — a clinician needs to understand why an AI recommendation was made, especially for anything that touches care decisions. And third, human-in-the-loop gates are mandatory for high-risk decisions — AI augments clinical judgment, it does not replace it. What I've built at Inflexis is a deterministic compliance engine where PHI never reaches an LLM inference call unless it's been through a governed, audited, authorized pipeline. That same principle applies to every clinical AI system Concentra would build.

**Q: How do you prioritize an AI portfolio when there are more opportunities than resources?**

> Four-axis evaluation matrix: impact (clinical outcomes, operational efficiency, revenue), data readiness (is the data clean, governed, and accessible?), regulatory risk (HIPAA implications, FDA guidance applicability, liability), and implementation speed (time-to-value). I would plot every proposed AI initiative on this matrix and sequence the portfolio to lead with high-impact, data-ready, low-risk pilots that produce measurable wins quickly — building organizational confidence and board-level support while the longer-horizon, higher-complexity initiatives get the data and governance infrastructure they need. In occupational health specifically, I'd prioritize use cases where AI augments employer reporting accuracy, reduces injury claim cycle time, and improves scheduling efficiency — those are areas with measurable ROI and relatively low clinical risk, which makes them ideal first-wave pilots.

---

### Section 2: Healthcare AI & Regulatory Compliance

**Q: Walk me through your HIPAA experience as it relates to AI.**

> HIPAA compliance is not something I advise on — it's something I've built into production systems. The AIXaaS™ platform I architected has zero-token PHI detection: protected health information is identified and governed before it reaches any LLM call. If data isn't cleared through the compliance pipeline, it doesn't move forward — not because of a policy document, but because the system physically prevents it. I've deployed a healthcare AI system — a HIPAA-governed therapeutic support platform — and I've written practitioner-level guidance on HIPAA AI data governance that's published and publicly available. The specific HIPAA considerations for occupational health are interesting: employer-employee data has a dual-party relationship. The employer is often a covered entity or business associate, the patient has privacy rights, and there are specific carve-outs for workplace injury data under HIPAA. I'd want to map those distinctions carefully in the first 30 days.

**Q: What's your understanding of FDA guidance on AI/ML-based software in clinical settings?**

> The FDA's 2021 AI/ML-Based Software as a Medical Device Action Plan established the regulatory framework for AI that supports clinical decision-making. The key distinction for occupational health AI is whether a system constitutes a Software as a Medical Device (SaMD) — which triggers the full FDA regulatory pathway — or whether it's administrative AI that augments workflows without making diagnostic or treatment recommendations. Most occupational health AI use cases I'd prioritize — scheduling optimization, employer reporting, injury pattern analytics, revenue cycle — fall clearly outside the SaMD threshold. The areas to be careful about are any AI that influences clinical decisions: injury severity classification, return-to-work recommendations, or diagnostic support. Those would require close partnership with clinical leadership and legal to determine the appropriate regulatory posture. I've actively tracked FDA guidance updates and would make monitoring the evolving AI/ML regulatory landscape a standing responsibility of this role.

**Q: How do you handle AI bias in a clinical context?**

> Bias in clinical AI can cause real harm — under-triaging certain patient populations, skewing return-to-work timelines, or producing inequitable recommendations across employer segments. My approach has three components: detection, testing, and ongoing monitoring. Before deployment, every model undergoes bias testing across demographic dimensions relevant to the patient population. I mandate explainability requirements so that model outputs can be interrogated, not just accepted. And after deployment, I maintain evaluation pipelines that continuously compare model performance across patient cohorts — with automated alerts when drift or disparity is detected. In a workforce health context, I'd specifically test for disparities across employer industry, geography, age, and injury type. The governance framework defines what acceptable performance looks like before a model goes live, not after someone notices a problem.

**Q: How do you stay current on the healthcare AI regulatory landscape?**

> I run a weekly AI intelligence collection process that tracks regulatory developments, model releases, platform benchmarks, and competitive shifts. I'd extend that specifically into healthcare AI regulatory monitoring as VP — tracking FDA guidance updates, state AI legislation (several states now have healthcare AI bills in progress), HIPAA enforcement actions involving AI vendors, and CMS reimbursement developments related to AI-assisted care. I'd establish a formal regulatory monitoring function within the AI team, with quarterly briefings to the compliance and legal teams, and an escalation path to the Chief Compliance Officer for anything that requires immediate organizational response.

---

### Section 3: Governance, Ethics & Risk Management

**Q: Describe how you've built an AI governance framework from scratch.**

> The AIXaaS™ governance framework started with a foundational question: what would have to be true for this system to be deployed safely in the most regulated environment we can imagine? That led to a 10-layer architecture where governance isn't a layer — it IS the structure. The key components I built: a deterministic compliance engine (25+ regulatory frameworks, zero reliance on LLM inference for enforcement decisions — the system doesn't ask an AI if something is HIPAA-compliant, it enforces it mechanically), human-in-the-loop approval gates for high-risk decisions, ADR (Architecture Decision Record) change control so every modification to model configuration, prompts, or retrieval pipelines is audited and approved before production, full audit trails that produce evidence acceptable for regulatory review, and an AI risk classification system that determines the review and approval process required based on clinical risk level. For Concentra, I'd adapt that framework specifically to occupational health — mapping the HIPAA requirements, FDA guidance thresholds, and employer data obligations into a governance policy that every AI initiative passes through before deployment.

**Q: Tell me about a time you said no to an AI initiative because of risk.**

> In one of our federal government contractor engagements, the client wanted to use AI to automate procurement decisions — routing contract awards based on AI-scored vendor assessments. The ROI case was strong. But when we mapped the regulatory exposure, we found the approach created FAR/DFARS compliance risk, lacked the audit trail required for federal procurement oversight, and introduced bias risk across vendor categories in a way we couldn't adequately test without a 6-month validation period. I recommended against it and proposed an alternative: AI as decision-support — surfacing ranked vendor assessments with explicit confidence scores and citations, with human contracting officers making final award decisions. That alternative passed regulatory review, launched on time, and the client got 80% of the productivity benefit with none of the compliance exposure. The rule I apply: if governance can't be built correctly before launch, the launch date moves — not the governance.

**Q: How do you manage AI vendor risk?**

> Vendor AI risk management has four dimensions. First, regulatory compliance: does the vendor have a signed BAA, do their data practices meet HIPAA requirements, where does data go for training, and what's their data retention policy? For AI vendors handling PHI, this is non-negotiable. Second, technical governance: does the vendor provide explainability, audit logs, and model version transparency? Can we validate model behavior before it touches our patient data? Third, concentration risk: if a vendor goes down or changes pricing, what's the business continuity plan? I've built multi-vendor AI architectures specifically to avoid single-vendor dependency. Fourth, market monitoring: the AI vendor landscape is moving fast, and a vendor that looks like the right choice today may be surpassed in 12 months. I maintain ongoing competitive monitoring so vendor relationships are governed by outcomes, not inertia.

---

### Section 4: AI Adoption & Change Management

**Q: How do you drive AI adoption across a workforce that includes both clinical and non-clinical staff?**

> The clinical and non-clinical adoption challenges are genuinely different, so I treat them separately. For clinical staff, the primary barrier is trust — clinicians need to understand what the AI can and cannot do, where its limitations are, and that it's augmenting their judgment, not replacing it. The adoption program for clinical staff is built on transparency: show the training data, show the error rates, show how the system flags uncertainty. For non-clinical staff — revenue cycle, scheduling, operations — the barrier is usually workflow disruption. The adoption approach there is workflow-first: AI gets embedded into the tools people already use, with minimal friction, and the benefit has to be visible within their first week of use. I've run multi-district AI adoption programs in K-12 environments — a comparably heterogeneous audience — and the pattern that works is: simple wins first, visible benefit, champion networks within each department, and consistent communication from senior leadership that AI is a tool they're being given, not a threat to their role.

**Q: How do you build AI literacy across a large organization?**

> I built CoreSkills4AI — a 25+ module AI training platform that covers everything from production AI engineering to safe deployment and governance — specifically to address the AI literacy gap in enterprise organizations. For Concentra, I'd design a tiered AI literacy program: executive literacy (what AI can do, what it can't, how to govern it, how to read AI performance metrics), clinical literacy (how AI supports care decisions, when to trust it, when to escalate, how to report issues), operational literacy (how to use AI tools embedded in their workflows, data hygiene responsibilities), and technical depth for the AI team (model evaluation, bias testing, prompt engineering, governance implementation). The program runs continuously — not as a one-time training event — with quarterly updates as AI capabilities evolve.

**Q: How do you handle resistance to AI from clinical staff?**

> Resistance from clinical staff is legitimate and should be taken seriously, not overcome. It usually comes from three sources: concern about accuracy (will this system hurt my patients?), concern about autonomy (will this system replace my judgment?), or concern about accountability (if the AI is wrong and I follow it, who is responsible?). My approach is to address each of these directly. On accuracy: I publish performance metrics openly — sensitivity, specificity, false positive rates — and I build in uncertainty flagging so the system tells the clinician when it's not confident. On autonomy: human-in-the-loop is the design principle, not the exception. The AI surfaces options; the clinician decides. On accountability: the governance framework explicitly documents that clinical decision authority remains with the licensed clinician — the AI is a tool, like a lab result or an imaging system. Getting clinical champions involved early — finding physicians and nurses who want to be part of the AI design process — converts skeptics to advocates faster than any top-down mandate.

---

### Section 5: Leadership & Team Building

**Q: How would you build the AI team at Concentra?**

> The VP AI role is an organizational build — I'd be designing the team structure before hiring the first role. My recommended structure: a core AI engineering team (ML engineers, data scientists, AI platform engineers), an AI product management function (AI PMs who translate clinical and operational needs into AI product requirements), an AI governance function (responsible AI, bias testing, regulatory monitoring), and embedded AI implementation leads who sit with clinical and operational teams to drive adoption. I'd sequence hiring around the AI portfolio priorities — the first hires support the highest-value use cases. For Concentra specifically, I'd prioritize hiring ML engineers with healthcare data experience and clinical AI product managers who understand EHR workflows and occupational health data structures.

**Q: How do you communicate AI progress to the board?**

> Board-level AI communication has three components: strategic positioning (where is AI in our organizational maturity model, and where are we going?), operational performance (are our AI deployments producing the outcomes we projected?), and risk management (what are the regulatory, operational, and reputational risks of our AI program, and how are they being managed?). I translate everything into business language — not model accuracy percentages, but injury claim cycle time reduction, employer satisfaction scores, revenue cycle improvement, and clinician time saved per patient encounter. For risk, I present a RAG (Red/Amber/Green) portfolio status with the specific governance actions being taken on anything in amber or red. I prepare boards for the AI regulatory landscape — they need to understand that HIPAA enforcement for AI is evolving and that the governance framework we're building is their protection. The goal is to make the board confident that AI at Concentra is an asset that's being managed professionally, not a liability they don't understand.

---

### Section 6: Why Concentra / Culture Fit

**Q: Why Concentra specifically? Why make this move?**

> I've built the governance infrastructure that healthcare AI needs — now I want to apply it where the stakes are highest and the mission is clear. Concentra's mission — improving the health of America's workforce, one patient at a time — is exactly the kind of anchor that makes AI governance feel important rather than bureaucratic. In a startup, you're always justifying the governance investment. Inside an organization where patient safety is the core value, governance isn't overhead — it's mission-critical. That alignment changes what's possible. Beyond mission, the practical context is compelling: Concentra has 40+ years of occupational health data, established employer relationships, clinical expertise, and national scale. Those are the assets that make AI genuinely transformative — not another SaaS vendor selling point solutions, but a governed AI program that compounds on everything Concentra has already built.

**Q: What do you know about occupational health that's relevant to AI?**

> Occupational health operates at a unique intersection: employer obligations, employee rights, clinical care, regulatory compliance, and insurance/compensation systems all overlap in every patient encounter. That complexity creates both the challenge and the opportunity for AI. The data in occupational health is rich — injury patterns by industry, employer, geography, job type — and predictive analytics on that data has enormous value: injury prevention recommendations to employers, return-to-work optimization, drug screening compliance, physical capability matching. The revenue cycle is also distinctive: billing in occupational health involves employer billing, workers' comp billing, and sometimes traditional insurance, with different coding requirements and compliance obligations. AI that helps revenue cycle teams navigate that complexity correctly has direct financial impact. I'd spend my first 30 days with clinical leadership and operations teams learning the workflows in detail — but the governance framework and AI strategy methodology transfer directly from my regulated-industry experience.

**Q: What does success look like at 12 months for you in this role?**

> At 12 months: an AI governance policy is adopted and embedded in how Concentra evaluates every new AI initiative. Two or three AI pilots are in production with published outcomes — measured in clinical, operational, or financial terms, not just technical metrics. An AI literacy program has completed its first cohort and has a waiting list for the second. The AI portfolio is defined, prioritized, and reported to the executive team quarterly. And the board has seen at least one clean AI strategy presentation with enough clarity that they're asking informed questions, not just listening. What I won't do is optimize for vanity metrics — number of AI tools deployed, number of use cases in flight. I'll optimize for AI that Concentra can trust, that produces outcomes you can measure, and that the clinical staff will still be using 18 months after launch.

---

## Questions to Ask Concentra

**For the CIO/CTO:**
- What does Concentra's current data infrastructure look like? Is there a unified data platform, or is data siloed across clinical, billing, and HR systems?
- What AI initiatives are already in flight — either vendor-purchased or internally built — and where have you hit the most friction scaling them?
- What's the relationship between the AI function and the data governance organization?

**For the CMO/Clinical Leadership:**
- How does clinical leadership currently think about the role of AI in occupational care — augmentation or automation?
- Are there specific clinical use cases clinical leaders are excited about, or cautious about?
- How would the AI team get access to clinical workflow expertise for designing AI tools?

**For the CEO/COO:**
- What does the board's current level of AI awareness look like, and are there specific AI risk concerns they've raised?
- Is there an existing AI governance committee or ethics board, or would this VP be building that from scratch?
- What's the organizational appetite for moving fast with AI versus being deliberate and governance-first?

**For HR/Talent:**
- Is there an existing AI team this VP would be inheriting, or is this a build-from-scratch?
- How does this role interface with the Chief Compliance Officer and legal counsel?
- What's the expected balance between internal AI development and AI vendor management?

---

## Compensation & Negotiation Framework

**Market range for VP AI in DFW healthcare:** $250,000–$375,000 base + bonus + equity/LTI

**Your position:** This is a lateral move from CTO of a startup — which means:
- You're trading equity upside for organizational scale, stability, and mission alignment
- You bring a governance framework that would cost Concentra $2M+ to build from scratch
- You're local to Addison, TX (no relocation premium, but worth acknowledging as a fit signal)
- Your published thought leadership and production track record are differentiators, not table stakes

**Anchor to value delivered:** "Based on the outcomes I've produced — collapsing AI implementation timelines from 12 months to weeks, delivering 35–50% operational efficiency improvements — I'm looking for a total compensation package in the range of [X]." Always frame compensation in terms of the value you'll create, not what you need.

---

## Pre-Interview Checklist

- [ ] Read Concentra's most recent news releases and press coverage
- [ ] Review FDA 2021 AI/ML-Based Software as a Medical Device Action Plan (30-min read)
- [ ] Research Concentra's executive leadership team (LinkedIn, Concentra website)
- [ ] Review any recent healthcare AI governance developments (HIPAA enforcement actions, state AI laws)
- [ ] Prepare 2–3 specific examples of measurable AI outcomes you can cite with numbers
- [ ] Practice the one-page version of your HIPAA AI story (under 90 seconds)
- [ ] Prepare 5 specific questions for each interview panel (from list above)
- [ ] Have the 90-day plan ready to walk through if asked
- [ ] Review the AIXaaS platform demos in case they ask for a live walkthrough
- [ ] Confirm you can speak to SOX compliance work specifically (they called it out in qualifications)

---

*This document is Bryan Shaw's private interview preparation — not for distribution.*
