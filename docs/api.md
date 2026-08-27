# API guide

Start the service:

~~~bash
uvicorn tsnt.api.app:create_app --factory --host 0.0.0.0 --port 8000
~~~

OpenAPI is available at /docs and /openapi.json.

## Endpoints

| Method/path | Purpose |
|---|---|
| GET /health | liveness and version |
| POST /v1/scoring/snii | exact and two-decimal structural score |
| POST /v1/flows/max | capacity-constrained maximum flow |
| POST /v1/flows/min-cost | exact-quantity minimum-cost routing |
| POST /v1/economics/leontief | productive Leontief solution |
| POST /v1/cascades/simulate | bounded cascade trajectory |
| POST /v1/scenarios/network | baseline/shock routing comparison |

All request models reject unknown fields. Analytical errors return HTTP 422
rather than a plausible-looking partial result.

## Authentication

When TSNT_API_KEY is empty, versioned endpoints are open for local development.
When it is configured, send:

~~~text
X-API-Key: <secret>
~~~

Use an identity-aware gateway and managed secret store in production. The
single-key mechanism is a deployment minimum, not a full authorization model.

## Example SNII request

~~~bash
curl -s http://localhost:8000/v1/scoring/snii \
  -H 'Content-Type: application/json' \
  -d '{
    "components": {
      "centrality": 8,
      "throughput": 7,
      "control": 6,
      "cascade": 5,
      "substitutability": 4
    }
  }'
~~~

Expected response:

~~~json
{"exact":"6.35","published":"6.35"}
~~~

Edge endpoints accept the complete EdgeRecord contract, including valid time,
transaction time, unit and evidence class. This is intentional: the API does not
silently invent temporal provenance.
