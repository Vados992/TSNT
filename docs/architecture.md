# Architecture

## Design objective

TSNT converts heterogeneous evidence into reproducible **conditional scenario
calculations**. It is designed to answer questions such as: which capacities
bind, which alternatives absorb a shock, how much flow/cost/time changes, which
sectors lose output, how deep an evidenced dependency cascade becomes, and how
uncertain those results are.

It does not collapse all outputs into one pseudo-probability.

## Logical components

~~~mermaid
flowchart TD
    S["Source adapters"] --> P["Provenance + unit gate"]
    P --> T["Bitemporal store"]
    T --> G["Multilayer graph snapshot"]
    G --> N["Network LP"]
    G --> I["Input-output LP"]
    G --> C["Cascade model"]
    N --> M["Monte Carlo"]
    I --> M
    C --> M
    M --> R["Recovery + output vector"]
    R --> V["Backtest + analyst review"]
~~~

### Layers

| Layer | Typical nodes | Typical edges | Primary output |
|---|---|---|---|
| Maritime | ports, canals, anchorages | vessel or cargo movements | flow, delay, rerouting cost |
| Trade | country-sector-market | commodity trade | quantity/value shortfall |
| Energy | fields, terminals, pipelines, grids | fuel and power flows | energy availability |
| Finance | country/sector aggregates, venues | exposures and payments | liquidity/exposure stress |
| Cable | landing points and aggregate regions | authorised capacity links | connectivity loss |
| Military | public aggregate capabilities | declared/logistical dependencies | scenario constraint only |
| Legal | jurisdictions and regimes | permissions, sanctions, treaties | feasible-route constraint |
| Institutional | agencies and agreements | coordination dependencies | response/recovery constraint |

Sensitive asset-level data are not required by the software contract and should
not enter a public deployment.

## Time model

Every versioned record has:

- valid time: when the fact applies in the represented world;
- transaction time: when the analytical system learned the fact.

A historical snapshot includes a record only when:

~~~text
valid_from <= as_of < valid_to (or valid_to is null)
and transaction_time <= analysis_cutoff
~~~

This separates later corrections from knowledge available at forecast time and
is the core defence against retrospective leakage.

## Scenario execution

1. Validate schema, units, source licence, checksums and canonical flow IDs.
2. Select the bitemporal snapshot.
3. Apply capacity factors to matching edge, node or layer targets.
4. Solve baseline and shocked maximum flow.
5. Route a comparable feasible quantity at minimum cost.
6. Translate shortages into sector constraints where an IO mapping exists.
7. Propagate only dependencies present in the reviewed influence matrix.
8. Sample uncertain inputs with a stored random seed.
9. calculate quantiles, recovery and the disaggregated output vector.
10. Store the request, source manifest, code version and results immutably.

## Fail-closed gates

A run is rejected on invalid intervals, unknown dimensions, duplicated edge
identifiers, duplicated canonical physical flows, infeasible optimization,
unproductive IO systems, changing Monte Carlo output schemas, non-finite values
or historical data published after the declared cutoff.

Warnings do not silently become numbers. Missing data remain missing and reduce
confidence.

## Scaling path

The in-process NetworkX graph is appropriate for transparent prototypes and
moderate snapshots. A production deployment can keep the public domain
contracts while replacing storage with PostgreSQL/Timescale, object storage and
a graph projection service. Independent scenario workers can scale horizontally
because computational functions are pure and runs carry deterministic seeds.
