from __future__ import annotations

import argparse
import json

from .analyzer import analyze_manifest, load_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI dataset lineage before promotion")
    parser.add_argument("manifest")
    args = parser.parse_args()
    report = analyze_manifest(load_manifest(args.manifest))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["decision"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
