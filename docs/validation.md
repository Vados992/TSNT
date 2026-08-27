# Validation and historical test protocol

## Principle

Backtesting must recreate what the system could have known **before** an event.
A good fit obtained with later revisions, final disruption duration or hindsight
route choices is invalid.

## Event families

The following are candidate test families, not bundled calibration data:

| Family | Freeze point | Observed targets | Primary starting source |
|---|---|---|---|
| Ever Given / Suez, March 2021 | immediately before grounding | transit capacity, queue, restoration time | [Suez Canal Authority](https://www.suezcanal.gov.eg/English/MediaCenter/News/Pages/nav_29-03-2021.aspx) |
| Red Sea rerouting, 2023–2024 | rolling weekly cutoffs | transits, distance, freight-rate interval | [UNCTAD report](https://unctad.org/publication/navigating-troubled-waters-impact-global-trade-disruption-shipping-routes-red-sea-black) |
| Panama drought, 2023–2024 | before each shipping advisory | daily slots, draft, waiting time | [Panama Canal Authority](https://pancanal.com/en/a-timeline-of-recent-future-progress-at-the-panama-canal/) |
| EU/Russian gas, 2021–2022 | monthly publication vintages | delivered volume, storage, substitution | [European Commission REPowerEU](https://enlargement.ec.europa.eu/news/repowereu-plan-rapidly-reduce-dependence-russian-fossil-fuels-and-fast-forward-green-transition-2022-05-18_en) |
| Taiwan-area crisis windows | pre-announced timestamp cutoffs | public aggregate shipping/market effects | official public notices and licensed aggregates only |

The Taiwan family must remain aggregate and non-operational. Do not publish
targetable infrastructure, unit movement, personal or classified data.

## Backtest procedure

1. Pre-register event, cutoff, target variables, horizon and baseline.
2. Freeze source versions and store content hashes.
3. Fit/calibrate using only records with transaction_time <= cutoff.
4. Run a deterministic baseline and a declared uncertainty ensemble.
5. Reveal observations after the horizon.
6. Score point, interval, rank and recovery outputs.
7. Repeat across event families; do not tune on the final held-out family.
8. Publish failures, missingness and model changes.

## Metrics

| Output | Minimum metric set |
|---|---|
| Continuous flow/cost/time/output | MAE, RMSE, sMAPE |
| Quantiles | pinball loss for each declared quantile |
| Prediction interval | empirical coverage and width |
| Binary exceedance | Brier score and calibration plot |
| Structural ranking | Kendall/Spearman stability |
| Recovery | TTR error and service-loss-area error |
| Analyst scoring | ICC(2,k), Kendall W and disagreement intervals |

A model must beat a declared simple baseline (for example persistence,
seasonality or unchanged routing), not only report low in-sample error.

## Inter-rater protocol

At least three analysts independently score the same blinded evidence packet.
Record both raw scores and written rationale. Calculate ICC(2,k) for averaged
continuous scores and Kendall W for ranking concordance. Large disagreement
triggers adjudication and wider uncertainty; averaging does not erase it.

## Acceptance gates

Thresholds are deployment-specific and must be set before testing. A release
should require, at minimum:

- no temporal leakage;
- complete run manifest and source hashes;
- dimensional and flow-balance checks;
- expected interval coverage within a pre-declared tolerance;
- non-degrading held-out skill against baseline;
- documented sensitivity and rank stability;
- independent review of model and data changes.

Passing tests demonstrates implementation consistency, not universal empirical
validity.
