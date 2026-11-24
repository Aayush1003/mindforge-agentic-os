"""Check whether a study report contains enough evidence for human review."""

from __future__ import annotations

import argparse
import json


REQUIRED_EVIDENCE = (
    "methods",
    "data",
    "code",
    "uncertainty",
    "negative_results",
    "independent_reproduction",
)


def verify_reproducibility(report: dict[str, bool] | None = None) -> dict[str, object]:
    """Audit a compact evidence report and return traceable checklist results.

    The input should contain one boolean key for each item in
    ``REQUIRED_EVIDENCE``. A false or missing value means the evidence is not
    established. This is a small decision aid, not an expert scientific audit.
    """
    report = {} if report is None else report
    findings = {
        item: bool(report.get(item, False))
        for item in REQUIRED_EVIDENCE
    }
    present = [item for item, available in findings.items() if available]
    missing = [item for item, available in findings.items() if not available]

    if not missing:
        status = "complete"
    elif len(present) >= 4:
        status = "partially_complete"
    else:
        status = "insufficient"

    return {
        "experiment": "human-readable reproducibility and uncertainty verifier",
        "status": status,
        "evidence_checks": findings,
        "missing_evidence": missing,
        "measured_outcome": (
            f"{len(present)} of {len(REQUIRED_EVIDENCE)} essential evidence items confirmed"
        ),
        "human_role": (
            "A person must inspect the underlying study, question every false or "
            "missing item, and judge whether the evidence is sufficient."
        ),
        "interpretation": (
            "The checklist helps organize review; it does not prove a claim, "
            "establish causation, or replace independent reproduction."
        ),
        "caveat": (
            "A report can answer every checklist item inaccurately. Sources and "
            "data should be verified independently before any result is accepted."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        required=True,
        help="JSON object with evidence keys set to true or false",
    )
    args = parser.parse_args()

    try:
        report = json.loads(args.report)
    except json.JSONDecodeError as error:
        parser.error(f"--report must be valid JSON: {error.msg}")

    if not isinstance(report, dict):
        parser.error("--report must be a JSON object")

    unexpected = set(report) - set(REQUIRED_EVIDENCE)
    if unexpected:
        parser.error(
            "--report contains unknown evidence keys: " + ", ".join(sorted(unexpected))
        )

    if any(not isinstance(value, bool) for value in report.values()):
        parser.error("Every evidence value must be true or false")

    print(json.dumps(verify_reproducibility(report), indent=2))


if __name__ == "__main__":
    main()
