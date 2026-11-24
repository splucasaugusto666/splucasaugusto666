# Research artifacts — start here

Reliable, Interoperable & Verifiable AI Systems. Independent, AI-assisted research; no institutional affiliation, peer-review claim or external validation. The owner must review before external submission.

## Verify the evidence in one command

Clone the repository and run (Node.js 18+ recommended, no third-party packages):

```sh
git clone https://github.com/splucasaugusto666/splucasaugusto666.git
cd splucasaugusto666
node research/audit-results.js
```

Expected: PASS, 1,392 recorded rows, 40 metric groups, 8,992 assertions and three intentionally corrupted metric files rejected in memory. The audit function was executed in a JavaScript tool runtime against the actual remotely fetched JSON files on 2026-11-23. It checks counts, denominators and selected labels against recorded rows; it does not independently reproduce experimental observations, validate all fields or establish scientific originality. The Node CLI wrapper itself has not yet been run in Node.

| Study | Question | Protocol | Code | Data | Report |
| --- | --- | --- | --- | --- | --- |
| RIV-001 | Correlated observer evidence | [Protocol](RIV-001/protocol.md) | [JS](RIV-001/experiment.js) | [JSON](RIV-001/results.json) | [Report](RIV-001/REPORT.md) |
| RIV-002 | Target state vs exact-write history | [Protocol](RIV-002/protocol.md) | [Python](RIV-002/experiment.py) | [JSON](RIV-002/results.json) | [Report](RIV-002/REPORT.md) |
| RIV-003 | Observability under evidence failures | [Protocol](RIV-003/protocol.md) | [JS](RIV-003/experiment.js) | [JSON](RIV-003/results.json) | [Report](RIV-003/REPORT.md) |
| RIV-004 | Matched SQLite verifier comparison (fixture validation only; product results pending) | [Protocol](RIV-004/protocol.md) | [Python](RIV-004/experiment.py) | Pending | [Checkpoint](RIV-004/REPORT.md) |

RIV-001 and RIV-003 are finite synthetic models; RIV-002 evaluates a pinned real file verifier using controlled local writes. These are not comparable samples and must not be pooled into a performance estimate.

## Reproduce individual studies
Follow each report's exact instructions and pinned source references. Record platform, runtime, repository commit, command, expected/observed output, and deviations. Do not run unreviewed code. Submit a focused reproducibility issue in the appropriate repository only if you want to share findings; avoid private data or credentials. Report negative results as well as successful replication.

## Referencing
For a reproducible reference use study title, study ID, repository URL, exact commit and access date. These are preliminary technical artifacts, not peer-reviewed publications. No DOI or publication venue is claimed. Review authorship and licensing with the owner before archival deposit, redistribution or formal submission.

See [APEX charter](APEX.md), [adoption scorecard](ADOPTION.md) and [opportunities](OPPORTUNITIES.md).
