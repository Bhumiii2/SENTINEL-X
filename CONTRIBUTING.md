# Contributing

1. Create a focused branch and explain the change.
2. Add or update tests for transformations, schemas, model behavior, or API contracts.
3. Run `ruff check .` and `pytest` before opening a pull request.
4. Never commit datasets, credentials, private telemetry, model binaries, or generated secrets.
5. Document data provenance, feature definitions, and any changes to model/evaluation assumptions.

Research changes should state the hypothesis, split strategy, baselines, metric, and failure condition. Do not report test-set tuning as generalization.
