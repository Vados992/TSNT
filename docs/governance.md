# Model governance

## Roles

| Role | Responsibility |
|---|---|
| Data steward | licence, source metadata, retention and access |
| Model owner | equations, assumptions, calibration and limitations |
| Independent validator | held-out tests and challenge analysis |
| Platform owner | security, availability and immutable deployment |
| Analyst | scenario contract, evidence review and interpretation |
| Decision owner | accountable use; may not delegate judgment to the engine |

The model owner and independent validator should not be the same person for a
consequential release.

## Change classes

- patch: implementation correction without intended numerical-method change;
- minor: new adapter, metric or backward-compatible model capability;
- major: equation, interpretation, schema or calibration change.

Any change that can alter outputs requires a versioned validation report.
Historical results retain their original code and input hashes.

## Prohibited shortcuts

- converting missing data to zero without a declared rule;
- treating structural importance as event likelihood;
- mixing observed values and analyst estimates without provenance;
- using post-event revisions in pre-event backtests;
- double counting one physical flow across layers;
- suppressing failed scenarios or unfavourable validation cases;
- exposing personal, classified or targetable infrastructure detail;
- automated consequential decisions without accountable human review.

## Model card requirement

Each deployment publishes purpose, users, excluded uses, data editions,
calibration window, held-out events, metrics, uncertainty, sensitivity,
limitations, security classification, owner and retirement trigger.
