# TSNT — Tsinderhoz Strategic Network Theory

[![CI](https://github.com/Vados992/TSNT/actions/workflows/ci.yml/badge.svg)](https://github.com/Vados992/TSNT/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-reference%20implementation-147D9A.svg)](#scope-and-claims)

TSNT is a reproducible computational architecture for analysing how shocks
propagate through interconnected maritime, trade, energy, financial, cable,
military and legal/institutional networks. The architecture and TSNT-specific
implementation were proposed by **Vadym Tsinderhoz**.

The repository turns the conceptual system into a working, testable reference
engine: bitemporal data selection, multilayer graphs, structural scoring,
capacity-constrained routing, input-output allocation, cascade propagation,
Monte Carlo uncertainty, recovery, provenance, quality gates and backtesting.

## Capabilities

- valid-time plus transaction-time graph snapshots that block look-ahead;
- SNII with exact decimal weights and deterministic ranking;
- max-flow and min-cost linear programs with parallel-edge identity;
- productive-system checks for Leontief input-output calculations;
- supply-constrained sector allocation under capacity and import limits;
- bounded cross-layer cascades with convergence diagnostics;
- seeded Monte Carlo P10/P50/P90 and exceedance probabilities;
- recovery time and cumulative service-loss calculations;
- one-at-a-time sensitivity analysis with dimensionless local elasticities;
- MAE, RMSE, sMAPE, pinball loss, coverage and Brier score;
- ICC(2,k), Kendall W, correlation/VIF and duplicate-flow controls;
- FastAPI, CLI, PostgreSQL schema, Docker and Kubernetes deployment;
- synthetic fixtures and tests that make arithmetic reproducible.

## Quick start

~~~bash
git clone https://github.com/Vados992/TSNT.git
cd TSNT
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
tsnt demo
uvicorn tsnt.api.app:create_app --factory --reload
~~~

Or:

~~~bash
cp .env.example .env
docker compose up --build
~~~

API: http://localhost:8000 · OpenAPI: http://localhost:8000/docs

## Architecture

~~~mermaid
flowchart TD
    A["Authorised sources"] --> B["Ingestion + provenance"]
    B --> C["Bitemporal multilayer graph"]
    C --> D["Flow + IO + cascade models"]
    D --> E["Monte Carlo + recovery"]
    E --> F["Validation + audit manifest"]
    F --> G["API / analyst review"]
~~~

The canonical result keeps unlike concepts separate:

~~~text
O[i,t,s] = [
  SNII, Hazard, DeltaFlow, DeltaCost, DeltaTime, DeltaOutput,
  CascadeDepth, TTR, ControlVector(P,L,F), Confidence
]
~~~

SNII is structural importance. Hazard is a time-specific analytical overlay.
Scenario values are conditional outputs, not probabilities of conflict.

## Repository map

~~~text
src/tsnt/
  api/              HTTP contracts and endpoints
  cascade/          dependency propagation
  data/             lineage, catalog, units and quality gates
  economics/        Leontief and constrained IO
  graph/            bitemporal multilayer graph
  ingestion/        adapters and protected connector seams
  optimization/     max-flow and min-cost LPs
  persistence/      SQLAlchemy version store
  recovery/         service curves and TTR
  scoring/          SNII
  service/          scenario orchestration
  uncertainty/      Monte Carlo
  validation/       backtests and reliability
~~~

## Scope and claims

This is a **working reference implementation**, not a bundled global
intelligence database and not proof that any specific forecast is true.
Operational deployment requires licensed or authorised feeds, source-specific
calibration, protected infrastructure, independent analysts and prospective
validation.

All bundled numerical fixtures are explicitly synthetic. They exercise the
engine but do not estimate a real chokepoint, state, company, conflict or person.
External connectors fail closed until a deployment provides credentials and a
reviewed licensed client.

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Data model](docs/data-model.md)
- [Validation and historical test protocol](docs/validation.md)
- [Requirements traceability](docs/traceability.md)
- [Model-card template](docs/model-card-template.md)
- [Source registry](docs/source-registry.md)
- [API](docs/api.md)
- [Deployment](docs/deployment.md)
- [Governance](docs/governance.md)
- [Roadmap](docs/roadmap.md)
- [Краткое описание на русском](docs/README.ru.md)

## Authorship and licence

TSNT architecture and TSNT-specific implementation: **Vadym Tsinderhoz, 2026**.
See [LICENSE](LICENSE), [NOTICE](NOTICE), [SECURITY.md](SECURITY.md) and
[CITATION.cff](CITATION.cff).
