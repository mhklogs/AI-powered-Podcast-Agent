# AI-Powered Podcast Agent — Delivery Roadmap (v3)

> **Provenance note.** This roadmap was produced on **2026-09-29** from the same
> static analysis as the rest of `documents/` (see `00-index.md`). Backlog items are
> derived from the functional requirements in `02-functional-requirements.md`, the
> non-functional targets in `03-non-functional-requirements.md`, and the market
> findings in `01-market-analysis.md`. Timeline targets are `[TO BE VALIDATED]`
> where they depend on future estimates rather than shipped code.

## 1. Objective & horizon

LangGraph + Gemini podcast episode generator from a script/topic. This roadmap plans the next **5–6 weeks** of incremental delivery in
lockstep with the SDLC phases and traceability rules in `07-sdlc-lifecycle.md`
(Requirements → Design → Implement → Verify → Release/Operate → Improve).

Current shipped state: `https://ai-powered-podcast-agent.vercel.app` (production), source committed, v2 documentation set complete.
The build is a `main.py` server plus `templates/` web UI behind a LangGraph
orchestration graph, with `vercel.json` for the serverless deploy and a companion
notebook (`langgraph_gemini_podcast_vertexai.ipynb`) as the end-to-end runbook.

## 2. Product backlog

Prioritised with MoSCoW. Items are phrased as outcomes (not tasks) and map to FR/NFR ids.

| ID | Item (outcome) | Source | Priority |
| --- | --- | --- | --- |
| PBI-01 | `main.py` starts and serves the episode-generation UI from a clean environment with documented inputs and expected outputs | FR-1.01, FR-4 | Must |
| PBI-02 | Generation returns output conforming to a declared schema, or fails with an explicit error — never partial or malformed episode content | FR-5 | Must |
| PBI-03 | Every generative call records model, prompt version, and token usage, so an episode's cost is attributable | FR-5 (inferred) | Must |
| PBI-04 | Missing credentials or `GOOGLE_CLOUD_PROJECT` are rejected at startup with a clear error rather than a mid-run failure | FR-8 | Must |
| PBI-05 | The topic/script input is validated and length-bounded before it reaches the graph | NFR-5.4 | Should |
| PBI-06 | A provider outage or timeout returns a typed error to the UI, with an explicit timeout and retry budget | NFR-4.1 | Should |
| PBI-07 | Per-request cost ceiling and maximum output token budget are set and observable | NFR-4.2, NFR-4.3 | Should |
| PBI-08 | Prompt-injection exposure of the LangGraph nodes is assessed and documented | NFR-4.4 | Should |
| PBI-09 | Automated tests cover the graph's routing and termination conditions | NFR-6.1 | Should |
| PBI-10 | CI runs a smoke path plus lint on every push, and the Vercel deploy stays green | NFR-6.3, NFR-6.2 | Should |
| PBI-11 | Long-running generation does not exceed the serverless execution budget, with progress surfaced to the user | operational hardening | Should |
| PBI-12 | Rate limiting on the public generation endpoint | NFR-5.5 | Could |
| PBI-13 | Latency and cold-start figures measured against NFR-1 targets, recognising model time dominates | NFR-1.1, NFR-1.5 | Won't (this horizon) |

## 3. Sprint plan

**Sprint cadence:** 1 week = 1 sprint; stand-up daily (15 min), sprint review + retrospective at the end of each sprint.

| Sprint | Goal | PBI delivered | Done/exit criteria | Phase (SDLC) |
| --- | --- | --- | --- | --- |
| Sprint 1 | Reproducible start-up from a clean environment | PBI-01, PBI-04 | `python main.py` serves the UI; missing credentials fail at startup with a clear message | Implement → Verify |
| Sprint 2 | Contract and attribute every generated episode | PBI-02, PBI-03 | declared output schema enforced; token usage retrievable for a sample run | Implement → Verify |
| Sprint 3 | Bound and validate the inputs | PBI-05, PBI-07 | oversized or malformed input rejected before the graph runs; cost budget trips below the ceiling | Verify |
| Sprint 4 | Fail safely inside a long-running generation | PBI-06, PBI-11 | simulated provider failure returns a typed error to the UI; generation stays inside the execution budget with progress shown | Verify |
| Sprint 5 | Test and pipeline the graph | PBI-09, PBI-10 | CI green on every push; a routing test fails if a node edge is removed | Verify → Release |
| Sprint 6 | Harden the graph boundary and cut a release | PBI-08, PBI-12 | injection scenarios exercised against graph nodes; release cut to `https://ai-powered-podcast-agent.vercel.app` | Release & Operate → Improve |

## 4. Ceremonies

- **Daily stand-up (15 min):** what shipped since yesterday, what's blocked, what's next — tied to the active sprint's PBI board.
- **Sprint review (30 min, end of sprint):** demo PBI outcomes against the sprint goal; update `05-use-cases.md` walkthrough where behavior changed.
- **Retrospective (30 min, end of sprint):** inspect + adapt; record one actionable improvement per sprint in git notes.
- **Backlog refinement (before sprint 1):** re-prioritise PBIs against latest market findings.

## 5. Burndown (planned)

Tracked as PBI points remaining per sprint. Planned trajectory below; the team records actuals at each sprint review. `[TO BE MEASURED]` until the first sprint completes.

| Sprint | Planned remaining points |
| --- | --- |
| Start | 13 |
| Sprint 1 | 11 |
| Sprint 2 | 9 |
| Sprint 3 | 7 |
| Sprint 4 | 5 |
| Sprint 5 | 3 |
| Sprint 6 (Done, 0) | 0 |

## 6. Rollout & deploy

- Build/deploy per `07-sdlc-lifecycle.md` §5 (release policy).
- Production: `https://ai-powered-podcast-agent.vercel.app` — Vercel serverless via `vercel.json`; `vercel deploy --prod` is the release command.
- Health: a broken build blocks the next sprint's first commit; security findings are release blockers.

## 7. Risks

| Risk | Mitigation |
| --- | --- |
| Requirements drift vs. implemented code | PBI↔FR↔use-case traceability check per change (`07-sdlc-lifecycle.md` §3) |
| Unmeasured NFRs treated as done | `[TO BE MEASURED]` targets stay visible until instrumented |
| Burndown actuals fall off plan | Over-plan cut scope in the retrospective, not mid-sprint |
| Serverless execution budget exceeded by long generations | Sprint 4 hardening; progress surfaced rather than silent timeouts |
| Category commoditized by Descript / Podcastle / Adobe Podcast / NotebookLM | Position on the LangGraph orchestration story, not price (`01-market-analysis.md` §7) |
