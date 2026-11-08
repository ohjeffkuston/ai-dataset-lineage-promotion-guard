# Demand and technical validation

Checked 2026-11-08.

## Authoritative sources

- [Amazon SageMaker ML Lineage Tracking](https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html) connects data preparation, datasets, training, models, and deployment for reproducibility, governance, and audit.
- [Querying SageMaker lineage entities](https://docs.aws.amazon.com/sagemaker/latest/dg/querying-lineage-entities.html) documents upstream and downstream dataset, job, model, endpoint, and pipeline relationships.
- [Google Cloud pipeline artifact lineage](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/pipelines/lineage) records training and evaluation metadata and dataset/model resources.
- [AWS Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) treats data and artifact lineage as a reproducibility and governance concern.

## Live demand signal

Current remote U.S. ML-platform and data-platform postings reviewed on 2026-11-08 repeatedly asked for lineage, versioning, reproducibility, data quality, distributed systems, Kubernetes, cloud platforms, CI/CD, and secure ML infrastructure. Salary examples surfaced from roughly $149,000 to above $280,000 base, but the strongest roles were senior or staff scopes and were assessed separately for eligibility.

## Rationale

This is a production platform problem, not a generic AI demo. Dataset identity and lineage are required to reproduce model behavior, investigate incidents, enforce privacy and licensing policy, and establish trustworthy promotion evidence.
