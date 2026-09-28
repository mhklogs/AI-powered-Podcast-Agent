# AI-powered-Podcast-Agent — Architecture Summary

> Generated from static analysis on 2026-09-28.

## Components

| Layer | Present | Evidence |
| --- | --- | --- |
| Presentation / UI | no | 0 route module(s), 0 component file(s) |
| API / server | yes | 0 handler(s), entrypoints: main.py |
| Domain / business logic | yes | AI/agent orchestration detected |
| Persistence | no | no database client |
| Authentication | no | none detected |

## Detected frameworks and libraries

| Package | Purpose (inferred) |
| --- | --- |
| `fastapi` | FastAPI |
| `uvicorn` | Uvicorn |

## Runtime and delivery

| Concern | Finding |
| --- | --- |
| Language mix | Python, HTML |
| Package manager | pip |
| Container | none |
| Serverless / PaaS | Vercel configuration present |
| CI | none detected |
| Tests | **none detected** |
| Type safety | type hints |

## Environment variables referenced

- `GOOGLE_CLOUD_PROJECT`
