# Lucas Augusto — Independent AI Research

**Research focus: Reliable, Interoperable & Verifiable AI Systems**

I develop open-source research prototypes and reproducible experiments on the reliability of AI-assisted systems, interoperability of agent infrastructure, and deterministic validation of structured data.

| Project | Research question | Current maturity |
| --- | --- | --- |
| [OpenActionProof](https://github.com/splucasaugusto666/OpenActionProof) | How can an observer distinguish a claimed action from verified outcomes, including partial failure and missing attribution? | Research preview; controlled local experiments |
| [SkillParity](https://github.com/splucasaugusto666/skillparity) | How can file-level drift across agent skill catalogs be detected reproducibly? | Released CLI; file parity is not semantic equivalence |
| [Fitness Programming Toolkit](https://github.com/splucasaugusto666/fitness-programming-toolkit) | How can structured domain data be validated and exported deterministically in AI-assisted workflows? | Alpha; structural validation, not clinical or exercise advice |


**Start here:** [Research artifact index and one-command results audit](research/README.md) · [Global adoption and authority scorecard](research/ADOPTION.md).

The research investigates AI agent reliability, outcome verification, evidence integrity, and cross-agent interoperability. Each study exposes its protocol, executable code, recorded data, limitations and reproduction instructions. The aggregate audit checks published metrics from raw records; it is not an independent replication or a ranking of deployed AI systems.

## Research practice

- State falsifiable hypotheses and explicit trust assumptions.
- Separate observations, claims, attribution and uncertainty.
- Publish reproducible code, baseline definitions, negative results and limitations.
- Prefer independent replication to self-reported performance.
- Disclose material AI assistance in research artifacts and review all claims before external submission.

This is an independent portfolio, not an institutional affiliation or a claim of peer-reviewed publications. External review and reproducible bug reports are welcome through each project's issue tracker.

## Research log

- [RIV-001 — Correlated evidence and verifier abstention](research/RIV-001/REPORT.md): exploratory exhaustive 16-state model with pre-execution protocol, baselines, raw results and negative controls. Not a peer-reviewed paper or a deployed-agent benchmark. Owner review pending.

- [Research opportunities and publication readiness](research/OPPORTUNITIES.md): dated routes, contribution constraints and next research gates.

- [RIV-002 — Outcome verification under collateral and transient effects](research/RIV-002/REPORT.md): actual pinned OpenActionProof file verifier, 12 controlled filesystem scenarios, three baselines, reproducible results and negative findings. Not an evaluation of later scoped modules or live agents.

- [RIV-003 — Evidence granularity and observability limits](research/RIV-003/REPORT.md): 341 histories across four trust regimes, executable model and negative controls; no external product ranking.

- [APEX competitive evaluation charter](research/APEX.md): reference landscape, fixed proposed 100-point rubric, and gates for comparable verifier evaluations.

- [RIV-004 — Matched SQLite verifier comparison](research/RIV-004/REPORT.md): actual pinned OpenActionProof and Verieffect implementations evaluated in CI; matched exact-state configurations tie (3/10 false accepts). Raw observations, reproduction commands and limitations published.

- [RIV-005 — Restricting effects versus verifying outcomes](research/RIV-005/REPORT.md): complete-plan SQLite broker prototype, 24 primary evaluations and seven controls; zero false accepts in the mediated fixture, with explicit bypass counterexamples.
