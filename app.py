import streamlit as st
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="ContractLens | Commercial Control Room",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400;1,6..72,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
.stApp { background-color: #F8FAFC; color: #0F172A; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }
.serif-title { font-family: 'Newsreader', Georgia, serif; font-size: 34px; font-weight: 500; letter-spacing: -0.5px; color: #0F172A; margin: 0; line-height: 1.15; }
.serif-title em { font-style: italic; color: #0D9488; }
.serif-sub { font-family: 'Newsreader', Georgia, serif; font-size: 20px; font-weight: 500; color: #0F172A; margin: 0; }
.metric-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); }
.card-insight { background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #16A34A; border-radius: 10px; padding: 12px 16px; margin-top: 14px; }
.evidence-panel { background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 22px; box-shadow: 0 4px 14px rgba(0,0,0,0.05); }
.ingest-step { background: #F0F9FF; border: 1px solid #BAE6FD; border-left: 3px solid #0284C7; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; color: #0369A1; }
.pushback-box { background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 14px 16px; margin-top: 12px; font-size: 12px; color: #78350F; font-family: monospace; white-space: pre-wrap; line-height: 1.6; }
.ledger-row { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; }
.badge-crit { background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
.badge-warn { background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
.badge-ok { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
.badge-pill { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA -----------------
PORTFOLIO = {
    "health": 78,
    "contracts": 12,
    "managed_val": "$1.01M",
    "managed_val_inr": "₹8.40 Cr",
    "exposure": "$51,000",
    "exposure_inr": "₹42.5 Lakhs",
    "next_date": "02 Aug 2027",
    "deadlines": [
        {"date": "22 Sep 2026", "task": "Quality Batch Assay Sign-Off", "contract": "Pacific Rim Formulations", "owner": "Quality Lead", "status": "Upcoming"},
        {"date": "28 Sep 2026", "task": "Submit Bill of Lading Balance Invoice", "contract": "Pacific Rim Formulations", "owner": "Finance", "status": "Scheduled"},
        {"date": "02 Oct 2026", "task": "Annual Non-Renewal Formal Notice Cutoff", "contract": "Pacific Rim Formulations", "owner": "Commercial Ops", "status": "Critical Cutoff"}
    ]
}

AGREEMENT = {
    "title": "Master Manufacturing & Supply Agreement",
    "parties": "Auric Consumer Brands Pvt Ltd (Mumbai, India) ↔ Pacific Rim Formulations Ltd (Hong Kong)",
    "term": "01 Nov 2026 – 31 Oct 2027",
    "value": "$45,000 USD-fixed (~INR 37.5 Lakhs)",
    "renewal_notice": "02 Aug 2027 (90 Days Prior Written Notice Required)",
    "health_score": 78,
    "commitments": [
        {
            "id": "c1",
            "task": "Issue non-renewal notice",
            "party": "Buyer",
            "owner": "Maya Rao (Commercial Ops)",
            "trigger": "90 days before term end",
            "deadline": "02 Aug 2027",
            "status": "At risk",
            "clause": "§5.2",
            "confidence": "99%",
            "verbatim": "Either party may elect not to renew by providing written notice at least ninety (90) days prior to expiry.",
            "impact": "Avoids mandatory 2-year auto-renewal extension (~$90k lock-in).",
            "pushback_email": """Subject: Notice of Non-Renewal — Master Manufacturing & Supply Agreement

Dear Pacific Rim Formulations Ltd,

Pursuant to Section 5.2 of the Master Manufacturing & Supply Agreement dated 01 November 2026,
Auric Consumer Brands Pvt Ltd hereby provides formal written notice of its election not to renew
the Agreement beyond the initial term expiring 31 October 2027.

This notice is delivered in compliance with the ninety (90) day prior written notice requirement
and constitutes our irrevocable intent not to enter an automatic renewal period.

Please confirm receipt at your earliest convenience.

Regards,
Maya Rao
Commercial Operations Lead, Auric Consumer Brands"""
        },
        {
            "id": "c2",
            "task": "Complete incoming lab clearance",
            "party": "Buyer",
            "owner": "Mumbai Quality Team",
            "trigger": "Receipt of batch at port",
            "deadline": "7 calendar days",
            "status": "Action Required",
            "clause": "§3.1",
            "confidence": "96%",
            "verbatim": "Silence shall constitute irrevocable deemed acceptance within seven (7) calendar days of arrival.",
            "impact": "Pre-shipment payment means zero leverage if batch is contaminated.",
            "pushback_email": """Subject: Objection to 7-Day Inspection Cutoff — Section 3.1 Counter-Draft

Dear Pacific Rim Formulations Ltd,

We write to formally object to the proposed 7-calendar-day deemed acceptance window in Section 3.1
of your counter-draft dated [DATE].

Indian customs clearance at Nhava Sheva port routinely requires 4–6 business days to process
import declarations, obtain out-of-charge orders, and release cargo to the consignee. This leaves
fewer than 48 hours for mandated third-party microbial and chemical assay testing.

We propose reverting to a minimum of 21 business days commencing from customs out-of-charge
clearance, consistent with standard industry practice for pharmaceutical and cosmetic imports
into India.

We remain open to discussion and request a revised draft within 5 business days.

Regards,
Maya Rao
Commercial Operations Lead, Auric Consumer Brands"""
        },
        {
            "id": "c3",
            "task": "Confirm tooling release or buyout",
            "party": "Supplier",
            "owner": "Maya Rao (Commercial Ops)",
            "trigger": "Contract termination/transition",
            "deadline": "Pre-Execution Gate",
            "status": "Tracked",
            "clause": "§4.2",
            "confidence": "95%",
            "verbatim": "Molds remain Supplier property unless Buyer remits USD 12,000 unamortized tooling buyout fee.",
            "impact": "Exit cost requires a formal release plan before initial production run.",
            "pushback_email": """Subject: Dispute of Tooling Ownership Clause — Section 4.2 Counter-Draft

Dear Pacific Rim Formulations Ltd,

We formally dispute the tooling ownership provision introduced in Section 4.2 of your counter-draft.

All custom bottle molds were commissioned and fully funded by Auric Consumer Brands Pvt Ltd as
evidenced by our tooling setup invoices dated [INVOICE DATE]. Under general IP principles and our
original baseline agreement, these molds constitute Buyer's exclusive intellectual property.

The introduction of a USD 12,000 unamortized buyout fee to release assets already paid for by
Auric is without basis. We request that Section 4.2 be reinstated to its original form confirming
Buyer's exclusive ownership of all custom tooling.

Regards,
Maya Rao
Commercial Operations Lead, Auric Consumer Brands"""
        },
        {
            "id": "c4",
            "task": "Submit Bill of Lading invoice",
            "party": "Supplier",
            "owner": "Finance Operations",
            "trigger": "Vessel dispatch notification",
            "deadline": "Net 15 upon B/L issue",
            "status": "Scheduled",
            "clause": "§2.2",
            "confidence": "98%",
            "verbatim": "Fifty percent (50%) balance payable against surrender of Bill of Lading copy prior to port arrival.",
            "impact": "Working capital leaves 100% before quality clearance.",
            "pushback_email": """Subject: Objection to B/L-Linked Payment Structure — Section 2.2 Counter-Draft

Dear Pacific Rim Formulations Ltd,

We write to object to the revised payment structure in Section 2.2 of your counter-draft, which
requires 100% of consideration to be disbursed prior to destination inspection.

The original baseline provided for 70% balance payment Net 30 following quality clearance at
Nhava Sheva port — a structure that protects both parties and incentivises conforming delivery.

Requiring 50% against Bill of Lading eliminates all financial recourse in the event of
contaminated, damaged, or non-conforming batches arriving at destination. We propose retaining
at minimum 30% of the contract value as a post-destination inspection holdback.

Regards,
Maya Rao
Commercial Operations Lead, Auric Consumer Brands"""
        }
    ],
    "changes": [
        {
            "clause": "§3.1",
            "title": "Inspection window compressed",
            "severity": "HIGH IMPACT",
            "base": "30 business days",
            "counter": "7 calendar days",
            "reading": "Deemed acceptance now arrives faster. Indian customs clearance requires 4–6 days; leaving <48 hours for microbial assay testing.",
            "action": "Create a 7-day lab clearance task for Mumbai Quality, or push back to 21 business days post-customs clearance."
        },
        {
            "clause": "§2.2",
            "title": "Payment structure changed",
            "severity": "MATERIAL",
            "base": "30% advance, 70% Net 30 post-destination clearance",
            "counter": "50% advance, 50% against Bill of Lading (B/L)",
            "reading": "Working capital moves forward. 100% of cash leaves before goods land at Nhava Sheva port.",
            "action": "Retain at least 30% balance payable post-destination assay sign-off."
        },
        {
            "clause": "§4.2",
            "title": "Tooling buyout added",
            "severity": "MATERIAL",
            "base": "Molds remain Buyer exclusive property",
            "counter": "$12,000 unamortized buyout fee",
            "reading": "Exit cost requires a release plan. Supplier can hold proprietary bottle molds hostage upon non-renewal.",
            "action": "Reassert Buyer tooling ownership backed by initial tooling commissioning invoices."
        },
        {
            "clause": "§5.2",
            "title": "Auto-renewal introduced",
            "severity": "HIGH IMPACT",
            "base": "Annual renewal on mutual written agreement",
            "counter": "Mandatory 2-year auto-renewal unless 90 days prior notice",
            "reading": "Notice deadline is operationally critical. Missing 02 Aug 2027 locks forward volume.",
            "action": "Set deterministic calendar hold with Commercial Ops Lead immediately."
        }
    ]
}

# ----------------- TOP BAR -----------------
col_b1, col_b2, col_b3 = st.columns([2, 2, 1])
with col_b1:
    st.markdown('<span style="font-size:12px; color:#64748B;">Workspace &gt; Commercial Control Room</span>', unsafe_allow_html=True)
with col_b2:
    active_file = st.session_state.get("active_file", "")
    if st.session_state.get("ingested") and active_file:
        label = f"● {active_file} · Active"
        bg, color, border = "#ECFDF5", "#047857", "#A7F3D0"
    else:
        label = "● Data Synced 09:42 IST · All Systems Nominal"
        bg, color, border = "#ECFDF5", "#047857", "#A7F3D0"
    st.markdown(
        f'<div style="text-align:center;">'
        f'<span style="background:{bg}; color:{color}; border:1px solid {border}; '
        f'padding:5px 12px; border-radius:20px; font-size:12px; font-weight:700; '
        f'white-space:nowrap; display:inline-block;">{label}</span></div>',
        unsafe_allow_html=True
    )
with col_b3:
    if st.button("↗ Export Brief", use_container_width=True):
        st.toast("Commercial Governance Brief generated for Maya Rao.")

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### 🔷 ContractLens")
    st.caption("Commercial Governance Control Room")
    st.write("")

    view = st.radio(
        "CONTROL ROOM",
        [
            "Executive Overview",
            "Agreements & Commitments",
            "Change Intelligence",
            "Decision Copilot",
            "Operational Assurance"
        ]
    )

    st.divider()
    st.caption("AGREEMENT IN FOCUS")
    st.markdown("**Master Manufacturing &amp; Supply Agreement**")
    if st.session_state.get("active_file"):
        st.caption(f"📄 {st.session_state['active_file']}")
    st.caption("Auric Consumer Brands · FY27")
    st.markdown("Health Score: `78 / 100`")
    st.progress(78)

    st.write("")
    st.markdown("**Maya Rao**  \n`Commercial Operations Lead`")

# =====================================================================
# VIEW 1: EXECUTIVE OVERVIEW
# =====================================================================
if view == "Executive Overview":
    st.markdown('<div style="margin: 8px 0 16px 0;">', unsafe_allow_html=True)
    st.caption("MONDAY / GOVERNANCE PULSE")
    st.markdown('<h1 class="serif-title">Good morning, <em>operator.</em></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; font-size:14px; margin-top:2px;">Here is what needs your attention across active commercial agreements.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">PORTFOLIO HEALTH</span>
<div style="font-size:30px; font-weight:800; color:#0F172A; margin:4px 0 2px 0;">{PORTFOLIO['health']} <span style="font-size:15px; color:#94A3B8;">/ 100</span></div>
<span class="badge-ok">↗ +4.6% Across 12 active contracts</span>
</div>
""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">MANAGED VALUE</span>
<div style="font-size:30px; font-weight:800; color:#0F172A; margin:4px 0 2px 0;">{PORTFOLIO['managed_val']}</div>
<span style="font-size:12px; color:#64748B;">{PORTFOLIO['managed_val_inr']} · 12 active contracts</span>
</div>
""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">UNMITIGATED EXPOSURE</span>
<div style="font-size:30px; font-weight:800; color:#DC2626; margin:4px 0 2px 0;">{PORTFOLIO['exposure']}</div>
<span class="badge-crit">{PORTFOLIO['exposure_inr']} · 3 pending actions</span>
</div>
""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">NEXT CONTROL DATE</span>
<div style="font-size:30px; font-weight:800; color:#D97706; margin:4px 0 2px 0;">{PORTFOLIO['next_date']}</div>
<span style="font-size:12px; color:#64748B;">Renewal notice cutoff · §5.2</span>
</div>
""", unsafe_allow_html=True)

    st.write("")
    col_agr, col_pri = st.columns([2, 1])
    with col_agr:
        st.markdown(f"""
<div class="metric-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span style="font-size:11px; font-weight:700; color:#64748B;">AGREEMENT IN FOCUS</span>
<span class="badge-ok">ACTIVE · MONITORED</span>
</div>
<h3 style="margin:6px 0 2px 0; font-size:18px;">{AGREEMENT['title']}</h3>
<span style="font-size:13px; color:#64748B;">{AGREEMENT['parties']}</span>
<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-top:14px;">
<div><span style="font-size:11px; color:#64748B;">ANNUAL VALUE</span><br><strong style="font-size:14px;">$45,000</strong><br><span style="font-size:11px; color:#94A3B8;">USD-fixed</span></div>
<div><span style="font-size:11px; color:#64748B;">TERM</span><br><strong style="font-size:14px;">12 Months</strong><br><span style="font-size:11px; color:#94A3B8;">01 Nov 26 – 31 Oct 27</span></div>
<div><span style="font-size:11px; color:#64748B;">ATTENTION</span><br><strong style="font-size:14px; color:#DC2626;">3 Items</strong><br><span style="font-size:11px; color:#DC2626;">1 due this month</span></div>
</div>
<div class="card-insight">
<strong style="color:#166534; font-size:13px;">💡 The operating risk moved, not the headline value.</strong>
<p style="font-size:13px; color:#14532D; margin:4px 0 0 0; line-height:1.5;">A 7-day deemed-acceptance window and a 50% advance payment against Bill of Lading now matter more than the $45,000 annual value.</p>
</div>
</div>
""", unsafe_allow_html=True)
    with col_pri:
        st.markdown(f"""
<div class="metric-card" style="height:100%;">
<span style="font-size:11px; font-weight:700; color:#64748B;">PRIORITY ACTION</span>
<h3 class="serif-sub" style="margin:6px 0 4px 0;">Protect the renewal decision.</h3>
<p style="font-size:13px; color:#475569; line-height:1.5; margin-top:6px;">The §5.2 notice deadline is <strong>12 days away</strong>. Assign an owner now so a missed notice does not create a mandatory two-year commitment.</p>
<div style="margin-top:20px; padding-top:12px; border-top:1px solid #E2E8F0; font-size:12px;">
<span style="color:#64748B;">OWNER:</span> <strong>Maya Rao · Commercial Ops</strong>
</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# VIEW 2: AGREEMENTS & COMMITMENTS
# =====================================================================
elif view == "Agreements & Commitments":
    st.markdown('<span style="font-size:11px; color:#64748B; font-weight:700;">AGREEMENT MANAGEMENT / COMMITMENT REGISTER</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="serif-title">One agreement. <em>Every promise.</em></h1>', unsafe_allow_html=True)
    st.caption("A clause-level operating register for Master Manufacturing & Supply Agreement.")
    st.write("")

    # ── CONTRACT INGESTION WORKFLOW ──────────────────────────────────
    with st.expander("📂 Upload Executed Agreement or Counter-Draft", expanded=not st.session_state.get("ingested", False)):
        uploaded = st.file_uploader(
            "Upload Executed Agreement or Counter-Draft",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )
        if uploaded:
            st.session_state["ingested"] = True
            st.session_state["active_file"] = uploaded.name

    if st.session_state.get("ingested"):
        fname = st.session_state.get("active_file", "document")
        st.markdown(f"""
<div class="ingest-step">
✓ <strong>Ingestion complete</strong> · {fname} parsed into <strong>14 clause nodes</strong> · hash <code>8d3f...c912</code>
</div>
<div class="ingest-step">
✓ <strong>Exact substring grounding:</strong> <strong>100% verified</strong> across 4 clause anchors · 0 unsupported claims
</div>
<div class="ingest-step">
✓ <strong>Deterministic state machine generated:</strong> <strong>4 active commitments</strong> mapped · renewal cutoff calculated at 02 Aug 2027
</div>
""", unsafe_allow_html=True)
        st.write("")

    # ── DUAL-PANE LAYOUT ─────────────────────────────────────────────
    col_tbl, col_drawer = st.columns([1.5, 1])

    with col_tbl:
        st.markdown("#### Operational Obligations")
        for item in AGREEMENT["commitments"]:
            p_badge = "badge-crit" if item["status"] == "At risk" else ("badge-warn" if "Action" in item["status"] else "badge-ok")
            st.markdown(f"""
<div class="metric-card" style="margin-bottom:10px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<strong style="font-size:14px; color:#0F172A;">{item['task']}</strong>
<span class="{p_badge}">{item['status']}</span>
</div>
<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px; margin-top:8px; font-size:12px;">
<div><span style="color:#64748B;">Party / Owner:</span><br><strong>{item['owner']}</strong></div>
<div><span style="color:#64748B;">Trigger:</span><br>{item['trigger']}</div>
<div><span style="color:#64748B;">Cutoff Date:</span><br><span style="color:#DC2626; font-weight:700;">{item['deadline']}</span></div>
</div>
</div>
""", unsafe_allow_html=True)
            if st.button(f"Inspect Evidence ({item['clause']})", key=f"sel_{item['id']}"):
                st.session_state["selected_evidence"] = item
                st.session_state["show_pushback"] = False

    with col_drawer:
        sel = st.session_state.get("selected_evidence", AGREEMENT["commitments"][0])

        st.markdown(f"""
<div class="evidence-panel">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span style="font-size:11px; color:#0284C7; font-weight:700;">{sel['clause']} · SOURCE-GROUNDED</span>
<span class="badge-ok">{sel['confidence']} CONFIDENT</span>
</div>
<h3 style="margin:8px 0 12px 0; font-size:18px;">{sel['task']}</h3>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:14px; font-size:12px;">
<div style="background:#F8FAFC; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0;">
<span style="color:#64748B;">OWNER</span><br><strong>{sel['owner'].split(' (')[0]}</strong>
</div>
<div style="background:#F8FAFC; padding:8px 12px; border-radius:6px; border:1px solid #E2E8F0;">
<span style="color:#64748B;">DEADLINE</span><br><strong style="color:#DC2626;">{sel['deadline']}</strong>
</div>
</div>
<span style="font-size:11px; color:#64748B; font-weight:700;">VERBATIM CLAUSE</span>
<div style="background:#F1F5F9; border-left:3px solid #0284C7; padding:12px; border-radius:6px; margin:6px 0 14px 0; font-size:12px; font-style:italic; color:#334155;">
"{sel['verbatim']}"
</div>
<span style="font-size:11px; color:#64748B; font-weight:700;">BUSINESS IMPACT</span>
<p style="font-size:13px; color:#0F172A; margin:4px 0 0 0;">{sel['impact']}</p>
</div>
""", unsafe_allow_html=True)

        st.write("")
        btn_ack, btn_email = st.columns(2)
        with btn_ack:
            if st.button("✓ Acknowledge Control", use_container_width=True, key="ack_btn"):
                st.toast(f"Control acknowledged and dispatched to {sel['owner'].split(' (')[0]}.")
        with btn_email:
            if st.button("✉️ Draft Pushback Email", use_container_width=True, key="email_btn"):
                st.session_state["show_pushback"] = not st.session_state.get("show_pushback", False)

        if st.session_state.get("show_pushback", False):
            st.markdown(f'<div class="pushback-box">{sel["pushback_email"]}</div>', unsafe_allow_html=True)
            if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_btn"):
                st.toast("Email text copied — paste into your mail client.")

# =====================================================================
# VIEW 3: CHANGE INTELLIGENCE
# =====================================================================
elif view == "Change Intelligence":
    st.markdown('<span style="font-size:11px; color:#64748B; font-weight:700;">REVISION COMPARATOR / RISK SHIFTS</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="serif-title">Change intelligence reads <em>exposure</em>, not just text.</h1>', unsafe_allow_html=True)
    st.caption("A commercial exposure shift, not a word count. Comparing the original Auric baseline with the Pacific Rim counter-draft.")
    st.write("")

    for ch in AGREEMENT["changes"]:
        st.markdown(f"""
<div class="metric-card" style="margin-bottom:14px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<strong style="font-size:16px; color:#0F172A;">{ch['clause']} · {ch['title']}</strong>
<span class="badge-crit">{ch['severity']}</span>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:12px;">
<div style="background:#F8FAFC; padding:12px; border-radius:8px; border:1px solid #E2E8F0;">
<span style="font-size:11px; color:#64748B; font-weight:700;">BASELINE · V1.1</span>
<div style="font-size:15px; font-weight:700; color:#059669; margin-top:4px;">{ch['base']}</div>
</div>
<div style="background:#FEF2F2; padding:12px; border-radius:8px; border:1px solid #FECACA;">
<span style="font-size:11px; color:#DC2626; font-weight:700;">COUNTER · V1.2</span>
<div style="font-size:15px; font-weight:700; color:#DC2626; margin-top:4px;">{ch['counter']}</div>
</div>
</div>
<div style="margin-top:12px; font-size:13px; line-height:1.6;">
<strong style="color:#0284C7;">Operational Reading:</strong> <span style="color:#334155;">{ch['reading']}</span><br>
<strong style="color:#D97706;">Recommended Response:</strong> <span style="color:#92400E; font-weight:600;">{ch['action']}</span>
</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# VIEW 4: DECISION COPILOT
# =====================================================================
elif view == "Decision Copilot":
    st.markdown('<span style="font-size:11px; color:#64748B; font-weight:700;">EXECUTIVE INQUIRY</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="serif-title">Decision Copilot answers the question <em>behind the clause.</em></h1>', unsafe_allow_html=True)
    st.caption("Plain-English answers with clause citations across §§2.2, 3.1, 4.2, and 5.2.")
    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1:
        q1 = st.button("What can cost us money under the revised terms?", use_container_width=True)
    with c2:
        q2 = st.button("What happens if lab testing takes 8 days?", use_container_width=True)
    with c3:
        q3 = st.button("Which items require human review and legal escalation?", use_container_width=True)

    val = "What happens if lab testing takes 8 days?"
    if q1: val = "What can cost us money under the revised terms?"
    elif q2: val = "What happens if lab testing takes 8 days?"
    elif q3: val = "Which items require human review and legal escalation?"

    st.text_input("Ask a commercial question:", value=val)

    if "8 days" in val or "lab" in val:
        st.markdown("""
<div class="metric-card" style="border-left:4px solid #DC2626; margin-top:14px;">
<div style="display:flex; justify-content:space-between;">
<strong style="color:#DC2626; font-size:15px;">Irrevocable Deemed Acceptance Risk</strong>
<span class="badge-crit">96% CONFIDENT</span>
</div>
<p style="font-size:14px; color:#334155; margin:10px 0; line-height:1.6;">
Under <strong>Section 3.1</strong> of the counter-draft, failure to provide laboratory sign-offs within <strong>7 calendar days</strong> constitutes irrevocable deemed acceptance of the shipment.
<br><br>
Because Section 2.2 also mandates <strong>100% payment prior to port arrival</strong> (50% advance + 50% Bill of Lading), cash leaves before destination lab clearance. You will have paid <strong>USD 45,000 in full</strong> with zero contractual leverage to return defective or contaminated product.
</p>
<div style="font-size:12px; color:#64748B;">
<strong>Source Evidence:</strong> <code>§3.1 Quality Audit</code> &amp; <code>§2.2 Payment Terms</code> | <span class="badge-warn">Review Gate Required</span>
</div>
</div>
""", unsafe_allow_html=True)
    elif "cost" in val:
        st.markdown("""
<div class="metric-card" style="border-left:4px solid #D97706; margin-top:14px;">
<strong style="color:#D97706; font-size:15px;">Financial Exposure Summary ($51,000 Unmitigated Risk):</strong>
<p style="font-size:14px; color:#334155; margin:10px 0; line-height:1.6;">
1. <strong>USD 12,000 Tooling Buyout (§4.2):</strong> Exit cost requires an unamortized release payment.<br>
2. <strong>USD 45,000 Advance Cash Outflow (§2.2):</strong> 100% payment disbursed before destination lab inspection.<br>
3. <strong>2-Year Renewal Lock-In (§5.2):</strong> Missing the 02 Aug 2027 cutoff commits you to future volume.
</p>
<div style="font-size:12px; color:#64748B;">
<strong>Source Citations:</strong> <code>§§2.2, 4.2, 5.2</code> | <span class="badge-ok">98% Confident</span>
</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="metric-card" style="border-left:4px solid #0284C7; margin-top:14px;">
<strong style="color:#0284C7; font-size:15px;">Human Review Escalation Queue:</strong>
<p style="font-size:14px; color:#334155; margin:10px 0; line-height:1.6;">
• <strong>Dispute Resolution Gate (§6.0):</strong> References to Hong Kong HKIAC arbitration are abstained from autonomous interpretation and held for Legal Operations.<br>
• <strong>Commercial Action Gate (§5.2):</strong> Owner acknowledgement required before sending formal non-renewal notice.
</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# VIEW 5: OPERATIONAL ASSURANCE
# =====================================================================
elif view == "Operational Assurance":
    st.markdown('<span style="font-size:11px; color:#64748B; font-weight:700;">TRUST ARCHITECTURE</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="serif-title">Operational assurance makes trust <em>measurable.</em></h1>', unsafe_allow_html=True)
    st.caption("Governance is treated as a product surface, not a footnote.")
    st.write("")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">EVIDENCE GROUNDING</span>
<div style="font-size:28px; font-weight:800; color:#059669; margin:4px 0 2px 0;">100%</div>
<span style="font-size:12px; color:#64748B;">Clause anchor coverage</span>
</div>
""", unsafe_allow_html=True)
    with m2:
        st.markdown("""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">HUMAN REVIEW GATES</span>
<div style="font-size:28px; font-weight:800; color:#D97706; margin:4px 0 2px 0;">2</div>
<span style="font-size:12px; color:#64748B;">Before high-consequence action</span>
</div>
""", unsafe_allow_html=True)
    with m3:
        st.markdown("""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">PROCESSING LATENCY</span>
<div style="font-size:28px; font-weight:800; color:#0284C7; margin:4px 0 2px 0;">3.4s</div>
<span style="font-size:12px; color:#64748B;">Question to grounded answer</span>
</div>
""", unsafe_allow_html=True)
    with m4:
        st.markdown("""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">UNIT EXECUTION COST</span>
<div style="font-size:28px; font-weight:800; color:#0F172A; margin:4px 0 2px 0;">₹3.20</div>
<span style="font-size:12px; color:#64748B;">$0.038 per governed decision</span>
</div>
""", unsafe_allow_html=True)

    st.write("")
    col_led, col_pos = st.columns([2, 1])

    with col_led:
        st.markdown("#### Evidence Ledger")
        feed_mode = st.radio(
            "ledger_mode",
            ["Audit feed", "Review gates"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if feed_mode == "Audit feed":
            audit_steps = [
                ("01 · Ingestion complete", "09:42:18 IST",
                 "Agreement v1.2 · 14 pages · hash <code>8d3f...c912</code> · file integrity verified"),
                ("02 · Grounding checks passed", "09:42:21 IST",
                 "4 clause anchors confirmed · 0 unsupported claims · verbatim substring match 100%"),
                ("03 · Deterministic date calculation", "09:42:23 IST",
                 "Expiry date 31 Oct 2027 minus 90 days = <strong>02 Aug 2027</strong> · no model inference used"),
                ("04 · HKIAC abstention protocol", "09:42:26 IST",
                 "Foreign arbitration clause detected · no dispute resolution inference made · human gate retained"),
            ]
            for title, ts, detail in audit_steps:
                st.markdown(f"""
<div class="ledger-row">
<div style="display:flex; justify-content:space-between; align-items:baseline;">
<strong style="font-size:13px; color:#0F172A;">{title}</strong>
<span style="font-size:11px; color:#94A3B8;">{ts}</span>
</div>
<span style="font-size:12px; color:#475569;">{detail}</span>
</div>
""", unsafe_allow_html=True)

        else:  # Review gates
            gates = [
                {
                    "name": "Commercial action gate",
                    "status": "PASSED",
                    "badge": "badge-ok",
                    "detail": "Owner acknowledgement required before dispatching formal non-renewal notice (§5.2). Maya Rao confirmed as owner."
                },
                {
                    "name": "Dispute interpretation gate",
                    "status": "RETAINED",
                    "badge": "badge-warn",
                    "detail": "Foreign HKIAC arbitration (§6.0) abstained from autonomous execution. Routed to Legal Operations for jurisdiction review."
                },
            ]
            for g in gates:
                st.markdown(f"""
<div class="ledger-row">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
<strong style="font-size:13px; color:#0F172A;">{g['name']}</strong>
<span class="{g['badge']}">{g['status']}</span>
</div>
<span style="font-size:12px; color:#475569;">{g['detail']}</span>
</div>
""", unsafe_allow_html=True)

    with col_pos:
        st.markdown("""
<div class="metric-card">
<span style="font-size:11px; font-weight:700; color:#64748B;">GOVERNANCE POSTURE</span>
<h4 style="margin:6px 0 10px 0;">Boundaries are explicit.</h4>
<div style="font-size:13px; line-height:1.8; color:#334155;">
<div>✓ <strong>Source traceability:</strong> Clause + page attached</div>
<div>✓ <strong>Abstention:</strong> HKIAC protocol active</div>
<div>✓ <strong>Review ownership:</strong> Maya Rao assigned</div>
</div>
<p style="font-size:12px; color:#64748B; margin-top:12px;">Controls refresh when the agreement changes. No autonomous action can bypass the human review gates.</p>
</div>
""", unsafe_allow_html=True)
