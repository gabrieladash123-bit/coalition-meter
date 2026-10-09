# Builder -> Intelligent Contracts

Title: CoalitionMeter: Consensus tariff cost-sharing and instability witnesses

## Notes / Description

CoalitionMeter is a GenLayer cooperative cost-sharing primitive. A caller supplies a commit-pinned tariff URL and SHA-256 from a fixed publisher. Leader and validators independently fetch full clauses and three requests, deriving total costs for seven coalitions. Exact KNOWN/UNKNOWN and cost agreement plus substantive clause checks bind prices to source clauses. Complete monotone tariffs feed six joining permutations to produce exact rational Shapley shares with budget balance. Subgroups charged above their standalone quote receive instability witnesses. Missing prices return REVIEW; decreasing totals expose domain violations without allocation. Integer previews disclose separate stability checks. StudioNet proofs cover additive costs, shared economies, unstable sharing, missing quotes and a promotional price outside the monotone domain. The repo includes 27 direct tests and 2,187 bounded cost tables. Synthetic tariffs demonstrate allocation, not bills, payments or delivery.

## Evidence

- Repository: https://github.com/gabrieladash123-bit/coalition-meter
- GenLayer contract: https://github.com/gabrieladash123-bit/coalition-meter/blob/main/contracts/coalition_meter.py
- Onchain proofs: https://github.com/gabrieladash123-bit/coalition-meter/blob/main/proofs/README.md

StudioNet contract: `0x3895e3953bc4aB21A4d39d4d447D708D3598dB03`.

[Deployment transaction](https://explorer-studio.genlayer.com/tx/0xd9ca96d544cbae2d4c13fcee38ac45542ef648c0f467a9ffbf30fe8d966e0daf). Six finalized MAJORITY_AGREE receipts match recorded state. Earlier rejected receipts and the final additive dissent are preserved in the proof set.
