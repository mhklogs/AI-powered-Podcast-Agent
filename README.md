# AI-Powered Podcast Agent

Generate a full podcast episode from a script topic — powered by **LangGraph + Gemini**, with a web UI.

## What it does

- Takes a topic/script and produces a natural-sounding podcast episode
- Orchestration graph built with **LangGraph** and **Gemini 1.5-Pro / Vertex AI**
- Web frontend served from `templates/`; deployable on Vercel via the FastAPI-style serverless entry (`vercel.json`)

## Files

```
langgraph_gemini_podcast_vertexai.ipynb  # end-to-end runbook (LangGraph + Vertex)
main.py                                  # server + episode generation
templates/                               # web UI
requirements.txt                         # deps
vercel.json                              # Vercel serverless config
```

## Run locally

```bash
pip install -r requirements.txt
python main.py            # serves the podcast UI
```

## Environment

- `GOOGLE_APPLICATION_CREDENTIALS` / `GEMINI_API_KEY` — for Gemini backend

## Deploy

```bash
vercel deploy --prod
```