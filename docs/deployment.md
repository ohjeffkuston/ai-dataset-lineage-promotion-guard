# Safe deployment guidance

1. Produce the manifest from the data pipeline after quality and PII scans.
2. Run the guard in pull requests and pipeline promotion stages.
3. Begin in report-only mode and measure false positives.
4. Verify referenced object version IDs and digests using read-only cloud APIs.
5. Store policy reports in an immutable, retention-controlled audit location.
6. Require named human approval for production promotion and time-bound exceptions.
7. Test reproducibility by rebuilding a model candidate from a historical manifest.

Use workload identity, least-privilege read access, signed CI artifacts, pinned dependencies, and separation of duties. This project performs no production mutation; promotion remains behind human approval.
