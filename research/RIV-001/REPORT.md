# RIV-001 — Correlated evidence and verifier abstention

**Status:** exploratory technical report, 2026-11-23. Not peer-reviewed. Human owner review pending.

## Abstract
We exhaustively enumerate a 16-state binary observation model in which two reports share one fault domain and a third report belongs to a distinct, potentially unavailable domain. In 12 states with at most one faulty domain, requiring agreement across both available domains removes false accepts (0/6 true failures) compared with majority voting (2/6), but makes decisions in only 2/12 states. Unanimity makes decisions in 8/12 states and falsely accepts 1/6 true failures. When both domains flip and are available, cross-domain agreement is wrong. The study illustrates a conditional reliability/coverage trade-off, not a novel consensus theorem, measured agent performance, or a security guarantee.

## Reproduction
The protocol was committed before enumeration: 73a3711e55375e0fab84af1637b2f7b5b83b2218.
Run from this directory with Node.js:

    node experiment.js > reproduced.json
    diff -u results.json reproduced.json

The JavaScript enumerator was executed in a JavaScript tool runtime; all seven assertions passed. Node-specific execution and independent replication are not yet verified. Raw results include every state and decision. No paid services or external datasets were used.

## Results — primary 12 states
| Method | False accepts / true failures | Decisions / states | Wrong / decisions |
| --- | --- | --- | --- |
| First report | 2/6 | 12/12 | 4/12 |
| Report majority | 2/6 | 12/12 | 4/12 |
| Report unanimity | 1/6 | 8/12 | 2/8 |
| Domain agreement | 0/6 | 2/12 | 0/2 |
| Always abstain | 0/6 | 0/12 | undefined |

All four hypotheses held under the stated model. With complete evidence (six primary states), unanimity and domain agreement yield identical decisions (2/6 coverage, zero errors). With missing B, domain agreement abstains in all six states; unanimity accepts an A-only observation, including one false acceptance. In the four two-fault stress states, domain agreement decides twice, both incorrectly; false accepts = 1/2 true failures. The all-abstain baseline makes explicit why false accepts alone are insufficient.

## Adversarial review
- State weights are uniform by construction. Missing B has two latent fault values even though its report is absent; these are distinct latent states, not independent samples. Do not estimate operational probabilities from these ratios.
- The two A reports are identical by design; this model deliberately disadvantages report counting when A is wrong. Domain identity is assumed known and trusted. Real observers may share infrastructure, prompts, credentials, or upstream data even when labels differ.
- Results are not head-to-head comparisons with existing frameworks or OpenActionProof. The mechanism is elementary corroboration under a bounded fault model. No novelty, external validation, or real-world superiority claim is warranted.
- Hypotheses are consequences of the model, not unexpected empirical discoveries. The value of this artifact is a reproducible executable specification and explicit negative controls.
- The next experiment should distinguish real trust domains, include asymmetric and non-identical faults, vary missingness, and measure utility/coverage with an independent fixture designer. Evaluate existing verifier implementations using held-out cases.

## Owner defense checklist
Explain the truth oracle, why duplicate reports are not independent, the one-fault assumption, abstention versus error, why all-abstain is a useful control, and why results cannot be generalized to deployed agents. Re-run the script and verify all rows before claiming personal authorship or submitting externally.

## Disclosure
This protocol, implementation and report were AI-assisted using ChatGPT. No external institution, author endorsement, review, or scientific publication is claimed. Related work and links are in protocol.md.
