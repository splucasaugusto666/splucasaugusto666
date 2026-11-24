# RIV-004 — Matched SQLite verifier comparison

Status: actual pinned implementation comparison completed on a public GitHub runner; independent replication pending. AI-assisted, not peer-reviewed.

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
Use fresh trusted checkouts, review code first, no credentials or network access during verdict execution. The harness checks clean Git trees, commit identity and relevant source blobs. Local environment DNS blocked GitHub clone during fixture validation; the subsequent GitHub Actions run succeeded as documented below. No aggregate competitive score yet.

## Remote execution checkpoint
A read-only public GitHub Actions reproduction workflow was proposed in [PR #1](https://github.com/splucasaugusto666/splucasaugusto666/pull/1), head a724595b4dd6f979cbe5508d96448c08587cf567. At the first check no PR workflow run was returned; subsequent verification is recorded below.


## Actual comparison — observed 2026-11-24 UTC (2026-11-23 Brazil)
[GitHub Actions run 45315497602](https://github.com/splucasaugusto666/splucasaugusto666/actions/runs/45315497602), job 138181239405: completed successfully on Ubuntu 26.04.1. The logs confirm exact pinned source checkout and successful harness execution. Full JSON extracted from the job log is in [results.json](results.json). The runner reported SHA-256 4e8e8fddbc1258e881d5d32903643f6b111ba80d7098e88f4b644313bac12456 for its original comparison.json. A separate JavaScript calculation checked all 36 labels and 27 confusion-count/ratio fields (63 checks); all matched. This is an audit of recorded metrics, not an independent execution.

| Configuration | TP | TN | FP | FN | Abstentions | False accepts / 10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenActionProof scoped verifier | 2 | 7 | 3 | 0 | 0 | 30% |
| Verieffect exact SQLite rows with caller precondition | 2 | 7 | 3 | 0 | 0 | 30% |
| Verieffect target-only SQLite probe | 2 | 2 | 8 | 0 | 0 | 80% |

Both exact configurations accept the two valid histories, reject all seven remaining invalid histories, and accept the three invalid cases collateral_reset, duplicate_reset, outside_scope. They reject precondition_mismatch without invoking the actor. Both accept lost_ack because the correct write committed before an exception. Therefore H1–H4 held in this run. The 50 percentage point gap to the weaker target-only configuration reflects the contract and available evidence, not a demonstrated product advantage. The matched exact configurations tie on all measured decisions.

## Implications and limits
A trusted revision vector is useful against ordinary transient writes but does not survive a malicious reset of that vector. A verifier scoped to one table does not see effects outside it. These are modeled violations of assumptions or intentionally broader contracts, not undisclosed security vulnerabilities. Verieffect's cryptographic receipt chain and OpenActionProof's separate public-key integration were not compared. No comparable latency, memory, adoption, live-agent, independent held-out, or cross-platform claim; the safety, acceptance and coverage results alone cannot establish an aggregate APEX score.

Next experiment: separate a trusted transaction gate that restricts the write API from after-the-fact verification. Compare matched histories with and without enforcement; distinguish prevented actions from detected violations and include controls for a compromised gate or out-of-band writes. Freeze the protocol before execution, then extend with independently authored realistic tasks.
