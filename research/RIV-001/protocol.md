# RIV-001 — Correlated evidence and verifier abstention

Protocol v1, fixed before executing the enumerator on 2026-11-23. Exploratory finite-state mechanism study, not a model evaluation or independent replication.

## Research question
Does requiring agreement between distinct trust domains rather than counting duplicate reports reduce false confirmation under a single faulty domain? What coverage is sacrificed? This is a candidate design principle for OpenActionProof, not an evaluation of its implementation.

## Model and controls
A binary ground truth (success/failure) is observed by two reporters in domain A and one in domain B. Each domain either reports truth or flips it. Both A reporters share exactly the same observation, a deliberately extreme dependency. B can be absent. Enumerate the Cartesian product of truth, A fault, B fault, B availability (16 states, including latent B fault when absent); use only cases with at most one faulty domain for the primary analysis (12 states), and retain the 4 two-fault cases as stress controls. Equal state weighting is a design convention, not an estimate of prevalence. No live agents, probabilities, network, or external data.

## Methods
- First report: accepts/rejects using A.
- Report majority: strict majority of available reports.
- Report unanimity: all available reports agree, else abstain.
- Domain agreement: both domains must be available and agree, else abstain.
- All-abstain negative control.

## Hypotheses and criteria
H1: Domain agreement has zero false accepts under at most one faulty domain; majority has at least one. H2: Domain agreement has lower coverage than majority. H3: With both domains faulty and B available, domain agreement can falsely confirm; this falsifies any unconditional guarantee. H4: The false-accept result is not attributable solely to domain identity: unanimity matches domain agreement on the complete-evidence primary subset. Missing B is the distinguishing condition. Report all outcomes even if hypotheses fail.

## Metrics
For each stratum and method report TP, TN, FP, FN, abstain-positive, abstain-negative, coverage = decisions / all, false-accept fraction = FP / all true failures, selective error = (FP+FN)/decisions (null if no decisions). Do not claim statistical significance from enumerated states. Include full row-level outputs, deterministic code and assertions. Reproduce with Node.js, no dependencies. Human review pending.

## Related work
- Microsoft Research, The Art of Building Verifiers for Computer Use Agents: https://www.microsoft.com/en-us/research/articles/the-art-of-building-verifiers-for-computer-use-agents/
- Anthropic, Demystifying evals for AI agents: https://www.anthropic.com/research/demystifying-evals-for-ai-agents
- METR, Task-Completion Time Horizons: https://metr.org/time-horizons/
- OpenAI, Research acceleration: The jagged frontier: https://openai.com/index/research-acceleration-jagged-frontier/
- Google DeepMind, Gemini 4 Neon model card: https://deepmind.google/models/model-cards/gemini-4-neon/

These motivate evaluation rigor; none is a head-to-head baseline. The general principle of independent corroboration is established; novelty of this particular model is not asserted. Next stage: map real observer fault dependencies and compare existing verifiers using held-out scenarios.

Material AI assistance: experiment protocol and code generated with ChatGPT; owner review required before scientific submission.
