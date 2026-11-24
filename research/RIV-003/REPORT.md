# RIV-003 — Evidence granularity and observability limits

Exploratory technical report. AI-assisted; owner review and independent reproduction pending. Not peer-reviewed.

## Method
Pre-execution protocol commit: 2ce80928aa48092ffb8499e77f940ef16d5fd8f2. Exhaustively enumerated 341 histories of length 0–4 over four writes to two binary resources; each history was evaluated in four evidence regimes (1,364 rows). Exactly one valid history per regime is intentionally specified. The truth oracle is exact history compliance, not merely the final state. This is a reference model, not OpenActionProof implementation or an external product benchmark.

## Results
False accepts among 340 violating histories per regime:
| Evidence regime | Target | Snapshot | Revision vector | Journal |
|---|---:|---:|---:|---:|
| Honest |154|84|0|0|
| Counters reset |154|84|84|0|
| Journal absent |154|84|0|0 (all abstain)|
| Both fabricated |154|84|84|84|

All five hypotheses held. Every method accepts the single valid history except the missing-journal policy, which abstains on all 341. Other coverage is 100%. With honest evidence, snapshot+revision and journal each score 100 under the predeclared scoring rubric, versus 87.65 snapshot and 77.35 target. When both evidence channels are fabricated, both scores fall to 87.65. Journal absence scores 0 because the rubric gives no credit to abstention (raw metrics retained); a deployment-specific cost function may prefer abstention to false accept. Scores are properties of this finite model, not rankings of commercial products.

## Identifiability
The compliant history shares its final target observation with 154 violating histories, and its full snapshot with 84. Under honest monotonic per-resource write counters, none share its revision observation. Resetting the counters restores the 84-history ambiguity. An honest complete journal distinguishes all histories, but a missing or fabricated journal cannot uniquely establish compliance. These are elementary model-specific observational equivalences, not a novel general theorem. No classifier using only the shared evidence can distinguish those specific histories perfectly.

## Reproduction
The exact experiment.js implementation ran twice in a JavaScript tool runtime; serialized results were identical. Assertions confirmed 341 unique histories, four valid observations across regimes, and all confusion-count totals. From this directory use Node.js (Node runtime itself not separately tested):
```sh
node experiment.js > reproduced.json
node -e "const fs=require('fs'); const a=JSON.parse(fs.readFileSync('results.json')); const b=JSON.parse(fs.readFileSync('reproduced.json')); if(JSON.stringify(a)!==JSON.stringify(b)) process.exit(1)"
```
Full rows in results.json. No external APIs or paid dependencies.

## Adversarial review
Only one compliant trace per regime, all fixed initial values, two resources, four possible events and no stochastic sampling. No real agent, cryptography, concurrency, storage compromise resistance or runtime performance evaluation. Equal history weights are not prevalence estimates. The journal is a perfect oracle when honest by construction; do not infer real-world superiority. Counter reset is a modeled trust failure, not a demonstrated exploit against a named product. Distinguish verification of an explicitly strict write contract from semantic task utility. Next: map this model to actual pinned verifier implementations and independent test cases, including explicit unknowns and time/overhead. Preserve negative findings. Related work includes AgentDojo (https://github.com/ethz-spylab/agentdojo) and Microsoft AgentPex (https://github.com/microsoft/agentpex); neither is a tested baseline here.
