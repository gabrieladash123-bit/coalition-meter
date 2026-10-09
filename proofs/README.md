# CoalitionMeter live StudioNet proofs

Contract: `0x3895e3953bc4aB21A4d39d4d447D708D3598dB03` on gasless **StudioNet**, chain **61999**, GenLayer's development chain.

[Contract source](../contracts/coalition_meter.py) | [Successful CLI run](https://github.com/gabrieladash123-bit/coalition-meter/actions/runs/37886905559) | [Deployment manifest](deployment.json)

All six current-deployment receipts finalized with `MAJORITY_AGREE` and successful execution. The additive call includes one dissenting vote; receipts preserve dissent and idle votes. Majority agreement is not unanimity or proof of publisher truthfulness.

| Scenario | Verified outcome | Transaction |
|---|---|---|
| Deployment | Empty append-only batch history; fixed publisher repository | [deploy](https://explorer-studio.genlayer.com/tx/0xd9ca96d544cbae2d4c13fcee38ac45542ef648c0f467a9ffbf30fe8d966e0daf) |
| Additive pricing | STABLE: exact shares 6/12/18, total 36 | [additive](https://explorer-studio.genlayer.com/tx/0xe76d3319fb7db8413ae8f78cdcba876e88f37e68c186fdcdb461977b3d4c95a0) |
| Shared economies | STABLE: exact shares 6/6/6, total 18 | [shared](https://explorer-studio.genlayer.com/tx/0xffe173aff01ac3a81a4d8332d4bfa6e4ea2b7f1530423ba449f272e1a36ce37e) |
| Unstable sharing | UNSTABLE: shares 8/8/8; each pair is charged 16 against its separate total quote of 10; three six-unit excess witnesses | [unstable](https://explorer-studio.genlayer.com/tx/0x816da2c94331a8f1c7a21c2b3ec9d037f69dd288361514b8e01b17aa7382cd95) |
| Missing grand quote | REVIEW: mask 7 UNKNOWN/null; no rational shares or integer preview allocated | [missing](https://explorer-studio.genlayer.com/tx/0xf44b633b80ba46b953158796fa3f5b0ea8808717fbf57f6584c6ed05af44d336) |
| Nonmonotone promotion | INCONSISTENT: explicit grand quote 9 preserved, six subset/superset decreases exposed; no allocation | [nonmonotone](https://explorer-studio.genlayer.com/tx/0xd2e55ca9b5c50357830f7e6a9f391f7bdee9f762d9f3a9a2977522ba6e8e97cc) |

Each action has a `<label>-receipt.json`, and each allocation has a `<label>.json` state snapshot. `pool-deploy` is the generic CLI deployment label; the contract is not a liquidity pool.

Deployed source SHA-256: `df22904e0e95d614a3bbc9252fb256ae4fcb0b2e72c5728a366eeeffd760b48e`. The CLI verified exact source bytes before calls and again afterward. Fixture revision: `4fc256ccb37732417de63a559e5739d4d5b97011`. Every batch records its fetched full source, byte hash, all seven normalized decisions and exact-source clause anchors.

`node scripts/verify-proofs.cjs` independently checks six finalized receipts, execution results, votes, destinations, transaction arguments, source hashes, 35 coalition decisions, all shares, exact budget balance, integer previews and every instability/domain witness. Its subset-weight formula differs from the contract's six-permutation implementation. Twenty-seven direct tests additionally cover disagreement, malformed responses, explicit UNKNOWN normalization, changed fetched bytes, rounding that hides rational instability and all 2,187 bounded cost tables.

## Earlier runs

`rejected/` preserves failed prototype receipts, source snapshots and reasons. `previous-deployment/` preserves three accepted demonstrations under the prior source; they are excluded from the current six-receipt proof set. Earlier failures included generated-quote mutations, an overstrict derived-price anchor judgment and a malformed UNKNOWN response. The final source resolves exact fetched clause indices, expands named member lists, permits explicitly authorized arithmetic and normalizes omitted cost only for an explicit UNKNOWN. It still requires exact independent cost/decision agreement and all seven positive substantive clause judgments. No failed transaction is presented as accepted.

Synthetic tariffs demonstrate interpretation and allocation, not genuine commercial quotes, bills, actual payments, physical observations or service delivery. INCONSISTENT is a violation of the primitive's monotone-cost policy, not evidence that the promotional price is false. UNSTABLE describes the chosen Shapley allocation, not proof that no stable allocation exists.
