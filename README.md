# CoalitionMeter

Standalone GenLayer cooperative cost allocation from natural-language tariffs. Consensus turns a complete publisher tariff and three member requests into all seven nonempty coalition costs. The contract then records exact Shapley cost shares, budget balance and explicit coalition-instability witnesses.

This is a cost-sharing primitive. It neither selects suppliers nor schedules jobs, edits a graph, redeems certificates or executes token transfers.

## Workflow

1. Deploy with a fixed source repository.
2. Anyone calls `allocate(commit_pinned_url, sha256)`.
3. Leader and validators fetch full source bytes and independently interpret every coalition's total quote. Exact KNOWN/UNKNOWN and integer-cost agreement plus substantive full-source clause verification is required. Zero-based clause anchors resolve to exact fetched text rather than model-generated quotes.
4. A missing price produces REVIEW without allocation. Decreasing coalition totals produce INCONSISTENT with subset/superset witnesses, because this instance restricts allocation to monotone cost games.
5. For complete monotone tariffs, marginal contributions over all six joining orders produce exact sixth-unit shares. Proper coalitions whose charges exceed their standalone quote become explicit UNSTABLE witnesses. Otherwise the allocation is STABLE relative to the interpreted tariff.

An integer largest-remainder preview preserves the total with amber/cobalt/jade tie order. Rational shares remain authoritative; rounded shares have separate core checks and may lose symmetry or hide rational instability.

## Files and verification

- `contracts/coalition_meter.py`: pinned single-file GenVM contract.
- `records/`: five synthetic tariffs with additive prices, economies, unstable sharing, missing quotes and nonmonotone promotion.
- `tests/direct/`: actual direct VM execution, validator replay and independent subset-weight formula over 2,187 tables.
- `scripts/`: genuine CLI proof collection and independent receipt/state verification.
- `docs/architecture.md`: policy, storage, bounds, trust boundary and math.
- `proofs/README.md`: live deployment and scenario transactions after verification.

```sh
pip install -r requirements.txt
genvm-lint download --version v0.2.16
genvm-lint check contracts/coalition_meter.py --json
pytest tests/direct -q
npm ci
node scripts/verify-proofs.cjs
```

Dispatch **StudioNet proof** for gasless development-chain CLI deployment. The workflow creates a masked ephemeral signing account. Resumption validates existing deployed bytes and avoids redeploying when a hash is supplied.

Generic CLI/workflow/Windows test scaffolding is adapted from WorkFair. The coalition interpretation, allocation, tests, fixtures and proof checker are purpose-built. Shapley allocation is established cooperative-game mathematics, not a claim of algorithmic invention. Synthetic tariff commitments prove byte identity, not genuine commercial offers, service delivery or permission to charge anyone.
