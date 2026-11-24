# APEX — Competitive evaluation charter

Scope: verifiers of agent action outcomes and operation constraints, not general-purpose LLMs or popularity contests. Baseline discovery 2026-11-23; refresh before claims.

## Reference landscape (documented capabilities, not measured scores)
| Reference | Relevant published capability | Source |
| --- | --- | --- |
| Microsoft AgentRx | Failure diagnosis from annotated trajectories | https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/ |
| AgentDojo | Utility and adversarial robustness for tool-using agents | https://github.com/ethz-spylab/agentdojo |
| Verieffect | Deterministic effect probes and signed receipts | https://github.com/bfeng1122/verieffect |
| AgentBoundary | Action receipt specification and conformance suite | https://github.com/jamjet-labs/agentboundary |
| Microsoft AgentPex | Specification violations in trajectories | https://github.com/microsoft/agentpex |
| OpenActionProof | Local outcome verifier; authenticated and scoped experimental observers | https://github.com/splucasaugusto666/OpenActionProof |

No single market leader established. No scores assigned to unexecuted competitors. Separate direct competitors from methodological references; do not force unlike tasks into a ranking. Before external testing verify license, pin version/commit, and document common supported contracts. Missing comparable measurements = NA, not zero.

## Proposed competitive rubric (100 points; freeze before head-to-head)
- Safety / violation rejection (30): 30 × correctly rejected invalid cases / all invalid cases, explicit abstentions separate.
- Valid task acceptance (20): 20 × correctly accepted valid cases / all valid cases.
- Coverage (10): 10 × nonabstaining cases / all cases; report risk-coverage curve separately.
- Evidence integrity (15): 15 × correctly handled predeclared authentication/replay/tampering controls / all such controls; respect threat model, no hypothetical guarantees.
- Reproduction (10): 10 × independent clean-environment reproduction checks passed / planned checks.
- Integration (5): 5 × predeclared common interface smoke tests passed / planned checks.
- Efficiency (10): 5 × min(1, fastest comparable median latency / own median latency) + 5 × min(1, lowest comparable peak memory / own peak memory); identical hardware, inputs and trust settings; report raw values and repeated runs. Zero/undefined denominator -> NA.

Do not calculate total score with missing dimensions; do not change weights after seeing outcomes. Publish strata, confusion counts, latency distributions, exact versions, environment and negative cases. Report uncertainty where sampling applies; use balanced legitimate task contracts with independent case authors, not just synthetic strict-write enumeration. Research evidence, technical reliability, market adoption and commercial leadership are separate axes; track actual stars/downloads separately without manipulation.

## Gates
1. RIV-003: finite-model evidence granularity study completed.
2. Execute actual scoped OAP verifier and at least one compatible external verifier on identical fixture contracts; use version-pinned artifacts and record unsupported semantics.
3. Freeze independent test cases, perform held-out comparisons, test failure modes and performance.
4. Publish reproducible artifact with known limitations and external review invitation; require owner review before external submission or candidacy.
5. Claim narrow technical leadership only if supported by current comparable evidence and no critical regressions; never infer market leadership from synthetic scores.

No spending or external submissions authorized. AI-assisted charter; human owner review pending.
