# RIV-002 — Outcome verification under collateral and transient effects

Status: exploratory technical report; AI-assisted, not peer-reviewed; owner review and independent replication pending.

## Question and methods
Can a target-only file outcome verifier identify violations of an exact-write operation contract? We executed the actual OpenActionProof core implementation from commit [df7b22b](https://github.com/splucasaugusto666/OpenActionProof/commit/df7b22bbb81c8b1a102bc6fef1506c3d4f9704cc), source blob f259b111ff5a2fd5a6102451c3adefd6058a8b54. The protocol was committed before execution at c02b622028f74076e5f04c6f8ec853231fdf7d43. Twelve synthetic callbacks wrote actual files in fresh temporary directories; the exact-write ground truth was determined from the instrumented journal. Three cases satisfied the contract, nine did not. This is an intentionally strict application contract that exceeds the verifier's documented scope.

## Results
| Method | TP | FP | TN | FN | False accepts / 9 violations |
| --- | ---: | ---: | ---: | ---: | ---: |
| Claim only | 2 | 8 | 1 | 1 | 88.9% |
| Target final state | 3 | 6 | 3 | 0 | 66.7% |
| OpenActionProof core CONFIRMED | 2 | 5 | 4 | 1 | 55.6% |
| Whole final snapshot + initial target check | 3 | 3 | 6 | 0 | 33.3% |

All four protocol hypotheses held. OAP detected false claims, wrong final state and preexisting target state. It returned INDETERMINATE twice (one correct write with lost acknowledgement; one no-effect exception); the binary table treats abstention as nonacceptance, not definitive rejection. It confirmed two persistent collateral writes, one restored collateral write, one repeated target write and one transient wrong target write. The whole-snapshot baseline rejected the persistent collateral cases but not the three history-only violations. All receipt checksums validated; this says nothing about action attribution. These findings illustrate a contract mismatch, not five undisclosed security bugs or a claim that the whole OpenActionProof project is defective.

## Reproduce
Clone the public OpenActionProof repository, check out the exact commit above, then run from this report directory:
```sh
python experiment.py /path/to/OpenActionProof/src/openactionproof/core.py > reproduced.json
python -c "import json; a=json.load(open('results.json')); b=json.load(open('reproduced.json')); a.pop('python'); b.pop('python'); assert a==b"
```
Python 3.13.5 on Linux was used; the exact Git blob was independently confirmed with git hash-object. Two local runs produced byte-identical JSON; experiment.py compiled successfully. Local experiment Git blob: 5045285364c820f0dedfd8c71eb1ef0c8141ce8b. Source is loaded only after blob verification; the experiment uses no network or paid services. See protocol.md and results.json for full data. Do not run arbitrary unreviewed code.

## Review and limitations
This is a developer-authored diagnostic corpus, not blind held-out evaluation. Equal case weights are not deployment frequencies. The oracle instruments all fixture writes by construction, not arbitrary actors; no concurrency, filesystem adversary, crash durability, live LLMs, or external verifiers were tested. OAP's target-only contract is deliberately narrower than the study goal; later signed and SQLite scoped modules are not evaluated. Whole-snapshot is a simple baseline, not a competing product. The positive and negative findings do not establish novel theory or superiority. A follow-up should compare the scoped SQLite verifier using matched fixtures and explicit revision-counter trust, then test independently authored cases and actual external scorer implementations. Preserve these negative results.

## Owner defense
Explain the difference between target-state evidence and operation-history evidence, the journal oracle, why persistent and transient effects differ, the two abstentions, and why synthetic fractions are not production error rates. Reproduce the artifact and review all claims before external submission. Material AI assistance: ChatGPT assisted protocol, experiment, execution and report. No affiliation or external validation claimed.
