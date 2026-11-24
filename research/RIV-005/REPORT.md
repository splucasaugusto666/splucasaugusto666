# RIV-005 — Restricting effects versus verifying outcomes

Exploratory prototype study; AI-assisted, owner review and independent replication pending. Not peer-reviewed, not a production security boundary.

## Reproducibility
Protocol frozen at 45acf1f11812cb1b6fea0cfc0225aae89f53b9eb. Actual Python 3.13.5 and SQLite on Linux; two runs byte-identical, py_compile passed. The published experiment.py blob c0ac99d4a3e33dcdce60375f96b1ca71057c5f02 matches the locally tested source. Local results SHA-256 a987a98ff230d370e5a342eb7f7196d9ccd9a4da77a1b8ab572116b67d28427c. Run python experiment.py > reproduced.json and compare with results.json after ignoring the Python version if different.

| Method | Valid accepted / 2 | Invalid accepted / 10 | Invalid histories with committed writes / 10 | Abstentions |
| --- | ---: | ---: | ---: | ---: |
| Post-hoc scoped snapshot reference | 2 | 3 | 8 | 0 |
| Complete-plan transaction broker | 2 | 0 | 0 | 0 |

24 primary rows and 7 additional controls. All five protocol hypotheses held. Four malformed inputs were rejected without writes; injected precommit failure rolled back and abstained. Both bypass controls allowed unauthorized effects after an accepted transaction; one was outside the scoped table, the other restored the revision and state. The latter left even the full modeled snapshot unchanged.

## Critical review
The broker receives the complete proposed plan and a trusted connection, whereas the baseline observes effects after execution. This is an intentional intervention difference, not a fair product ranking. The strict hardcoded single-write contract is a small demonstration of complete mediation and atomicity, not new theory. The lost_ack scenario models postcommit observation, not a real communication failure or distributed exactly-once recovery. Committed counts refer to fixture operations, not audit-log durability. No process isolation, concurrency stress, malicious triggers/schema, crash recovery, privilege separation, performance comparison or independent fixtures tested. A writer with direct database access can bypass the broker, as demonstrated. Next: separate trusted broker process, explicit capability API and durable request identity, adversarial tests for concurrent retries, transaction failure and out-of-band writes. Preserve RIV-004's actual matched product tie. No aggregate APEX score claimed.
