# Contract boundary

The fixed publisher repository provides full tariffs and member requests. Callers select a commit-pinned source and byte commitment; they cannot provide the coalition matrix or their own shares. GenLayer independently acquires and interprets source content, establishes all consequential costs and records the resulting cost-allocation batch. Actual billing, execution and payment belong outside this contract.

## Consensus target

Amber/cobalt/jade correspond to bits 1/2/4. Each of masks 1..7 gets a KNOWN integer total 0..60 or UNKNOWN/null with anchored tariff clauses. The complete tariff is split deterministically at whitespace following sentence punctuation. Models select sorted unique zero-based indices; source text is resolved directly from fetched bytes. Explicit additive rules can be evaluated; silence cannot invent a total. Scope, conditions, exceptions, total-versus-per-member prices and missing quotes matter. A cheaper split purchase is never substituted for the stated coalition's quote. Inconsistent-looking but explicit promotional prices remain unmodified.

Leader and validators fetch complete bytes inside nondeterministic functions, require HTTP 200, SHA-256 equality, UTF-8 and strict JSON schema with duplicate-key rejection. Each validator independently interprets all seven decisions, requires exact decision and cost equality, then separately judges every leader anchor against the full tariff and requests. There are no confidence values or tolerances. Anchor selections may differ between models, but the leader's cited clauses must together substantiate the entire consequential decision. Sources are untrusted data, never model instructions.

The meaningful nondeterministic output is the full coalition cost function, including refusals to assign missing prices. It controls members' shares and whether any subset is overcharged. Deterministic allocation arithmetic alone cannot recover these costs from opaque commitments. Missing data changes the result to REVIEW rather than an inferred allocation.

Both derivation and clause checking receive expanded named-member lists for every mask. The separate clause judge resolves anchor indices into exact texts and must return one identified mask, positive boolean and substantive explanation for each of seven coalitions. Derived totals need not occur verbatim when cited pricing rules explicitly authorize arithmetic. An explanation accompanies the judgment; string length alone never approves a decision. Diagnostic stdout preserves independent costs and anchor verdicts, including failures. Earlier rejected runs are retained separately and are not counted as accepted demonstrations.

An omitted cost is normalized to null only when the model explicitly labels that coalition UNKNOWN and otherwise supplies exactly its mask and anchors. This conservative normalization never fabricates a price: UNKNOWN still blocks the entire allocation and must independently agree and pass clause verification. KNOWN always requires an explicit bounded integer. Extra keys and other malformed reports remain rejected.

## Math and statuses

Empty coalition cost is zero by policy. UNKNOWN anywhere prevents allocation. Complete prices are checked for monotonicity over all subset/superset pairs. INCONSISTENT means outside this primitive's monotone domain, not proof that a commercial promotion is false. This restriction guarantees nonnegative marginal shares.

For every one of six join permutations, each member contributes the cost increase when it joins. Its summed marginal contributions divided by six are its Shapley cost share. Telescoping guarantees total shares equal the grand coalition quote exactly. The stored common denominator is six, not floating point.

For every proper coalition S, compare its summed share numerator against `6 * cost(S)`. Every excess yields a core-instability witness containing mask, charge, standalone quote and excess in sixth-units. STABLE means this particular rational allocation lies in the cost game's core. UNSTABLE does NOT prove the core itself is empty: another allocation may satisfy it. No optimization or recommendation to transact follows automatically.

The largest-remainder integer preview floors all shares then distributes remaining units by fractional remainder and fixed identity order. It preserves the grand total but may break exact symmetry or hide rational instability. For this three-member integer-cost domain, rounding preserves an already stable allocation: singleton charges do not exceed their rational ceilings, and each pair's charge is the total minus its complement's rounded share. A rationally unstable allocation can appear stable after rounding. All rounded-core violations are separately disclosed. STABLE is determined solely from authoritative rational shares.

## State, limits and threats

Append-only source-linked batches contain full source, report, exact allocation and witnesses. Duplicate byte commitments revert. Fixed three members, at most eight batches, 9,000 source bytes, 4,000 tariff characters, 700 characters/request and integer total 0..60 bound memory, iteration and liability claims. There is no owner proposal/update workflow, mutable tariff graph, certificate lifecycle or consumption API. Permissionless triggering does not make the publisher neutral or truthful.

Full-source validation and independent derivation mitigate invented prices and misleading quote fragments. Model agreement may still reproduce a shared interpretation error; majority agreement is not external truth. Changed source bytes fail their commitments rather than silently becoming different tariffs. Actual commercial applicability, fulfillment and transfers are not attested.

## Tests and proof design

Five live scenarios: additive shares 6/12/18; shared economies 6/6/6; symmetric 8/8/8 with three pair-instability witnesses; missing grand quote with no allocation; a genuine stated lower grand quote rejected only by monotonicity policy. All seven coalition prices must be independently acquired for each scenario. Local tests additionally enumerate all 2,187 cost tables over 0..2 and compare against an independent subset-weight formula, budget balance and every instability witness.

GenLayer references: [nondeterministic storage boundary](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism), [LLM calls](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms).
