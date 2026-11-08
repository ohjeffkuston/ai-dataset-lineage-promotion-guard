import yaml

from dataset_lineage_guard.analyzer import analyze_manifest


def manifest():
    with open("samples/compliant-manifest.yaml", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_compliant_manifest_passes():
    report = analyze_manifest(manifest())
    assert report["decision"] == "PASS"
    assert report["score"] == 100


def test_unversioned_uri_blocks():
    item = manifest(); item["dataset"]["uri"] = "s3://bucket/data.parquet"
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_bad_digest_blocks():
    item = manifest(); item["dataset"]["digest"] = "latest"
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_missing_schema_blocks():
    item = manifest(); item["dataset"]["schema_version"] = ""
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_quality_failure_blocks():
    item = manifest(); item["quality"]["validity"] = 0.80
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_missing_quality_report_requires_review():
    item = manifest(); item["quality"]["report_digest"] = ""
    assert analyze_manifest(item)["decision"] == "REVIEW"


def test_missing_pii_scan_blocks():
    item = manifest(); item["privacy"]["pii_scan_status"] = "unknown"
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_missing_encryption_blocks():
    item = manifest(); item["privacy"]["encryption_at_rest"] = False
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_unapproved_license_blocks():
    item = manifest(); item["governance"]["usage_approved"] = False
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_missing_lineage_blocks():
    item = manifest(); item["lineage"]["transformations"] = []
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_split_overlap_blocks():
    item = manifest(); item["usage"]["splits"]["test"]["digest"] = "sha256:1111"
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_missing_workflow_reference_requires_review():
    item = manifest(); item["usage"]["evaluation_run_id"] = ""
    assert analyze_manifest(item)["decision"] == "REVIEW"


def test_invalid_retention_requires_review():
    item = manifest(); item["governance"]["retention_days"] = 0
    assert analyze_manifest(item)["decision"] == "REVIEW"


def test_missing_human_approval_blocks():
    item = manifest(); item["governance"]["approval"]["status"] = "pending"
    assert analyze_manifest(item)["decision"] == "BLOCK"


def test_missing_immutable_audit_requires_review():
    item = manifest(); item["governance"]["audit_record"]["immutable"] = False
    assert analyze_manifest(item)["decision"] == "REVIEW"
