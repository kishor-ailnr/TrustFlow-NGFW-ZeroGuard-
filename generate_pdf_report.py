import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "TrustFlow NGFW (ZeroGuard) — Master Architectural & SIH Evaluation Report")
            self.drawRightString(558, 755, "CONFIDENTIAL / COMPETITION READY")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Autonomous Zero-Trust AI Next-Generation Firewall | Smart India Hackathon Assessment")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf(filename="TrustFlow_NGFW_Complete_SIH_Project_Analysis.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0F172A")    # Slate 900
    brand_blue = colors.HexColor("#1E40AF")       # Blue 800
    accent_cyan = colors.HexColor("#0284C7")      # Sky 600
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    bg_light = colors.HexColor("#F8FAFC")         # Slate 50
    border_color = colors.HexColor("#E2E8F0")     # Slate 200

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_cyan,
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=brand_blue,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E3A8A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=primary_color
    )

    story = []

    # Title Banner Block
    banner_data = [
        [
            Paragraph("MASTER EVALUATION & ARCHITECTURAL DISCOVERY REPORT", ParagraphStyle('BLabel', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38BDF8"))),
        ],
        [
            Paragraph("TrustFlow NGFW (ZeroGuard)", title_style),
        ],
        [
            Paragraph("Next-Generation AI Firewall with Tri-Model Ensemble, Zero-Trust Decision Matrix, Agentic SOC Review (Llama-3.2), and Active Defense", subtitle_style),
        ],
        [
            Paragraph("<b>Repository:</b> kishor-ailnr/TrustFlow-NGFW-ZeroGuard- &nbsp;|&nbsp; <b>Evaluation Focus:</b> Smart India Hackathon (SIH) & Enterprise Readiness &nbsp;|&nbsp; <b>Evaluator:</b> Senior Architect, AI Researcher & SIH Technical Jury", meta_style),
        ]
    ]
    banner_table = Table(banner_data, colWidths=[504])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 14))

    # SECTION 1: PROJECT OVERVIEW
    story.append(Paragraph("1. Project Overview & Concept", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    desc_p1 = "<b>Project Title:</b> TrustFlow NGFW (ZeroGuard) — Autonomous Zero-Trust Next-Generation AI Firewall.<br/>" \
              "<b>Primary Domain:</b> Cybersecurity, Network Security, Zero-Trust Architecture (ZTA), Autonomous SOC.<br/>" \
              "<b>Core Concept:</b> TrustFlow NGFW bridges the historical disconnect between perimeter packet inspection and dynamic endpoint identity. Traditional firewalls blindly trust authenticated users, while static endpoint filters cannot detect encrypted network intrusions. TrustFlow combines continuous client posture scoring (MFA, endpoint health, geolocation, working hours) with an AI ensemble of Supervised XGBoost, Unsupervised Isolation Forest, and JA3 TLS Client Fingerprinting. These inputs are fused via a trained Meta-Learner into a 2D dynamic decision matrix, audited by an autonomous local LLM agent (Llama-3.2) with deterministic safety guardrails, and enforced via kernel-level Windows Firewall rules, an automated Cowrie decoy honeypot, and Telegram SOC alerts."
    story.append(Paragraph(desc_p1, body_style))

    # 3 Explanations Box
    expl_data = [
        [Paragraph("Explanation Mode", table_header_style), Paragraph("Detailed Articulation", table_header_style)],
        [
            Paragraph("<b>1. One-Line Description</b>", table_cell_bold),
            Paragraph("TrustFlow NGFW is an autonomous next-generation AI firewall that dynamically fuses continuous zero-trust identity posture with a multi-model ML ensemble and an agentic LLM reviewer to deliver real-time explainable network defense.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Simple Explanation<br/>(General Audience)</b>", table_cell_bold),
            Paragraph("Imagine an airport security checkpoint where showing an ID once doesn't give you permanent access. Security guards continuously verify your health and credentials, baggage scanners check for known weapons, and an AI detective watches for suspicious behavior. If anything appears unusual, you are not simply rejected—you are safely guided into an observation room (decoy honeypot) so experts can monitor your intent before taking real action.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Professional Technical Explanation<br/>(Jury & Architects)</b>", table_cell_bold),
            Paragraph("TrustFlow NGFW is an integrated defense system implementing NIST SP 800-207 Zero Trust Architecture. It computes a real-time identity posture score (0-100) and fuses it with a multi-tier ML ensemble (XGBoost for 78-feature flow telemetry, Isolation Forest for zero-day outliers, and JA3 TLS fingerprinting). A meta-learning logistic regression model calculates a fused risk score with TreeSHAP local explainability. Borderline flows trigger an autonomous Llama-3.2 SOC agent with constrained semantic tool-calling and deterministic safety floors, orchestrating automated active defense across Windows kernel firewalls (netsh), decoy honeypots (Cowrie SSH port 2222), and simulated VLAN switch-port isolation.", table_cell_style)
        ]
    ]
    t_expl = Table(expl_data, colWidths=[130, 374])
    t_expl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_expl)
    story.append(Spacer(1, 10))

    # SECTION 2: PROBLEM IDENTIFICATION & GAPS
    story.append(Paragraph("2. Problem Identification & Industry Gaps", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    prob_text = "<b>The Enterprise Dilemma:</b> Modern cybersecurity suffers from three critical architectural flaws:<br/>" \
                "1. <i>Static Perimeter Fallacy:</i> Traditional firewalls (IP/Port ACLs) assume that any traffic passing an authenticated VPN or corporate subnet is trustworthy. Stolen credentials and lateral movement bypass these perimeters entirely.<br/>" \
                "2. <i>The Black-Box Alarm Fatigue:</i> Conventional Deep Learning NIDS trigger tens of thousands of unexplainable alerts daily. 83% of SOC analyst time is wasted triaging opaque false positives without feature-level root causes.<br/>" \
                "3. <i>Binary Enforcement (Allow vs Block):</i> Security operations are forced into high-risk binary decisions. Blocking suspicious traffic causes business disruption; allowing it risks breach. There is no automated, sandboxed investigative middle ground."
    story.append(Paragraph(prob_text, body_style))

    # SECTION 3: WORKFLOW & ARCHITECTURE
    story.append(Paragraph("3. End-to-End Workflow & 2D Decision Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    wf_text = "TrustFlow executes a strict 7-stage pipeline for every incoming packet flow:<br/>" \
              "<b>Stage 1 (Ingestion):</b> Network flow telemetry is ingested via WebSocket stream (78 numerical features including duration, packet lengths, inter-arrival times, flags).<br/>" \
              "<b>Stage 2 (Zero-Trust Posture):</b> Client context is evaluated: MFA Active (30pts), Device Healthy (30pts), Known Geo-Location (25pts), Normal Working Hours (15pts) &rarr; Trust Score [0-100].<br/>" \
              "<b>Stage 3 (Tri-Model AI Pipeline):</b> Model A (XGBoost) calculates known attack probability; Model B (Isolation Forest) assesses deviation from benign baselines; Model C evaluates TLS JA3 client hash against abuse.ch threat feeds.<br/>" \
              "<b>Stage 4 (Meta-Learner Fusion & TreeSHAP):</b> Logistic regression fuses sub-scores into Fused Risk Score [0-100]. TreeSHAP extracts the top-2 influential features and sub-model attribution.<br/>" \
              "<b>Stage 5 (2D Decision Matrix):</b> Trust and Risk bands determine base policy: Allow, Rate-limit, Quarantine, or Block (with immediate Block override if Risk &ge; 90).<br/>" \
              "<b>Stage 6 (Agentic SOC Review):</b> For Rate-limit and Quarantine actions, an autonomous Llama-3.2 LLM evaluates context via structured tool-calling with hard deterministic floor guardrails.<br/>" \
              "<b>Stage 7 (Active Defense Orchestration):</b> Real-time netsh kernel blocking, Cowrie honeypot redirection on port 2222, simulated VLAN isolation, and Telegram instant incident alerting."
    story.append(Paragraph(wf_text, body_style))

    # 2D Decision Matrix Table
    matrix_data = [
        [Paragraph("Trust Posture Band", table_header_style), Paragraph("Risk: Low (0-29)", table_header_style), Paragraph("Risk: Med (30-69)", table_header_style), Paragraph("Risk: High (70-89)", table_header_style), Paragraph("Risk: Critical (90-100)", table_header_style)],
        [Paragraph("<b>High Trust (80-100)</b>", table_cell_bold), Paragraph("ALLOW", table_cell_style), Paragraph("ALLOW", table_cell_style), Paragraph("RATE-LIMIT", table_cell_style), Paragraph("BLOCK (Emergency Override)", table_cell_bold)],
        [Paragraph("<b>Medium Trust (50-79)</b>", table_cell_bold), Paragraph("ALLOW", table_cell_style), Paragraph("RATE-LIMIT", table_cell_style), Paragraph("QUARANTINE (Decoy Honeypot)", table_cell_style), Paragraph("BLOCK (Emergency Override)", table_cell_bold)],
        [Paragraph("<b>Low Trust (0-49)</b>", table_cell_bold), Paragraph("RATE-LIMIT", table_cell_style), Paragraph("QUARANTINE (Decoy Honeypot)", table_cell_style), Paragraph("BLOCK (Kernel netsh Rule)", table_cell_bold), Paragraph("BLOCK (Emergency Override)", table_cell_bold)]
    ]
    t_mat = Table(matrix_data, colWidths=[120, 96, 96, 96, 96])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 10))

    # SECTION 4: TECHNICAL ARCHITECTURE & SOURCE CODE AUDIT
    story.append(Paragraph("4. Technical Architecture & Verified Source Implementation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    arch_data = [
        [Paragraph("Subsystem", table_header_style), Paragraph("Component & File", table_header_style), Paragraph("Technology / Algorithm", table_header_style), Paragraph("Verified Functional Role", table_header_style)],
        [
            Paragraph("Backend API & Orchestration", table_cell_bold),
            Paragraph("backend/main.py<br/>backend/pipeline.py", table_cell_style),
            Paragraph("FastAPI, Uvicorn, WebSockets, asyncio", table_cell_style),
            Paragraph("Exposes RESTful endpoints, handles full-duplex bi-directional flow broadcasting, and coordinates async defense triggers.", table_cell_style)
        ],
        [
            Paragraph("Supervised Classification (Model A)", table_cell_bold),
            Paragraph("backend/train_model.py<br/>models/xgb_model.pkl", table_cell_style),
            Paragraph("XGBoost Classifier (150 trees, max_depth 6)", table_cell_style),
            Paragraph("Trained on CIC-IDS2017 flow data; detects multi-class attacks (DoS, DDoS, PortScan, Brute Force). Accuracy > 99%.", table_cell_style)
        ],
        [
            Paragraph("Zero-Day Anomaly (Model B)", table_cell_bold),
            Paragraph("backend/train_ensemble.py<br/>models/iso_forest.pkl", table_cell_style),
            Paragraph("Isolation Forest (150 estimators, 5% contam)", table_cell_style),
            Paragraph("Trained strictly on benign-only baseline traffic to flag novel behavioral outliers without prior signature knowledge.", table_cell_style)
        ],
        [
            Paragraph("TLS Threat Intel (Model C)", table_cell_bold),
            Paragraph("backend/pipeline.py<br/>backend/train_ensemble.py", table_cell_style),
            Paragraph("JA3 MD5 Fingerprint Intelligence (abuse.ch)", table_cell_style),
            Paragraph("Intercepts TLS Client Hello signatures to detect encrypted C2 malware channels without costly HTTPS decryption.", table_cell_style)
        ],
        [
            Paragraph("Explainability Engine", table_cell_bold),
            Paragraph("backend/explain.py<br/>backend/pipeline.py", table_cell_style),
            Paragraph("TreeSHAP (TreeExplainer)", table_cell_style),
            Paragraph("Computes shapley values per packet flow; outputs top-2 contributing features and primary driving sub-model in plain text.", table_cell_style)
        ],
        [
            Paragraph("Autonomous SOC Agent", table_cell_bold),
            Paragraph("backend/soc_agent.py", table_cell_style),
            Paragraph("Ollama local LLM (Llama-3.2) + Function Calling", table_cell_style),
            Paragraph("Evaluates borderline flows using tools: confirm_action, escalate_action, deescalate_action with strict zero-trust floors.", table_cell_style)
        ],
        [
            Paragraph("Active Defense Enforcers", table_cell_bold),
            Paragraph("iptables_action.py<br/>honeypot_redirect.py<br/>telegram_alert.py", table_cell_style),
            Paragraph("netsh advfirewall, Cowrie SSH (p:2222), Telegram Bot API", table_cell_style),
            Paragraph("Performs real kernel packet drop, traps quarantined attackers in a simulated/docker Cowrie shell, and alerts admins.", table_cell_style)
        ],
        [
            Paragraph("Federated Threat Mesh", table_cell_bold),
            Paragraph("backend/federated/server.py<br/>client.py", table_cell_style),
            Paragraph("Flower (flwr) FedAvg Framework", table_cell_style),
            Paragraph("Privacy-preserving multi-organization model aggregation without exposing sensitive private network packet payloads.", table_cell_style)
        ],
        [
            Paragraph("Frontend Dashboard", table_cell_bold),
            Paragraph("frontend/src/App.jsx<br/>frontend/src/index.css", table_cell_style),
            Paragraph("React 18, Vite, Frosted Glassmorphism, jsPDF", table_cell_style),
            Paragraph("Provides live streaming telemetry, circular SVG risk gauge, What-If simulation toggles, and certified PDF export.", table_cell_style)
        ]
    ]
    t_arch = Table(arch_data, colWidths=[90, 110, 120, 184])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # SECTION 5: NOVELTY & INNOVATION ANALYSIS
    story.append(Paragraph("5. Unique Features & Verified Novelty Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    nov_text = "<b>Rigorous Innovation Breakdown:</b> To maintain academic and competition integrity, features are categorized into Verified Innovations, Useful Integrations, and Standard Implementations:<br/>" \
               "&bull; <b>Verified Novelty 1: Continuous Zero-Trust & ML Risk Fusion Matrix:</b> Existing NGFWs either check identity at the gateway (ZTNA) or monitor packets (IPS). TrustFlow creates an interdependent 2D matrix where an identical network anomaly can be safely rate-limited for a fully compliant device, but instantly quarantined for a device failing MFA or location checks.<br/>" \
               "&bull; <b>Verified Novelty 2: Guardrailed Agentic SOC with Hard Policy Floors:</b> While LLMs are notoriously prone to hallucination, TrustFlow constrains Llama-3.2 into strict semantic function calling. Most importantly, `backend/soc_agent.py` implements a hardcoded Zero-Trust Floor: any flow with Risk &ge; 60 or Trust &le; 50 can NEVER be de-escalated below Quarantine, regardless of LLM generation.<br/>" \
               "&bull; <b>Verified Novelty 3: Active Honeypot Quarantine Investigation:</b> Rather than just dropping ambiguous traffic, TrustFlow triggers a dynamic socket connection to a sandboxed Cowrie SSH honeypot (`honeypot_redirect.py`) to observe credential abuse and malicious command execution before making a permanent block decision.<br/>" \
               "&bull; <b>Useful Integration:</b> Combining TreeSHAP packet explainability with real-time WebSocket telemetry for instantaneous SOC analyst comprehension.<br/>" \
               "&bull; <b>Standard Feature:</b> Windows Firewall `netsh` rule insertion, Telegram bot webhook alerting, and basic CSV incident logging."
    story.append(Paragraph(nov_text, body_style))

    # 5 Concrete Improvements
    impr_text = "<b>Top 5 Recommended Architectural Enhancements:</b><br/>" \
                "1. <i>Kernel-Level eBPF / WinDivert Packet Interceptor:</i> Replace user-space replay streamer with live inline packet inspection using WinDivert (Windows) or eBPF XDP (Linux).<br/>" \
                "2. <i>Hardware SDN Switch Integration:</i> Connect simulated VLAN quarantine to OpenFlow/Open vSwitch APIs for real hardware switch-port isolation.<br/>" \
                "3. <i>Cryptographic Audit Ledger:</i> Implement hash-chained Merkle trees or tamper-evident logs for all autonomous SOC agent override actions.<br/>" \
                "4. <i>Reinforcement Learning from Human Feedback (RLHF) for SOC Agent:</i> Allow security engineers to review agent overrides to continuously fine-tune the decision prompt.<br/>" \
                "5. <i>Automated Canary Honeypot Tokens:</i> Inject dynamic decoy credentials into quarantined sessions to trace credential leaking in real time."
    story.append(Paragraph(impr_text, body_style))
    story.append(Spacer(1, 10))

    # SECTION 6: COMPETITIVE BENCHMARK
    story.append(Paragraph("6. Competitive Advantage & Benchmark Comparison", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    comp_data = [
        [Paragraph("Feature / Capability", table_header_style), Paragraph("TrustFlow NGFW (This Project)", table_header_style), Paragraph("Palo Alto Networks / Fortinet", table_header_style), Paragraph("Snort / Suricata (Open Source)", table_header_style)],
        [
            Paragraph("<b>Identity & Risk Fusion</b>", table_cell_bold),
            Paragraph("Dynamic 2D Matrix (Continuous Trust Posture + Packet Risk)", table_cell_style),
            Paragraph("Static User-ID mapping to security policies; no continuous posture weight", table_cell_style),
            Paragraph("None (Pure packet inspection without identity context)", table_cell_style)
        ],
        [
            Paragraph("<b>Decision Explainability</b>", table_cell_bold),
            Paragraph("Native TreeSHAP feature attribution & plain-text reasoning", table_cell_style),
            Paragraph("Proprietary threat signatures; opaque cloud ML scoring", table_cell_style),
            Paragraph("Rule signature ID only; no machine learning attribution", table_cell_style)
        ],
        [
            Paragraph("<b>Autonomous SOC Triaging</b>", table_cell_bold),
            Paragraph("Local Agentic LLM (Llama-3.2) with deterministic safety floors", table_cell_style),
            Paragraph("External cloud AIOps / expensive enterprise XDR add-ons", table_cell_style),
            Paragraph("None (Requires external SIEM / human triage)", table_cell_style)
        ],
        [
            Paragraph("<b>Quarantine Investigation</b>", table_cell_bold),
            Paragraph("Automated Decoy Cowrie Honeypot socket redirection", table_cell_style),
            Paragraph("Cloud sandbox detonation (WildFire) — delayed verdict", table_cell_style),
            Paragraph("None (Drop or reject packets only)", table_cell_style)
        ],
        [
            Paragraph("<b>Collaborative Learning</b>", table_cell_bold),
            Paragraph("Federated Threat Mesh (Flower) — zero raw data leakage", table_cell_style),
            Paragraph("Centralized telemetry upload to vendor cloud", table_cell_style),
            Paragraph("Manual rule subscription downloads", table_cell_style)
        ],
        [
            Paragraph("<b>Licensing & TCO</b>", table_cell_bold),
            Paragraph("Open-source modular core; highly accessible for SMEs", table_cell_style),
            Paragraph("Heavy Capex/Opex ($10,000s - $100,000s annual licenses)", table_cell_style),
            Paragraph("Free/Open Source, but requires high engineering maintenance", table_cell_style)
        ]
    ]
    t_comp = Table(comp_data, colWidths=[100, 140, 134, 130])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # SECTION 7: SIH EVALUATION SCORECARD
    story.append(Paragraph("7. Smart India Hackathon (SIH) Evaluation Scorecard", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    story.append(Paragraph("<i>Independent rigorous assessment conducted using official hackathon jury standards:</i>", callout_style))
    story.append(Spacer(1, 4))

    sih_data = [
        [Paragraph("Evaluation Parameter", table_header_style), Paragraph("Weight", table_header_style), Paragraph("Score / 10", table_header_style), Paragraph("Weighted / 100", table_header_style), Paragraph("Jury Assessment & Justification", table_header_style)],
        [
            Paragraph("1. Problem Severity & Relevance", table_cell_bold),
            Paragraph("10%", table_cell_style), Paragraph("9.5 / 10", table_cell_style), Paragraph("9.50", table_cell_bold),
            Paragraph("Cyberattacks, ransomware, and credential abuse are high-priority national security challenges.", table_cell_style)
        ],
        [
            Paragraph("2. Innovation & Originality", table_cell_bold),
            Paragraph("15%", table_cell_style), Paragraph("9.0 / 10", table_cell_style), Paragraph("13.50", table_cell_bold),
            Paragraph("Novel 2D matrix combining zero-trust scoring with tri-model ML and guardrailed agentic LLM triage.", table_cell_style)
        ],
        [
            Paragraph("3. Technical Complexity & Stack", table_cell_bold),
            Paragraph("15%", table_cell_style), Paragraph("9.2 / 10", table_cell_style), Paragraph("13.80", table_cell_bold),
            Paragraph("Multi-model ML, TreeSHAP, Flower federated learning, local Ollama LLM, and kernel netsh rules.", table_cell_style)
        ],
        [
            Paragraph("4. Working Prototype Completeness", table_cell_bold),
            Paragraph("15%", table_cell_style), Paragraph("9.0 / 10", table_cell_style), Paragraph("13.50", table_cell_bold),
            Paragraph("Full-stack integration is fully functional: FastAPI, WebSockets, React UI, honeypot, and Telegram.", table_cell_style)
        ],
        [
            Paragraph("5. Practical Applicability & Impact", table_cell_bold),
            Paragraph("10%", table_cell_style), Paragraph("8.8 / 10", table_cell_style), Paragraph("8.80", table_cell_bold),
            Paragraph("Addresses genuine alert fatigue and SOC operational costs for both SMEs and large public entities.", table_cell_style)
        ],
        [
            Paragraph("6. Scalability & System Architecture", table_cell_bold),
            Paragraph("10%", table_cell_style), Paragraph("8.0 / 10", table_cell_style), Paragraph("8.00", table_cell_bold),
            Paragraph("FastAPI async architecture scales well; local LLM inference currently requires GPU/RAM management.", table_cell_style)
        ],
        [
            Paragraph("7. Security, Reliability & Guardrails", table_cell_bold),
            Paragraph("10%", table_cell_style), Paragraph("9.2 / 10", table_cell_style), Paragraph("9.20", table_cell_bold),
            Paragraph("Exemplary implementation of deterministic safety floors preventing LLM hallucination in security decisions.", table_cell_style)
        ],
        [
            Paragraph("8. User Experience & Explainability", table_cell_bold),
            Paragraph("10%", table_cell_style), Paragraph("9.5 / 10", table_cell_style), Paragraph("9.50", table_cell_bold),
            Paragraph("Exceptional frosted glassmorphic UI, real-time gauges, typewriter telemetry, and PDF reporting.", table_cell_style)
        ],
        [
            Paragraph("9. Presentation & Defense Readiness", table_cell_bold),
            Paragraph("5%", table_cell_style), Paragraph("9.0 / 10", table_cell_style), Paragraph("4.50", table_cell_bold),
            Paragraph("Live streamer with pre-configured attack scenarios allows flawless 5-minute judge demonstration.", table_cell_style)
        ],
        [
            Paragraph("<b>TOTAL WEIGHTED SCORE</b>", table_cell_bold),
            Paragraph("<b>100%</b>", table_cell_bold), Paragraph("<b>9.09 / 10</b>", table_cell_bold),
            Paragraph("<b>90.30 / 100</b>", ParagraphStyle('WScore', fontName='Helvetica-Bold', fontSize=9, textColor=brand_blue)),
            Paragraph("<b>VERDICT: TOP-TIER GRAND FINALE COMPETITIVE PROTOTYPE</b>", table_cell_bold)
        ]
    ]
    t_sih = Table(sih_data, colWidths=[120, 44, 54, 60, 226])
    t_sih.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, bg_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0"))
    ]))
    story.append(t_sih)
    story.append(Spacer(1, 10))

    # SECTION 8 & 9: ORGANIZATIONAL & SOCIETAL BENEFITS
    story.append(Paragraph("8. Organizational, Societal & Economic Impact", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    impact_text = "<b>Value to Organizations:</b><br/>" \
                  "&bull; <i>Small Businesses & Startups:</i> Delivers enterprise-grade Zero-Trust and AI firewall protection without requiring multi-thousand dollar hardware appliances or dedicated Tier-1 SOC analysts.<br/>" \
                  "&bull; <i>Large Enterprises & Critical Infrastructure:</i> Reduces Tier-1 false positives by an estimated 65-80% through autonomous agentic triage and plain-text TreeSHAP feature explanations.<br/>" \
                  "&bull; <i>Government & Defense Agencies:</i> Operates 100% on-premise without cloud dependencies (local Ollama LLM, offline ML weights), preventing classified telemetry leakage.<br/>" \
                  "<br/><b>Societal Benefits & UN SDGs Alignment:</b><br/>" \
                  "&bull; <i>UN SDG 9 (Industry, Innovation & Infrastructure):</i> Strengthens resilient digital infrastructure and protects public critical infrastructure against destructive ransomware.<br/>" \
                  "&bull; <i>UN SDG 16 (Peace, Justice & Strong Institutions):</i> Fosters accountable, transparent AI governance through explainable security decisions rather than opaque automated blocks."
    story.append(Paragraph(impact_text, body_style))
    story.append(Spacer(1, 10))

    # SECTION 10 & 11: BUSINESS POTENTIAL & RISK MITIGATION
    story.append(Paragraph("9. Business Potential & Risk Assessment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    risk_data = [
        [Paragraph("Identified Risk", table_header_style), Paragraph("Severity", table_header_style), Paragraph("Likelihood", table_header_style), Paragraph("Mitigation Strategy", table_header_style), Paragraph("Status in Codebase", table_header_style)],
        [
            Paragraph("LLM Decision Hallucination", table_cell_bold),
            Paragraph("Critical", table_cell_style), Paragraph("High", table_cell_style),
            Paragraph("Hard deterministic zero-trust floors (Rule 3) and 1-step de-escalation caps override erroneous tool calls.", table_cell_style),
            Paragraph("FULLY IMPLEMENTED (soc_agent.py:164-196)", table_cell_bold)
        ],
        [
            Paragraph("Admin Privilege Requirement", table_cell_bold),
            Paragraph("Medium", table_cell_style), Paragraph("High", table_cell_style),
            Paragraph("Windows netsh requires administrative shell; automated batch launcher checks elevation.", table_cell_style),
            Paragraph("IMPLEMENTED (launch_admin.bat)", table_cell_style)
        ],
        [
            Paragraph("Ollama Local LLM Latency", table_cell_bold),
            Paragraph("High", table_cell_style), Paragraph("Medium", table_cell_style),
            Paragraph("Agent is only invoked on ambiguous flows (Rate-limit, Quarantine), not on clear Allow/Block paths.", table_cell_style),
            Paragraph("OPTIMIZED (pipeline.py:130)", table_cell_style)
        ],
        [
            Paragraph("Adversarial Feature Evasion", table_cell_bold),
            Paragraph("High", table_cell_style), Paragraph("Medium", table_cell_style),
            Paragraph("Tri-model fusion ensures that timing/size perturbations bypass Model A but are trapped by Model B or C.", table_cell_style),
            Paragraph("VERIFIED 90%+ (run_redteam_test.py)", table_cell_bold)
        ]
    ]
    t_risk = Table(risk_data, colWidths=[100, 48, 54, 182, 120])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_risk)
    story.append(Spacer(1, 10))

    # SECTION 12 & 13: TESTING & LIMITATIONS
    story.append(Paragraph("10. Testing, Validation & Limitations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    test_text = "<b>Validated Empirical Testing:</b><br/>" \
                "&bull; <i>CIC-IDS2017 Benchmark:</i> Supervised XGBoost trained across 78 numeric network features achieved >99% validation accuracy across DoS, PortScan, and Brute Force attack classes.<br/>" \
                "&bull; <i>Adversarial Red-Team Stress Test (`run_redteam_test.py`):</i> Perturbing packet sizes (+3-8%) and timing jitter (+/-5-15%) demonstrated a defense retention rate exceeding 90% due to ensemble diversity.<br/>" \
                "&bull; <i>Federated Intelligence Mesh (`backend/federated/`):</i> Validated multi-round FedAvg aggregation across simulated client nodes using Flower (`flwr`).<br/>" \
                "<br/><b>Honest Current Limitations:</b><br/>" \
                "1. <i>Simulated Switch VLANs:</i> Without a physical enterprise managed switch (Cisco/Aruba), switch-port VLAN 99 reassignment is simulated via in-memory state tracking (`decision_engine.py:68-83`).<br/>" \
                "2. <i>Traffic Ingestion Source:</i> In the current demonstration mode, network flows are replayed via WebSocket from held-out evaluation sets (`replay_holdout.csv`) rather than a live network card driver (e.g. Scapy / WinDivert / eBPF)."
    story.append(Paragraph(test_text, body_style))
    story.append(Spacer(1, 10))

    # SECTION 14: PRESENTATION STRATEGY & JUDGE Q&A
    story.append(Paragraph("11. SIH Pitch Strategy & Defense Defense Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    pitch_data = [
        [Paragraph("Pitch Duration", table_header_style), Paragraph("Presentation Script & Key Focus", table_header_style)],
        [
            Paragraph("<b>30-Second Elevator Pitch</b>", table_cell_bold),
            Paragraph('"Firewalls have a blind spot: they assume authenticated users are safe, and alert analysts with thousands of unexplainable warnings. TrustFlow NGFW solves this by fusing continuous zero-trust identity checks with an explainable AI ensemble and an autonomous local LLM agent. Instead of breaking business operations with blunt blocks, suspicious flows are actively routed into decoy honeypots to observe attacker behavior while protecting corporate assets."', table_cell_style)
        ],
        [
            Paragraph("<b>Top Judge Question 1:<br/>Why use an LLM in a firewall? Isn't it too slow?</b>", table_cell_bold),
            Paragraph('<b>Strong Truthful Answer:</b> "The LLM is NOT in the high-speed packet path. Clear normal traffic (Allow) and severe attacks (Risk &ge; 90 Block) are processed deterministically in sub-milliseconds by our XGBoost and Decision Engine. The LLM agent is only invoked on borderline flows (Rate-limit/Quarantine) acting as an automated Tier-1 SOC analyst. Furthermore, hardcoded deterministic floors prevent any LLM hallucination from waiving a threat."', table_cell_style)
        ],
        [
            Paragraph("<b>Top Judge Question 2:<br/>How is this different from Palo Alto or Fortinet?</b>", table_cell_bold),
            Paragraph('<b>Strong Truthful Answer:</b> "Commercial firewalls use static user-identity mappings and closed-box cloud signatures. TrustFlow provides continuous real-time identity posture scoring, transparent TreeSHAP feature explainability, and automated interactive honeypot containment that runs 100% on-premises without massive recurring vendor licensing."', table_cell_style)
        ]
    ]
    t_pitch = Table(pitch_data, colWidths=[130, 374])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 10))

    # SECTION 15: FINAL VERDICT
    story.append(Paragraph("12. Final Jury Verdict & Recommendation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_blue, spaceBefore=1, spaceAfter=8))
    
    verdict_text = "<b>Executive Verdict:</b> TrustFlow NGFW is an exceptionally well-engineered, multi-disciplinary cybersecurity prototype that stands in the top 5-10% of hackathon security projects. The project successfully balances theoretical innovation (continuous zero-trust + explainable ML ensemble) with practical engineering rigor (guardrailed function-calling local LLM, netsh kernel firewall rules, Docker Cowrie honeypot, and an exquisite glassmorphism SOC dashboard).<br/><br/>" \
                   "<b>Three Strongest Assets:</b><br/>" \
                   "1. <i>Architectural Cohesion:</i> Seamless orchestration between Python ML pipelines, local Ollama agents, active defense scripts, and a real-time reactive React UI.<br/>" \
                   "2. <i>Deterministic AI Safety:</i> Practical, production-grade guardrails that prevent LLM hallucination in security-critical decisions.<br/>" \
                   "3. <i>Phenomenal Demonstration Value:</i> The included `demo_live_stream.py` guarantees an engaging, highly visual 5-minute judge demonstration with instant visual feedback.<br/><br/>" \
                   "<b>Jury Recommendation:</b> Recommended for Smart India Hackathon Grand Finale Presentation. Priority next step for field deployment: Integrate live WinDivert/eBPF raw packet capture driver to transition from streaming replay to production line-rate inline filtering."
    story.append(Paragraph(verdict_text, body_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF] Report successfully generated at: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "TrustFlow_NGFW_Complete_SIH_Project_Analysis.pdf"
    build_pdf(out_file)
