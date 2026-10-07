from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .collector import CollectionError
from .engine import scan
from .models import Status
from .reporting import write_json, write_pdf


def _print_summary(result) -> None:
    print("\nCyberQuality Static Assessor")
    print("=" * 58)
    print(f"Target:       {result.target_url}")
    print(f"Final URL:    {result.final_url}")
    print(f"HTTP status:  {result.http_status}")
    print(f"Response:     {result.response_time_ms:.1f} ms")
    print(f"Score:        {result.overall_score}/100 (Grade {result.grade})")
    print("-" * 58)
    print(
        "Findings: "
        f"critical={result.counts['critical']}  high={result.counts['high']}  "
        f"medium={result.counts['medium']}  low={result.counts['low']}  passed={result.counts['passed']}"
    )
    print("\nFailed checks:")
    failed = [finding for finding in result.findings if finding.status == Status.FAIL]
    if not failed:
        print("  No failed checks in the current rule set.")
    for finding in failed:
        print(f"  [{finding.severity.value.upper():8}] {finding.rule_id}  {finding.title}")
        print(f"             Evidence: {finding.evidence}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Static rule-based cybersecurity assessor")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_parser = sub.add_parser("scan", help="Assess an HTTP(S) endpoint")
    scan_parser.add_argument("--url", required=True, help="Target URL")
    scan_parser.add_argument("--output", default="reports/assessment", help="Output path prefix")
    scan_parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds")
    scan_parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification for a controlled laboratory target",
    )

    sub.add_parser("demo-server", help="Start the deterministic local demonstration target")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo-server":
        from demo.demo_server import run

        run()
        return 0

    prefix = Path(args.output)
    try:
        result = scan(args.url, timeout=args.timeout, verify_tls=not args.insecure)
    except (CollectionError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    json_path = write_json(result, prefix.with_suffix(".json"))
    pdf_path = write_pdf(result, prefix.with_suffix(".pdf"))
    _print_summary(result)
    print(f"\nJSON report: {json_path}")
    print(f"PDF report:  {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
