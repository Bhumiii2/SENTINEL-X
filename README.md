# SENTINEL-X
### Autonomous Cyber Threat Detection & Intelligence Platform

SENTINEL-X is a defensive research and engineering platform for network intrusion detection. It ingests public or explicitly authorized network-flow telemetry, detects known and unusual behaviour, correlates related alerts into incidents, and presents evidence-backed explanations through an analyst-facing application.

> **Status:** Initial repository scaffold (v0.1.0). Models, ingestion pipelines, and cloud infrastructure are not implemented yet.

## Mission and research focus

The core research question is whether sequence-aware, self-supervised representation learning improves detection of withheld attack families at a fixed false-positive budget compared with strong tabular baselines.

The engineering goal is a reproducible platform with offline replay, authenticated inference, incident context, model lineage, monitoring, and cost-controlled AWS deployment.

**Important limitation:** SENTINEL-X is a defensive research/demo platform, not a claim of production-ready zero-day detection. Novel-attack detection is a hypothesis to test using withheld-family evaluation, not a guaranteed capability.

## MVP priorities

1. Public flow dataset ingestion, validation, provenance, and canonical schema.
2. Leakage-aware preprocessing and reproducible train/validation/test splits.
3. Logistic regression and Random Forest/XGBoost tabular baselines.
4. One PyTorch temporal model (Transformer or TCN), evaluated against the baselines.
5. One novelty method (autoencoder or contrastive encoder).
6. Authenticated FastAPI inference and offline trace replay.
7. Deterministic incident grouping, analyst evidence, and a usable dashboard.
8. Experiment tracking, drift/operational monitoring, tests, and lean AWS deployment.

GraphSAGE/GAT, continual learning, and threat-intelligence enrichment are stretch extensions. Build them only after the baseline, temporal model, and novelty method are evaluated.

## Architecture

```text
Public datasets / authorized lab flow logs
                 |
          Ingest + validate
                 |
        Versioned raw storage (S3)
                 |
       Transform + leakage-safe split
                 |
    Curated Parquet + feature manifest
                 |
       +---------+----------+
       |                    |
   Model training       Offline replay
       |                    |
 LogReg / XGBoost /       Queue (SQS)
 PyTorch temporal            |
       |                FastAPI inference
 MLflow + model registry    |
       +--------------------+
                 |
            Event store
                 |
       Deterministic incident
          correlation
                 |
         Analyst dashboard
                 |
      CloudWatch + drift + feedback
```

The local-first path uses Python, Polars/Pandas, Parquet, and Make/DVC. Kafka/MSK is not a default requirement: SQS is the preferred low-cost queue for the portfolio demo unless a measured need justifies Kafka.

## Repository map

```text
sentinel-x/
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── pyproject.toml
├── dvc.yaml
├── configs/
├── data/
│   └── README.md
├── docs/
│   ├── architecture/
│   ├── adrs/
│   ├── model-cards/
│   └── data-cards/
├── src/sentinel_x/
│   ├── ingestion/
│   ├── validation/
│   ├── features/
│   ├── datasets/
│   ├── models/
│   │   ├── baselines/
│   │   ├── temporal/
│   │   └── novelty/
│   ├── training/
│   ├── evaluation/
│   ├── explainability/
│   ├── correlation/
│   ├── serving/
│   └── monitoring/
├── api/
├── dashboard/
├── replay/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── ml/
│   └── security/
├── infra/terraform/
├── docker/
├── .github/workflows/
├── scripts/
├── notebooks/exploration_only/
└── reports/figures/
```

## Quickstart

Python 3.11+ is required.

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Optional dependencies are deliberately separated:

```bash
pip install -e ".[ml]"                 # PyTorch
pip install -e ".[tracking]"           # MLflow
pip install -e ".[explainability]"     # SHAP
pip install -e ".[aws]"                # AWS SDK
```

Run the initial checks:

```bash
pytest
ruff check .
```

## Data governance and evaluation rules

- Download datasets from their original publishers and preserve license terms and citations.
- Record source URL, retrieval date, checksum, license, schema, row counts, labels, missingness, and duplicates in a data card.
- Keep raw data out of Git. Do not commit private traffic captures, credentials, or sensitive identifiers.
- Split data before fitting encoders, imputers, scalers, feature selectors, or resampling steps.
- Prefer chronological/grouped splits where metadata permits; retain an untouched final holdout.
- For novelty claims, withhold complete attack families from training and calibration, not random rows from known families.
- Never pass `label` or `attack_family` into the model feature path.
- Compare models using PR-AUC and recall at fixed false-positive rates, not accuracy alone.
- Report negative findings, uncertainty, class prevalence, and limitations.

Initial datasets: UNSW-NB15 (primary supervised baseline) and CICIDS2017 (independent benchmark). Verify dataset terms and provenance before use.

## API direction

The planned API contract includes authenticated `POST /v1/events`, `POST /v1/predict`, `POST /v1/replay/jobs`, incident listing/detail/feedback routes, model metadata, and `/healthz` plus `/readyz`. Do not expose raw ingestion anonymously.

## AWS deployment philosophy

Start local-first. The intended lean deployment uses S3 for versioned data/artifacts, one CPU ECS Fargate or small EC2 API deployment, SQS for asynchronous replay, MLflow with S3 artifacts, CloudWatch for telemetry, IAM/Secrets Manager for identity and secrets, and Terraform for infrastructure-as-code. Train locally or with ephemeral jobs; avoid always-on GPU endpoints, EKS, MSK, and costly managed databases without evidence they are needed.

Set AWS budget alerts, tag resources, and provide teardown scripts before deploying billable infrastructure. The blueprint's AUD budget bands are planning allowances, not quotes.

## Roadmap

| Weeks | Milestone | Exit artifact |
|---|---|---|
| 1–2 | Setup, threat model, dataset license and data cards | Repo, README, ADRs, dataset manifest |
| 3–4 | Ingestion, cleaning, leakage-safe splits | Validated Parquet and data tests |
| 5–6 | Baseline ML and tracking | Logistic/XGBoost results + MLflow |
| 7–9 | Temporal PyTorch model | Reproducible checkpoints and ablations |
| 10–11 | Self-supervised pretraining/fine-tuning | Novelty and fine-tuning study |
| 12–13 | API, replay, incident rules | Integrated authenticated demo |
| 14–16 | AWS, IaC, observability | Bounded demo with cost alarms |
| 17–18 | Robustness and calibration | Final holdout report |
| 19–20 | UI and documentation | Portfolio-ready v1.0 |
| 21–24 | Optional graph extension | GNN study and research write-up |

## Intended use and safety

For authorized defensive monitoring, public-dataset research, and controlled lab testing only. Analyze network telemetry you own or are explicitly authorized to process. No autonomous blocking, offensive exploitation, or unsupported zero-day guarantees are in scope.

See [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md), and the architecture notes before contributing.
