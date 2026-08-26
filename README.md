# TSNT — Tsinderhoz Strategic Network Theory

[![CI](https://github.com/Vados992/TSNT/actions/workflows/ci.yml/badge.svg)](https://github.com/Vados992/TSNT/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB.svg)](https://www.python.org/)
[![Status: reference implementation](https://img.shields.io/badge/status-reference%20implementation-147D9A.svg)](#maturity-and-scope)

**TSNT** is a reproducible reference implementation of the Tsinderhoz Strategic
Network Theory computational architecture proposed by **Vadym Tsinderhoz**.

It combines a bitemporal multilayer graph, structural node scoring, physical
flow optimization, supply-constrained input-output analysis, verified
cross-layer cascades, Monte Carlo uncertainty, recovery modelling, provenance,
quality gates and historical backtesting.

## What this repository can do

- reproduce the published 15-node SNII baseline and rounding rules;
- represent time-versioned maritime, trade, energy, financial, cable, military
  and legal/institutional layers;
- solve capacity-constrained maximum-flow and minimum-cost routing problems;
- propagate physical shortages into Leontief and supply-constrained IO models;
- simulate explicitly evidenced cascade dependencies;
- report P10/P50/P90, exceedance probabilities and deterministic run metadata;
- measure recovery time, interval coverage, forecast error and inter-rater
  reliability;
- reject runs when units, provenance, balances or duplicate-flow controls fail;
- expose the engine through FastAPI and a command-line interface;
- run locally, with Docker Compose, or on Kubernetes.

## Quick start

```bash
git clone https://github.com/Vados992/TSNT.git
cd TSNT
cp .env.example .env
docker compose up --build
```

Open:

- API: http://localhost:8000
- OpenAPI: http://localhost:8000/docs
- health: http://localhost:8000/health

Local development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
tsnt demo
uvicorn tsnt.api.app:create_app --factory --reload
```

## Repository map

```text
src/tsnt/
  api/              FastAPI routes and schemas
  cascade/          dependency propagation
  data/             provenance, catalog and quality gates
  economics/        Leontief and supply-constrained IO
  graph/            temporal multilayer graph
  ingestion/        adapter contracts and CSV implementation
  optimization/     max-flow and min-cost linear programs
  persistence/      SQLAlchemy models and repositories
  recovery/         repair/adaptation curves and TTR
  scoring/          SNII and structural ranking
  service/          scenario orchestration
  uncertainty/      Monte Carlo and quantiles
  validation/       metrics, backtests, double counting, inter-rater
```

## Maturity and scope

This repository is a **working, tested reference implementation**, not a claim
that a globally complete operational dataset is bundled. Real deployment needs
licensed AIS, trade, energy, finance, cable and other authorised data feeds,
domain validation, a protected-data environment and prospective testing.

The included demonstration graph and scenarios are explicitly synthetic. They
verify code paths and arithmetic; they are not forecasts of a real conflict or
instructions for operational targeting.

## Core output

The system keeps unlike quantities separate:

```text
O[i,t,s] = [
  SNII, Hazard, DeltaFlow, DeltaCost, DeltaTime, DeltaOutput,
  CascadeDepth, TTR, ControlVector(P,L,F), Confidence
]
```

SNII is structural importance, Hazard is a time-specific analytical overlay,
and scenario outputs are conditional model results. None is a probability of
war.

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Data model](docs/data-model.md)
- [Validation standard](docs/validation.md)
- [API guide](docs/api.md)
- [Deployment](docs/deployment.md)
- [Security](SECURITY.md)
- [Roadmap](docs/roadmap.md)

## Authorship and use

System architecture and TSNT-specific implementation: **Vadym Tsinderhoz,
2026**. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
