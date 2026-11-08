"""Policy engine for AI dataset promotion evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_manifest(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("manifest must be a YAML mapping")
    return value


def _finding(rule: str, severity: str, passed: bool, message: str) -> dict[str, Any]:
    return {"rule": rule, "severity": severity, "passed": passed, "message": message}


def analyze_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    dataset = manifest.get("dataset", {})
    quality = manifest.get("quality", {})
    privacy = manifest.get("privacy", {})
    lineage = manifest.get("lineage", {})
    usage = manifest.get("usage", {})
    governance = manifest.get("governance", {})
    findings: list[dict[str, Any]] = []

    uri = str(dataset.get("uri", ""))
    digest = str(dataset.get("digest", ""))
    immutable = uri.startswith(("s3://", "gs://", "az://")) and "versionId=" in uri and digest.startswith("sha256:") and len(digest) == 71
    findings.append(_finding("immutable-identity", "block", immutable, "Dataset has a versioned object-store URI and SHA-256 digest."))

    schema_ok = bool(dataset.get("schema_version")) and bool(dataset.get("format"))
    findings.append(_finding("schema-contract", "block", schema_ok, "Dataset schema and storage format are versioned."))

    quality_ok = float(quality.get("completeness", 0) or 0) >= 0.98 and float(quality.get("validity", 0) or 0) >= 0.98 and float(quality.get("duplicate_rate", 1) or 1) <= 0.02
    findings.append(_finding("quality-thresholds", "block", quality_ok, "Completeness, validity, and duplicate-rate thresholds pass."))

    scan_ok = quality.get("scan_status") == "passed" and bool(quality.get("report_digest"))
    findings.append(_finding("quality-evidence", "review", scan_ok, "A passed quality report is content-addressed."))

    classification = privacy.get("classification")
    pii_ok = classification in {"public", "internal", "confidential", "restricted"} and privacy.get("pii_scan_status") == "passed"
    findings.append(_finding("privacy-classification", "block", pii_ok, "Data classification and PII scan result are declared."))

    encryption_ok = privacy.get("encryption_at_rest") is True and privacy.get("encryption_in_transit") is True
    findings.append(_finding("encryption", "block", encryption_ok, "Encryption is required at rest and in transit."))

    license_ok = bool(governance.get("license")) and bool(governance.get("owner")) and governance.get("usage_approved") is True
    findings.append(_finding("license-owner", "block", license_ok, "License, accountable owner, and approved usage are recorded."))

    sources = lineage.get("sources", [])
    transformations = lineage.get("transformations", [])
    lineage_ok = bool(sources) and all(str(item.get("digest", "")).startswith("sha256:") for item in sources if isinstance(item, dict)) and bool(transformations) and all(item.get("code_commit") and item.get("run_id") for item in transformations if isinstance(item, dict))
    findings.append(_finding("source-output-lineage", "block", lineage_ok, "Sources and transformations are content-addressed and reproducible."))

    split = usage.get("splits", {})
    split_ok = all(split.get(name, {}).get("digest") for name in ("train", "validation", "test")) and len({split.get(name, {}).get("digest") for name in ("train", "validation", "test")}) == 3
    findings.append(_finding("split-separation", "block", split_ok, "Train, validation, and test splits have distinct digests."))

    refs_ok = bool(usage.get("training_job_id")) and bool(usage.get("evaluation_run_id")) and bool(usage.get("model_candidate_id"))
    findings.append(_finding("workflow-linkage", "review", refs_ok, "Training, evaluation, and model candidate references are linked."))

    retention = int(governance.get("retention_days", 0) or 0)
    retention_ok = 1 <= retention <= 3650 and bool(governance.get("deletion_policy"))
    findings.append(_finding("retention-deletion", "review", retention_ok, "Retention and deletion policy are bounded."))

    approval = governance.get("approval", {})
    approval_ok = approval.get("status") == "approved" and bool(approval.get("approver")) and bool(approval.get("approved_at"))
    findings.append(_finding("human-approval", "block", approval_ok, "A named human approval is recorded."))

    audit_ok = governance.get("audit_record", {}).get("immutable") is True and bool(governance.get("audit_record", {}).get("uri"))
    findings.append(_finding("immutable-audit", "review", audit_ok, "Promotion evidence is written to an immutable audit record."))

    failed_block = sum(1 for item in findings if not item["passed"] and item["severity"] == "block")
    failed_review = sum(1 for item in findings if not item["passed"] and item["severity"] == "review")
    decision = "BLOCK" if failed_block else ("REVIEW" if failed_review else "PASS")
    score = round(100 * sum(1 for item in findings if item["passed"]) / len(findings))
    return {"dataset": dataset.get("name", "unnamed"), "decision": decision, "score": score, "findings": findings}
