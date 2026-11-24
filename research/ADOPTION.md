# APEX — Global discovery and legitimate adoption

Baseline: 2026-11-23. Preserve the technical rubric in APEX.md; this is a separate portfolio-level scorecard. Objective is useful, independently reproducible work and real adoption, not a claim of market leadership.

## Evidence and competitive signals
- AgentDojo: public evaluation environment, public benchmark tasks and a peer-reviewed paper (https://github.com/ethz-spylab/agentdojo, https://papers.nips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html). A GitHub search snapshot showed about 1k stars; approximate, not synchronized with our data.
- AgentPex: transparency note documents a 424-trace evaluation subset and limitations (https://github.com/microsoft/agentpex/blob/main/transparency-note.md).
- Verieffect: README exposes deterministic probes, receipts, limitations and a roadmap (https://github.com/bfeng1122/verieffect).
- GitHub official guidance recommends READMEs, licensing, citations, contribution guidelines and topics (https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories ; https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).
- These are observable practices, not causal proof of growth.

Authenticated repository metadata confirmed public visibility for the profile, OpenActionProof, SkillParity, FPTK and the external references. The connector did not expose star/fork/download/traffic/contributor counts in this query. Do not fill missing metrics with zero. No synchronous comparative adoption ranking possible.

## Frozen provisional weights
| Axis | Weight | Evidence gate |
| --- | ---: | --- |
| Technology | 40 | Comparable pinned technical benchmark from APEX.md, security and regression gates |
| Experience and adoption | 20 | Timed independent first-use test (10), documented setup/replication pass rate (5), comparable integration checks (5) |
| Recognition and distribution | 25 | Authentic stars/forks (5), verified downloads (5), external references (5), search visibility on fixed query set (5), active community growth (5) |
| Authority and sustainability | 15 | Independent reproduction (5), transparent methods and artifacts (4), external contributions and review (3), maintenance/governance (3) |

Define cohorts, observation windows, scoring anchors and normalization for nontechnical metrics before formal scoring. Report raw values, source and timestamp. Missing values = NA; no aggregate score if any component lacks a defensible comparable measure. Separate profile and project metrics; never add stars as unique users. Do not conflate repository growth with scientific impact.

## First adoption experiment GROWTH-001
Hypothesis: a single index and automated audit reduce the effort needed to locate and check research evidence. Implemented research/README.md and audit-results.js. Technical check: 1,392 records, 40 metric groups, 8,992 assertions; three corrupted metric controls rejected. Actual independent time-to-first-benefit, conversion, downloads and retention remain unknown. No growth claim yet.

## Next
Recruit voluntary independent replication only after explicit authorization for external outreach; prepare a reproducibility template and a reviewed versioned archive/citation file; confirm licensing and owner authorship before deposit. Measure comparable external adoption from authorized public sources, and pursue RIV-004 actual scoped/external verifier evaluation. No paid services, fake engagement, spam or external submissions.

## APEX Infinity — prospective scorecard v2 (not retroactive)

Effective for future formal cycles only; preserve the v1 rubric above and technical APEX rubric. No earlier rankings recalculated.

| Axis | Weight | Required evidence |
| --- | ---: | --- |
| Technology | 30 | Matched functionality, performance, reliability, scalability tests |
| Security and quality | 15 | Scoped adversarial and regression controls, documented trust boundaries |
| Innovation | 15 | Demonstrable user benefit over relevant prior art, original contribution review |
| Experience and adoption | 15 | Independent setup/first-use success, integrations and verified retention |
| Recognition and distribution | 15 | Dated authentic visibility, downloads, external references |
| Authority and sustainability | 10 | Independent replication, contributors, maintenance and governance |

Freeze measurement anchors, denominators, cohorts and windows before comparison. Unknown = NA; no aggregate when incomplete. Track current value, peer value, dated source, confidence, gap and action. RIV-004 is a tie on matched SQLite decisions (3/10 invalid accepted per exact configuration); RIV-005 reduces invalid acceptance to 0/10 under a different intervention (complete trusted mediation), NOT a new head-to-head product victory. External adoption remains unmeasured. Prioritize privilege separation and independent test authorship. Improve the research workflow after each iteration by identifying the highest-value action, wasted effort, negative result, regression guard and next executable step. No fake recognition, external submissions or spending.
