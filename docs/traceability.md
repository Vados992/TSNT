# Requirements traceability

| Architecture requirement | Implementation | Verification |
|---|---|---|
| Temporal multilayer graph | src/tsnt/graph/temporal.py | tests/test_temporal_graph.py |
| Valid-time and knowledge-time firewall | TemporalMultiLayerGraph and backtest.py | temporal and leakage tests |
| AIS/trade/energy/finance/cable seams | src/tsnt/ingestion/connectors.py | fail-closed credential contract |
| CSV and provenance checksum | csv_adapter.py and provenance.py | tests/test_ingestion.py |
| Max-flow/min-cost | optimization/flow.py | tests/test_flow.py |
| Input-output | economics/input_output.py | tests/test_economics.py |
| Cross-layer cascade | cascade/engine.py | tests/test_cascade.py |
| Monte Carlo intervals | uncertainty/monte_carlo.py | tests/test_uncertainty.py |
| Recovery/TTR | recovery/model.py | tests/test_recovery.py |
| Independent analyst reliability | validation/inter_rater.py | tests/test_validation.py |
| Historical backtesting | validation/backtest.py and data/backtests/catalog.json | leakage test and protocol |
| Sensitivity analysis | validation/sensitivity.py | tests/test_sensitivity.py |
| Double-counting defence | quality.py and validation/double_count.py | tests/test_quality.py |
| Scenario integration | service/orchestrator.py | tests/test_orchestrator.py |
| API and database | api/, persistence/, migrations/ | API and persistence tests |
| Reproducible deployment | Dockerfile, Compose, Kubernetes, run schema | CI wheel and deployment docs |
| Static/security analysis | CI and CodeQL workflows | GitHub Actions |

This table proves code and test coverage of architecture requirements. It does
not prove empirical accuracy of an uncalibrated deployment; that requires the
held-out protocol in validation.md.
