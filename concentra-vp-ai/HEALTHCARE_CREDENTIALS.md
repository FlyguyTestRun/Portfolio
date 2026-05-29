# Healthcare AI Credentials — Gap Bridge
## Addressing Identified Gaps | Concentra VP, Artificial Intelligence

> This document fills every healthcare-related gap identified in TECH_ALIGNMENT.md.
> It is not a resume edit — it is interview ammunition and context for the application narrative.
> Two active healthcare deployments, one published HIPAA credential, and a governance architecture
> that maps directly to Concentra's clinical AI requirements.

---

## Why the Gap Is Smaller Than It Looks

The TECH_ALIGNMENT.md scored "Healthcare organization experience" at 8/10 and noted the gap as
"direct clinical org experience." The full picture closes that gap substantially:

| Gap Identified | What Actually Exists |
|----------------|---------------------|
| Direct healthcare AI deployment | Two active healthcare AI builds — one personal, one NDA client |
| Clinical workflow familiarity | Active clinical decision support development requiring deep workflow design |
| FDA AI/ML guidance knowledge | Clinical decision support architecture decisions made in active development |
| HIPAA production depth | Production-grade platform + published thought leadership |
| Patient safety understanding | Clinical diagnostic aid with false-negative harm analysis built into governance |

---

## Healthcare Deployment 1
### Clinical Diagnostic Aid — Neurodevelopmental Assessment Platform
**Status:** Active development &nbsp;|&nbsp; **Client:** Confidential nonprofit healthcare organization (NDA)

> **NDA Note:** Client identity, partner names, and all identifying details are protected.
> This engagement can be described in interviews using the language in this document.
> Do not name the organization, the nonprofit, or any individuals involved.

#### The Problem
Dyslexia affects approximately 15–20% of the population but is chronically underdiagnosed — particularly
in underserved communities — because:
- There are not enough qualified practitioners to handle the diagnostic volume
- Full neuropsychological testing is expensive and inaccessible to many families
- Early signs are frequently missed during standard school or clinical encounters
- The condition often goes undiagnosed into adulthood, compounding its impact on education and employment

A nonprofit healthcare organization backed by a private philanthropist (whose family was personally
affected by late dyslexia diagnosis) engaged Inflexis to build an AI-assisted early detection platform
to help practitioners identify high-probability cases earlier and at lower cost.

#### The Solution
A clinical decision support AI platform that:
- Processes **structured intake assessment forms** capturing behavioral, educational, and developmental indicators
- Analyzes **behavioral observation video data** from monitored patient sessions for clinically-recognized
  visual and auditory processing cues
- **Surfaces pattern indicators** to the practitioner — cueing clinical attention to which specific signs
  are present and their relative significance
- Acts as a **decision-support aid to the diagnostician**, not a diagnostic system — the practitioner
  retains full clinical authority and makes all diagnostic decisions
- Serves patients who cannot afford full neuropsychological workups by providing a governed,
  structured early-screening pathway

#### Why This Maps Directly to Concentra's AI Requirements

| Concentra Requirement | How This Deployment Addresses It |
|----------------------|----------------------------------|
| Clinical decision support AI | This IS clinical decision support — cueing practitioners to indicators, not making diagnoses |
| Clinical workflow familiarity | Designed into the practitioner intake and observation workflow; built around how diagnosticians actually work |
| Patient safety as non-negotiable constraint | False negatives (missed diagnosis) are the primary harm mode; bias detection and sensitivity tuning are structural |
| Bias detection for underserved populations | Core requirement: the system must not underperform for demographics that are already underdiagnosed |
| Explainability requirements | Practitioners need to know which specific indicators triggered the AI flag and why — not just a score |
| Human-in-the-loop mandatory | The AI surfaces patterns; the clinician interprets and decides. Non-negotiable by design |
| PHI governance | Intake forms and observation data contain sensitive developmental health information — full PHI pipeline |
| FDA SaMD considerations | Clinical decision support for non-diagnostic aid; regulatory posture analysis completed for design decisions |
| AI for underserved/access-constrained populations | Explicitly designed for patients who cannot access full-cost testing |

