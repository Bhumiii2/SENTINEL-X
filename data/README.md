# Data directory

Raw datasets are intentionally not committed.

- `raw/`: original publisher downloads; immutable locally.
- `external/`: externally sourced assets with separate provenance.
- `interim/`: validated/intermediate transformations.
- `processed/`: curated model-ready Parquet and split manifests.

For every dataset, create a data card recording publisher/source URL, retrieval date, license, checksum, schema, row counts, label distribution, missingness, duplicates, preprocessing, and known limitations. Split before fitting any preprocessing. Keep labels and attack-family metadata out of model feature tensors.
