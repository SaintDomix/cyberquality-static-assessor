from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .models import AssessmentResult, Status


def write_json(result: AssessmentResult, path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def _safe(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_pdf(result: AssessmentResult, path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="CyberQuality Static Assessment Report",
        author="CyberQuality Static Assessor",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="FindingTitle", parent=styles["Heading3"], spaceBefore=8, spaceAfter=4))

    story = [
        Paragraph("CyberQuality Static Assessor", styles["CenterTitle"]),
        Paragraph("Static Cybersecurity Quality Assessment Report", styles["Heading2"]),
        Spacer(1, 5 * mm),
    ]

    summary = [
        ["Target", Paragraph(_safe(result.target_url), styles["Small"])],
        ["Final URL", Paragraph(_safe(result.final_url), styles["Small"])],
        ["Collected", _safe(result.collected_at)],
        ["HTTP status", str(result.http_status)],
        ["Response time", f"{result.response_time_ms:.1f} ms"],
        ["Overall score", f"{result.overall_score}/100 (Grade {result.grade})"],
    ]
    table = Table(summary, colWidths=[42 * mm, 120 * mm])
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([table, Spacer(1, 5 * mm)])

    counts = result.counts
    count_table = Table(
        [
            ["Critical", "High", "Medium", "Low", "Passed", "N/A"],
            [
                counts["critical"],
                counts["high"],
                counts["medium"],
                counts["low"],
                counts["passed"],
                counts["not_applicable"],
            ],
        ],
        colWidths=[27 * mm] * 6,
    )
    count_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([count_table, Spacer(1, 6 * mm), Paragraph("Dimension scores", styles["Heading2"])])

    dim_data = [["Dimension", "Score"]] + [[name, f"{score}/100"] for name, score in result.dimension_scores.items()]
    dim_table = Table(dim_data, colWidths=[115 * mm, 40 * mm])
    dim_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([dim_table, PageBreak(), Paragraph("Detailed findings", styles["Heading1"])])

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    sorted_findings = sorted(
        result.findings,
        key=lambda f: (0 if f.status == Status.FAIL else 1, order.get(f.severity.value, 9), f.rule_id),
    )
    for item in sorted_findings:
        story.append(
            Paragraph(
                f"{_safe(item.rule_id)} — {_safe(item.title)} [{item.status.value.upper()} / {item.severity.value.upper()}]",
                styles["FindingTitle"],
            )
        )
        detail_rows = [
            ["Category", _safe(item.category)],
            ["Description", Paragraph(_safe(item.description), styles["Small"])],
            ["Evidence", Paragraph(_safe(item.evidence), styles["Small"])],
            ["Recommendation", Paragraph(_safe(item.recommendation), styles["Small"])],
            ["Source", _safe(item.source)],
        ]
        detail = Table(detail_rows, colWidths=[35 * mm, 125 * mm])
        detail.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("PADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.extend([detail, Spacer(1, 3 * mm)])

    story.append(PageBreak())
    story.append(Paragraph("Interpretation and scope", styles["Heading1"]))
    story.append(
        Paragraph(
            "This module performs non-destructive, observable rule-based checks against the supplied HTTP(S) endpoint. "
            "A finding is evidence for a security-control assessment, not proof that an exploit exists. The score is a "
            "transparent weighted summary intended for comparison and prioritization; severe findings should remain visible "
            "even when the overall score is high.",
            styles["BodyText"],
        )
    )

    doc.build(story)
    return output