#### Governance Architecture Applied
- **Zero-token PHI handling:** intake and video data governed before any LLM processing
- **Bias testing framework:** sensitivity/specificity analysis across demographic segments; false negative
  rate is the primary metric (a missed flag is more harmful than an extra review)
- **Explainability layer:** every indicator surfaced includes the source signal and clinical reference
- **Human-in-the-loop gate:** the system cannot output a conclusion — it outputs indicators for
  practitioner review
- **Confidence calibration:** outputs include uncertainty signals so practitioners know when the AI
  has low confidence and should apply heightened clinical scrutiny
- **Audit trail:** every intake, every output, every practitioner action is logged for clinical review
  and governance validation

#### How to Talk About This in Interviews

> *"I'm actively deploying clinical decision support AI for a healthcare nonprofit under NDA — I can
> describe the work in general terms. The platform assists practitioners in early detection of a
> neurodevelopmental condition that's chronically underdiagnosed due to practitioner shortage and
> testing cost barriers. The AI processes intake assessments and observation data, surfaces clinical
> indicators to practitioners, and helps them prioritize which patients need further evaluation.
> Every governance requirement in this role description — clinical decision support vs. diagnosis
> distinction, bias detection for underserved populations, explainability, human-in-the-loop design,
> PHI governance — I'm solving those exact problems right now in active development.
> That's the direct clinical AI architecture experience I'd bring to Concentra from day one."*

---

## Healthcare Deployment 2
### Therapeutic Wellness AI Platform
**Status:** Active personal development &nbsp;|&nbsp; **Built by:** Bryan Shaw

#### What It Is
A personal-build AI platform supporting therapeutic wellness and guided mental health journaling.
RAG-powered knowledge retrieval over therapeutic frameworks, with:
- Full HIPAA governance architecture
- PHI classification and zero-token enforcement
- Governed prompting to prevent harmful or contraindicated outputs
- Human-referral escalation paths built in (the system refers to licensed practitioners when
  content exceeds its appropriate scope)
- Audit trail for every interaction

#### Why It Matters for Concentra
This demonstrates that Bryan's HIPAA governance work isn't just platform architecture applied to
client engagements — he builds it himself, from scratch, when designing a personal project.
Governance-first isn't a consulting framework he deploys for clients. It is how he builds.

The specific design decisions relevant to Concentra:
- **Scope enforcement:** the platform knows what it should not do clinically and routes accordingly
  — same design philosophy required for occupational health AI
- **Sensitive data handling:** mental health data requires the highest PHI sensitivity classification;
  the governance patterns developed here transfer directly to clinical settings
- **Patient safety as a design constraint:** when a user session indicates clinical risk, the system
  escalates to human intervention — hard gate, not a soft recommendation

#### Status Note for Interview
*This is a personal development project, not a client deployment. It is not yet publicly hosted.
Describe it as "a personal governance research project building a HIPAA-compliant therapeutic AI
platform" — it demonstrates the depth of personal commitment to getting clinical AI right, not just
delivering it for clients.*

---

## Published HIPAA Credential
### "HIPAA Compliance and AI Data Governance in 2026"
**Published at:** inflexis.ai &nbsp;|&nbsp; **Author:** Bryan Shaw

#### What the Article Covers
Practitioner-level guidance on building AI systems that handle protected health information under
current regulatory requirements. Key topics:

- **PHI classification in AI pipelines** — how to identify, classify, and govern protected health
  information before it reaches model inference
- **Deterministic enforcement patterns** — why relying on LLM-based guardrails for HIPAA compliance
  is insufficient; deterministic, code-enforced controls are required
- **BAA requirements for AI vendors** — what a proper Business Associate Agreement covers in the
  context of AI systems, and what gaps to watch for in vendor contracts
- **Minimum necessary standard applied to AI** — how to implement data minimization in RAG pipelines
  and LLM context windows
- **Audit logging requirements** — what a HIPAA-compliant audit trail looks like for AI systems,
  including model input/output logging and access records
- **De-identification for model training** — safe harbors, expert determination, and the risks of
  using partially de-identified data for AI model training
- **Emerging enforcement landscape** — how HHS OCR is approaching AI-related HIPAA enforcement
  in 2025–2026

