# Methodology

## 1. Structural score

For node i, the structural-network importance index is:

~~~text
SNII_i = 0.25 C_i + 0.25 T_i + 0.20 K_i + 0.20 D_i + 0.10 S_i
~~~

where C is centrality, T throughput, K control, D cascade relevance and S the
coded lack of substitutability. Each component is bounded to [0,10]. The engine
uses decimal arithmetic and rounds only for publication. Exact values determine
rank order; deterministic secondary keys resolve true ties.

Weights are assumptions, not natural constants. A release must publish their
rationale, analyst reliability, sensitivity intervals and correlations. The
composite score must never be added to physical loss or interpreted as an event
probability.

## 2. Capacity-constrained routing

For directed edge e with capacity u_e and unit cost c_e, max-flow solves:

~~~text
maximize F
subject to 0 <= f_e <= u_e
           sum_out(v) f_e - sum_in(v) f_e = 0       for intermediate v
           sum_out(s) f_e - sum_in(s) f_e = F
           sum_in(t) f_e - sum_out(t) f_e = F
~~~

Min-cost routing fixes a feasible quantity Q and minimizes
sum_e(c_e f_e). Every parallel edge is a distinct variable. Capacity is never
inferred from centrality.

Reported network effects are:

~~~text
DeltaFlow = Flow_shock - Flow_baseline
DeltaCost = Cost_shock(Q*) - Cost_baseline(Q*)
DeltaTime = Time_shock(Q*) - Time_baseline(Q*)
Q* = min(maxFlow_baseline, maxFlow_shock)
~~~

Using Q* separates lost throughput from the cost of rerouting the throughput
that remains feasible.

## 3. Input-output accounting

The unconstrained Leontief model is:

~~~text
x = A x + f
x = (I - A)^(-1) f
~~~

The engine requires non-negative inputs, spectral radius rho(A) < 1 and an
acceptable condition number. This is an accounting response under fixed
coefficients, not a general-equilibrium forecast.

The supply-constrained model maximizes priority-weighted delivered final demand
y with:

~~~text
A x + y <= x + m
0 <= x <= capacity
0 <= y <= final_demand
~~~

where m is the reviewed net-import/resource vector. Prices, inventory,
substitution and behavioural response need explicit extensions; they are not
implicitly invented.

## 4. Cascades

With initial disruption s and reviewed influence matrix B:

~~~text
z(k+1) = clip(s + B z(k), 0, 1)
~~~

The engine reports convergence, spectral radius, affected indices and the last
step at which a new node crosses the threshold. A coefficient is admitted only
with a defined direction, unit/scale, source and calibration record.
Correlations alone do not establish a causal edge.

## 5. Uncertainty

A seeded Monte Carlo run samples a declared joint input distribution and
re-evaluates the deterministic model. Outputs include mean, standard deviation,
minimum, P10, P50, P90, maximum and optional exceedance probability.

Correlated inputs must be sampled jointly. Running independent marginal samples
for dependent capacities creates false precision. The run manifest stores the
seed, sample count, distribution version and code commit.

## 6. Recovery

For a piecewise-linear service curve q(t), cumulative service loss is:

~~~text
LossArea = integral [1 - q(t)] dt
~~~

TTR(theta,w) is the first threshold crossing at which service stays above theta
for a sustained window w. Reporting both TTR and deficit area distinguishes a
fast partial recovery from a slow full restoration.

## 7. Confidence

Confidence is separate from effect magnitude. The reference orchestrator uses
the weakest evidence-class score on active edges as a conservative placeholder.
A production calibration must estimate confidence from completeness, source
agreement, freshness, validation coverage and analyst reliability. It must not
be described as a frequentist probability unless it is calibrated as one.

## 8. Sensitivity and double counting

Every consequential run should vary weights, capacities, substitution,
elasticities, thresholds and recovery parameters. Report rank stability and
partial effects. Canonical flow identifiers block the same physical movement
from entering more than once; correlation and VIF diagnostics flag redundant
indicators but do not automatically decide which measure is substantively
correct.
