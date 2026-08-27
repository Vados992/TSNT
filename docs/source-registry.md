# Source registry and access boundaries

This registry identifies appropriate starting points. It does not grant a
licence and the repository does not download these sources automatically.

| Layer | Candidate source | What it can support | Access caution |
|---|---|---|---|
| Maritime | [IMO AIS overview](https://www.imo.org/en/ourwork/safety/pages/ais.aspx) | field semantics and carriage context | AIS coverage has gaps, errors and spoofing risk; live archives are often licensed |
| Trade | [UN Comtrade](https://comtradeplus.un.org/TradeFlow) | bilateral commodity value/quantity | respect API limits, revisions, confidentiality and usage agreement |
| IO | [OECD ICIO](https://www.oecd.org/en/data/datasets/inter-country-input-output-tables.html) | internationally balanced sector linkages | tables are lagged and aggregated; record edition and price basis |
| Energy | [IEA Data and Statistics](https://www.iea.org/data-and-statistics) | balances, production, demand and prices | licensing differs by product; store dataset version |
| Finance | [BIS Data Portal](https://data.bis.org/) | aggregate banking, credit, liquidity and payments | country-level aggregates are not transaction networks |
| Cables | [ITU cable-resilience material](https://www.itu.int/en/mediacentre/backgrounders/Pages/submarine-cable-resilience.aspx) | resilience context and public aggregates | exact routes/capacity may be commercial or sensitive |
| Composite indices | [OECD/JRC handbook](https://www.oecd.org/sdd/42495745.pdf) | normalization, weighting, sensitivity and uncertainty practice | methodology guidance, not TSNT validation |
| Legal | official treaty databases, legislation and sanctions registers | feasibility constraints and effective dates | legal status changes; version by jurisdiction and timestamp |
| Military | official public aggregate releases only | high-level scenario assumptions | exclude classified, personal and targetable detail |

## Source acceptance checklist

- authority and publisher identified;
- licence permits the intended storage and derivative use;
- retrieval and effective timestamps captured;
- raw content hash retained;
- original unit, revision status and seasonal/price basis captured;
- coverage and missingness measured;
- known manipulation, survivorship and reporting biases documented;
- entity mapping reviewed by a second analyst;
- later revisions append a new transaction-time version.

Commercial feeds should be injected by deployment-specific adapters. Credentials
and raw licensed extracts must never be committed.
