# Security Policy

SENTINEL-X is a defensive research and demonstration project.

## Supported scope
- Public benchmark datasets.
- Network telemetry from systems you own or are explicitly authorized to monitor.
- Controlled local replay and testing.

## Reporting
Do not publish sensitive traffic captures, credentials, private IP inventories, or exploitable details in public issues. Report suspected vulnerabilities privately to the repository maintainer.

## Security expectations
- Authenticate ingestion and administrative endpoints.
- Validate payload schemas and cap request sizes/rates.
- Apply least-privilege IAM and keep secrets outside source control.
- Restrict retention and mask network identifiers where possible.
- Checksum/sign model artifacts and audit analyst feedback.