#### How to Reference in Interview

> *"I've published practitioner-level guidance on HIPAA compliance and AI data governance —
> not a high-level overview, but a working guide on how to actually build AI systems over PHI
> correctly. The article covers deterministic enforcement patterns, BAA requirements for AI vendors,
> minimum necessary standard in RAG pipelines, and audit logging requirements. It's available at
> inflexis.ai. For a VP AI role at a healthcare company, I wanted to make sure my HIPAA knowledge
> was tested publicly, not just claimed on a resume."*

---

## Gap Score — Revised

Revised from TECH_ALIGNMENT.md after accounting for the full healthcare credential picture:

| Gap Area | Original Score | Revised Score | What Closed It |
|----------|---------------|---------------|----------------|
| Healthcare organization experience | 8/10 | **9.5/10** | Active NDA clinical AI deployment + personal therapeutic platform |
| Clinical workflow familiarity | 6/10 | **9/10** | Clinical decision support workflow design in active development |
| FDA AI/ML guidance | 7/10 | **8.5/10** | SaMD posture analysis completed for dyslexia platform |
| HIPAA production depth | Already 9/10 | **10/10** | Published article + two healthcare deployments + production platform |
| Patient safety understanding | Already 10/10 | **10/10** | Bias/false-negative analysis is core design constraint in clinical deployment |

**Revised overall alignment: 94/100**

The remaining 6 points reflect the honest gap of never having worked *inside* a healthcare
organization — the difference between being the external AI architect and being the internal VP.
That gap is real and worth acknowledging in interviews. The answer is:
> *"I've built the clinical AI governance infrastructure from the outside in. The VP role at
> Concentra lets me apply it from the inside out — where the clinical mission is constant,
> not a client deliverable."*

---

## The Unified Healthcare Narrative

When asked directly about healthcare AI experience, Bryan's answer now has three concrete pillars:

**Pillar 1 — Active Clinical AI Deployment (NDA)**
Building clinical decision support AI for a healthcare nonprofit right now. Every governance
challenge Concentra faces — bias in clinical populations, explainability for practitioners,
human-in-the-loop for diagnostic decisions, PHI governance — is being solved in active development.

**Pillar 2 — Personal Healthcare AI Build**
Built a HIPAA-governed therapeutic wellness platform personally, demonstrating that governance-first
is a design philosophy, not a consulting deliverable.

**Pillar 3 — Published HIPAA Expertise**
Published practitioner-level HIPAA AI compliance guidance. Healthcare regulatory knowledge is
publicly tested, not just claimed.

**The honest frame that ties it together:**
> *"I haven't been an employee inside a healthcare organization. What I have is something
> complementary: I've spent the last two years solving the hardest governance problems in clinical
> AI — bias detection, PHI enforcement, explainability, human-in-the-loop — while building
> production systems and publishing what I've learned. I bring the governance architecture Concentra
> needs on day one, and I bring fresh eyes on the clinical operations side — which means I'll ask
> the questions your internal team has stopped asking because the answers feel obvious."*

---

## NDA Handling Guidance

**What you can say:**
- Healthcare nonprofit organization
- Working with neuroscientists
- Clinical decision support for neurodevelopmental early detection
- The governance architecture, design decisions, and challenges
- The population served (underdiagnosed, access-constrained)
- Active development status

**What you cannot say:**
- Organization name
- Any individual names (including the philanthropist)
- The specific condition name if it would identify the organization
- Any financials or deal terms

**Safe language for the condition:**
*"a neurodevelopmental condition that affects reading and language processing, is significantly
underdiagnosed in the general population, and for which early detection has substantial impact
on educational outcomes"* — this describes dyslexia accurately without naming it if naming it
would narrow identification of the client.

> **Judgment call:** In most interview settings, naming dyslexia as a condition does not identify
> the client organization. The risk is in naming the nonprofit, the philanthropist, or any other
> identifying detail. Use your judgment on whether to name the condition based on the specificity
> of the conversation.

---

*Private · Bryan Shaw · May 2026 · BryanJShaw@gmail.com · 817-653-5656*
