from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

from cyberquality.collector import CollectionError
from cyberquality.engine import scan
from cyberquality.models import Status
from cyberquality.reporting import write_pdf

st.set_page_config(page_title="CyberQuality Static Assessor", page_icon="🛡️", layout="wide")

st.title("🛡️ CyberQuality Static Assessor")
st.caption("Static rule-based cybersecurity assessment module for adaptive educational platforms")

with st.sidebar:
    st.header("Assessment settings")
    target = st.text_input("Target URL", value="http://127.0.0.1:8765/insecure")
    timeout = st.slider("Timeout (seconds)", min_value=2, max_value=30, value=10)
    insecure = st.checkbox("Disable TLS verification (lab targets only)", value=False)
    st.markdown("---")
    st.markdown(
        "This tool performs non-destructive observable checks only. "
        "Use it on systems you own or are authorized to assess."
    )

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("Run assessment", type="primary", use_container_width=True):
    try:
        with st.spinner("Collecting evidence and evaluating rules..."):
            st.session_state.result = scan(target, timeout=timeout, verify_tls=not insecure)
    except (CollectionError, ValueError) as exc:
        st.error(str(exc))
        st.session_state.result = None

result = st.session_state.result
if result:
    score_col, grade_col, high_col, medium_col = st.columns(4)
    score_col.metric("Security score", f"{result.overall_score}/100")
    grade_col.metric("Grade", result.grade)
    high_col.metric("High findings", result.counts["high"])
    medium_col.metric("Medium findings", result.counts["medium"])

    st.subheader("Dimension scores")
    for dimension, score in result.dimension_scores.items():
        left, right = st.columns([4, 1])
        left.progress(score / 100, text=dimension)
        right.write(f"**{score}/100**")

    st.subheader("Findings")
    rows = []
    for item in result.findings:
        rows.append(
            {
                "Rule": item.rule_id,
                "Status": item.status.value.upper(),
                "Severity": item.severity.value.upper(),
                "Category": item.category,
                "Finding": item.title,
                "Evidence": item.evidence,
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)

    failed = [item for item in result.findings if item.status == Status.FAIL]
    st.subheader("Recommendations")
    if not failed:
        st.success("No failed checks in the current rule set.")
    for item in failed:
        with st.expander(f"{item.rule_id} · {item.title} · {item.severity.value.upper()}"):
            st.write(item.description)
            st.code(item.evidence, language=None)
            st.write("**Recommendation:**", item.recommendation)

    json_bytes = json.dumps(result.to_dict(), indent=2, ensure_ascii=False).encode("utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "cyberquality-report.pdf"
        write_pdf(result, pdf_path)
        pdf_bytes = pdf_path.read_bytes()

    dl1, dl2 = st.columns(2)
    dl1.download_button(
        "Download JSON report",
        data=json_bytes,
        file_name="cyberquality-assessment.json",
        mime="application/json",
        use_container_width=True,
    )
    dl2.download_button(
        "Download PDF report",
        data=pdf_bytes,
        file_name="cyberquality-assessment.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
