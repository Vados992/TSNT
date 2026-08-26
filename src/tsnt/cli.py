"""Command-line interface for reproducible local runs."""

import json
from datetime import UTC, datetime

import typer

from tsnt import __version__
from tsnt.domain.enums import EvidenceClass, Layer
from tsnt.domain.models import EdgeRecord
from tsnt.optimization.flow import max_flow

app = typer.Typer(no_args_is_help=True)


@app.command()
def version() -> None:
    """Print the engine version."""
    typer.echo(__version__)


@app.command()
def demo() -> None:
    """Run a small synthetic max-flow example."""
    now = datetime(2026, 1, 1, tzinfo=UTC)
    edges = [
        EdgeRecord(
            edge_id="demo-a",
            source="origin",
            target="hub",
            layer=Layer.TRADE,
            commodity="synthetic-unit",
            capacity=80,
            cost_per_unit=2,
            valid_from=now,
            transaction_time=now,
            evidence_class=EvidenceClass.SYNTHETIC,
        ),
        EdgeRecord(
            edge_id="demo-b",
            source="hub",
            target="destination",
            layer=Layer.TRADE,
            commodity="synthetic-unit",
            capacity=60,
            cost_per_unit=3,
            valid_from=now,
            transaction_time=now,
            evidence_class=EvidenceClass.SYNTHETIC,
        ),
        EdgeRecord(
            edge_id="demo-c",
            source="origin",
            target="destination",
            layer=Layer.TRADE,
            commodity="synthetic-unit",
            capacity=15,
            cost_per_unit=8,
            valid_from=now,
            transaction_time=now,
            evidence_class=EvidenceClass.SYNTHETIC,
        ),
    ]
    result = max_flow(edges, "origin", "destination")
    typer.echo(
        json.dumps(
            {
                "fixture": "synthetic",
                "total_flow": result.total_flow,
                "total_cost": result.total_cost,
                "edge_flows": result.edge_flows,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    app()
