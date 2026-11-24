# RIV-004 — Matched SQLite verification (checkpoint)

Status: fixture validation completed; actual product comparison pending. AI-assisted, not peer-reviewed.

The pre-execution protocol is committed at 27494f30207edb748f4d6dae2157deedcf91ea3a. The benchmark harness is published at 9c6e7f7020235c5909a65c2146df28c1c1c6660c; Git blob 060f4a9558d182d671b79c0d98d8a5b0d6a33454 matches the locally tested file.

## Verified local result
Python 3.13.5 on Linux, actual SQLite database operations, fixture-reference mode only. Two runs produced identical JSON and py_compile passed. Output SHA-256: 8bacc3cda8a4cc20e16831f952119cb941f5f2ccf59840002267fa7a40de0658.
Reference: TP 2, TN 7, FP 3, FN 0, abstentions 0; three false accepts out of ten invalid histories. The accepted invalid histories were collateral_reset, duplicate_reset and outside_scope. All remaining invalid histories were rejected. This is not a product result.

## Reproduce
From this directory:
```sh
python experiment.py --fixtures-only > fixture-results.json
git clone https://github.com/splucasaugusto666/OpenActionProof.git /tmp/riv004-oap
git -C /tmp/riv004-oap checkout --detach b535850af64a460f96edfbcf56fa40df0d5ff974
git clone https://github.com/bfeng1122/verieffect.git /tmp/riv004-verieffect
git -C /tmp/riv004-verieffect checkout --detach bfb6af94984ddda87133bd76bbcce2b28d10f485
python experiment.py --oap /tmp/riv004-oap --verieffect /tmp/riv004-verieffect > comparison.json
```
Use fresh trusted checkouts, review code first, no credentials or network access during verdict execution. The harness checks clean Git trees, commit identity and relevant source blobs. Local environment DNS blocked GitHub clone; no actual competitor results claimed. Next: execute the full harness, preserve all rows, compare hypotheses and publish evidence. Do not substitute fixture metrics for actual product evaluation. No aggregate competitive score yet.
