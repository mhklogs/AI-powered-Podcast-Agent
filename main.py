import asyncio
import json
import logging
import os
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Podcast Agent")
BASE_DIR = Path(__file__).parent

STAGE_LABELS = {
    "generating_outline": "Generating Outline",
    "researching": "Researching Topic",
    "writing_script": "Writing Script",
    "critiquing": "Critiquing Draft",
    "revising": "Revising Script",
    "complete": "Complete!",
}

def _make_script(topic: str, r1: str, r2: str, r3: str = "", version: int = 1) -> str:
    """Generate demo script using the provided role names."""
    if version == 1:
        if r3:
            return (
                f"**{r1}:** Welcome everyone to 'Future Watch'! I'm your host, and today we're diving into something that's keeping a lot of people up at night — {topic}. (pauses) And I have to say, after preparing for this episode, even I'm feeling a mix of excitement and concern.\n\n"
                f"**{r2}:** (nervous laugh) Tell me about it. When I first read about {topic}, I won't lie — my stomach dropped. I kept thinking, 'Is my future going to exist in two years?' It's honestly been keeping me awake.\n\n"
                f"**{r3}:** (warm, confident tone) And that's exactly the right question to ask — but let me offer some perspective. I've been studying these transitions for years. Here's what history tells us: every major shift creates as many opportunities as it removes. (pauses) The key is understanding how to navigate it.\n\n"
                f"**{r1}:** That's reassuring. But I think our friend here has a real concern — what's on your mind?\n\n"
                f"**{r2}:** (sighs) I look at what these models can do now and I think, 'What am I bringing to the table that a machine can't?' (trails off) it's scary.\n\n"
                f"**{r3}:** (emphatically) And that fear is completely valid. But studies show teams using {topic} effectively aren't the ones who replaced people — they're the ones who upskilled them. The demand for people who bridge the gap between the tech and the business is actually growing. (exhales) I've seen this pattern play out multiple times.\n\n"
                f"**{r1}:** So the message isn't 'don't worry,' it's 'worry about the right things'?\n\n"
                f"**{r2}:** (thoughtfully) I guess the question becomes not 'will I be replaced' but 'how do I evolve'? That actually makes me feel a little better.\n\n"
                f"**{r3}:** (chuckles) Now that's the right question. And I'll tell you exactly what I'd tell my own children..."
            )
        return (
            f"**{r1}:** Welcome everyone to 'Future Watch'! Today we're diving into something that's keeping a lot of people up at night — {topic}. (pauses) Even I'm feeling a mix of excitement and concern.\n\n"
            f"**{r2}:** (nervous laugh) Tell me about it. When I first read about {topic}, I won't lie — my stomach dropped. I kept thinking, 'Is my future going to exist in two years?'\n\n"
            f"**{r1}:** That's a real concern. But here's what I've learned — every major shift creates as many opportunities as it removes. (pauses) The key is understanding how to navigate it.\n\n"
            f"**{r2}:** (sighs) I look at what these models can do now and I think, 'What am I bringing to the table that a machine can't?' (trails off) it's scary.\n\n"
            f"**{r1}:** (emphatically) And that fear is completely valid. But studies show teams using {topic} effectively aren't the ones who replaced people — they're the ones who upskilled them. The demand for people who bridge the gap is actually growing.\n\n"
            f"**{r2}:** (thoughtfully) So the question isn't 'will I be replaced' but 'how do I evolve'? That actually makes me feel a little better.\n\n"
            f"**{r1}:** (chuckles) Exactly. And that's the most important takeaway of this whole conversation."
        )

    # version 2 (revised)
    if r3:
        return (
            f"**{r1}:** Welcome back to 'Future Watch'! Today we're tackling a question I hear everywhere — {topic}. (pauses) And to help us unpack this, I've brought two people with very different perspectives. Let's jump in!\n\n"
            f"**{r2}:** (nervous exhale) Thanks for having me. So, full disclosure — when I look at what {topic} can do now, I get this knot in my stomach. I read a report that said millions of jobs could be affected... (trails off) That's terrifying, right?\n\n"
            f"**{r3}:** (calm, measured) Let me stop you right there — because that statistic gets thrown around a lot, but here's what it actually means. 'Affected' doesn't mean 'eliminated.' In fact, recent reports project that while some jobs may be displaced, even more new roles will emerge. (emphatically) The net is positive — but only if we prepare.\n\n"
            f"**{r1}:** That's a crucial distinction. So the headline isn't 'everyone's losing their job,' it's 'the job landscape is shifting'?\n\n"
            f"**{r2}:** (skeptical) Okay, but that's easy to say from where you're sitting. I've got bills to pay, and 'new roles will emerge' doesn't help me if I don't know what those roles are. (frustrated sigh) Like, what am I supposed to do?\n\n"
            f"**{r3}:** (chuckles warmly) And that frustration is completely fair. But here's the thing — the shelf life of specific technical skills has always been about 3 to 5 years. That was true before AI. The difference now is that human skills — judgment, communication, ethical reasoning — are becoming more valuable, not less. (pauses) Let me give you a concrete example...\n\n"
            f"**{r1}:** So instead of 'learn to code,' the advice is shifting to something more nuanced?\n\n"
            f"**{r2}:** (slowly, processing) So... I shouldn't be trying to compete with the AI at its own game? I should focus on what I bring as a human?\n\n"
            f"**{r3}:** (warmly) Exactly. The ones who'll thrive are the ones who can ask the right questions, understand the context, and communicate across teams. That's where the real value is. I've seen it happen in every technological shift I've studied.\n\n"
            f"**{r1}:** That's genuinely empowering. So what's the one thing you'd tell our listeners who are worried right now?\n\n"
            f"**{r2}:** (deep breath) Honestly? I came in here scared, but I'm leaving with a plan. I need to focus less on the tech and more on the problems I can solve with it.\n\n"
            f"**{r3}:** (warm laugh) And that, right there, is the most important takeaway. Well said.\n\n"
            f"**{r1}:** Thank you both for an incredible discussion. See you next time!"
        )
    return (
        f"**{r1}:** Welcome back to 'Future Watch'! Today we're tackling a question I hear everywhere — {topic}. (pauses) And to help us unpack this, I've brought someone with a very different perspective. Let's jump in!\n\n"
        f"**{r2}:** (nervous exhale) Thanks for having me. When I look at what {topic} can do now, I get this knot in my stomach. I read a report that said millions of jobs could be affected... (trails off) That's terrifying, right?\n\n"
        f"**{r1}:** (calm, measured) Let me address that — 'affected' doesn't mean 'eliminated.' Recent reports project that while some jobs may be displaced, even more new roles will emerge. (emphatically) The net is positive — but only if we prepare.\n\n"
        f"**{r2}:** (skeptical) That's easy to say, but 'new roles will emerge' doesn't help me if I don't know what those roles are. (frustrated sigh) Like, what am I supposed to do?\n\n"
        f"**{r1}:** (chuckles warmly) And that frustration is completely fair. The shelf life of specific technical skills has always been about 3 to 5 years. That was true before AI. The difference now is that human skills — judgment, communication, ethical reasoning — are becoming more valuable, not less.\n\n"
        f"**{r2}:** So... I shouldn't be trying to compete with the AI at its own game? I should focus on what I bring as a human?\n\n"
        f"**{r1}:** (warmly) Exactly. The ones who'll thrive are the ones who can ask the right questions, understand the context, and communicate across teams.\n\n"
        f"**{r2}:** (deep breath) Honestly? I came in here scared, but I'm leaving with a plan. I need to focus less on the tech and more on the problems I can solve with it.\n\n"
        f"**{r1}:** (warm laugh) And that's the most important takeaway of this whole conversation. See you next time!"
    )

class PodcastAgent:
    def __init__(self):
        self.use_vertex = False
        self.model = None
        self._init_model()

    def _init_model(self):
        project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        if project:
            try:
                from langchain_google_vertexai import ChatVertexAI
                self.model = ChatVertexAI(project=project, model="gemini-2.0-flash-001", temperature=0)
                self.use_vertex = True
                logger.info("Using Vertex AI Gemini model")
            except Exception as e:
                logger.warning(f"Vertex AI not available: {e}")

    def run_stage(self, stage: str, topic: str, data: dict, roles: list = None) -> dict:
        if self.use_vertex and self.model:
            try:
                return self._run_vertex_stage(stage, topic, data, roles)
            except Exception as e:
                logger.warning(f"Vertex stage failed, falling back: {e}")
        return self._run_demo_stage(stage, topic, data, roles)

    def _run_demo_stage(self, stage: str, topic: str, data: dict, roles: list = None) -> dict:
        time.sleep(1.2)
        if stage == "generating_outline":
            return {
                "outline": (
                    f"## Podcast: {topic}\n\n"
                    f"**Show Title:** Deep Dive: {topic}\n\n"
                    f"**1. Introduction**\n"
                    f"- Hook: Why {topic} matters right now\n"
                    f"- Brief overview of what we'll cover\n\n"
                    f"**2. The Basics**\n"
                    f"- What is {topic}?\n"
                    f"- Why is it important?\n\n"
                    f"**3. Deep Dive**\n"
                    f"- Key concepts and techniques\n"
                    f"- Recent developments and breakthroughs\n\n"
                    f"**4. Real World Impact**\n"
                    f"- Current applications\n"
                    f"- Future potential\n\n"
                    f"**5. Conclusion**\n"
                    f"- Key takeaways\n"
                    f"- Where to learn more"
                )
            }
        elif stage == "researching":
            return {
                "content": [
                    {"source": "arXiv", "title": f"Recent Advances in {topic}", "snippet": f"A comprehensive 2024 survey covering the latest developments in {topic}, including novel architectures and training methodologies that have shown significant improvements over traditional approaches."},
                    {"source": "Wikipedia", "title": f"{topic}", "snippet": f"{topic} encompasses a wide range of techniques and methodologies. The field has seen rapid growth with applications spanning multiple domains including healthcare, finance, and technology."},
                    {"source": "PubMed", "title": f"Clinical Applications of {topic}", "snippet": f"Recent clinical studies published in 2024 demonstrate the transformative potential of {topic} in medical diagnosis and treatment planning, with accuracy rates improving by over 30%."},
                ],
                "search_count": data.get("search_count", 0) + 1,
            }
        elif stage == "writing_script":
            r1 = roles[0] if roles and len(roles) > 0 else "Host"
            r2 = roles[1] if roles and len(roles) > 1 else "Guest"
            r3 = roles[2] if roles and len(roles) > 2 else ""
            return {
                "draft": _make_script(topic, r1, r2, r3, version=1),
                "revision_number": data.get("revision_number", 0) + 1,
            }
        elif stage == "critiquing":
            return {
                "critique": (
                    "## Script Critique\n\n"
                    "**Strengths:**\n"
                    "- Good energy and enthusiasm throughout\n"
                    "- Solid research citations\n"
                    "- Clear structure\n\n"
                    "**Areas for Improvement:**\n"
                    "- The opening hook could be punchier to grab attention immediately\n"
                    "- Add more specific examples and data points\n"
                    "- Make the host banter feel more natural and conversational\n"
                    "- Consider adding a surprising fact or statistic early on\n"
                    "- The conclusion could be more impactful\n\n"
                    "**Suggestions:**\n"
                    "- Start with a provocative question or surprising statistic\n"
                    "- Include at least one more research citation for credibility\n"
                    "- Add brief pauses for reflection between major topics"
                )
            }
        elif stage == "revising":
            r1 = roles[0] if roles and len(roles) > 0 else "Host"
            r2 = roles[1] if roles and len(roles) > 1 else "Guest"
            r3 = roles[2] if roles and len(roles) > 2 else ""
            return {
                "draft": _make_script(topic, r1, r2, r3, version=2),
                "revision_number": data.get("revision_number", 0) + 1,
            }
        return {}

    @staticmethod
    def _fix_roles(text: str, roles: list) -> str:
        if not roles:
            return text
        import re
        role_set = {r.lower() for r in roles}
        idx = 0

        def replacer(m):
            nonlocal idx
            label = m.group(1)
            if label.lower() in role_set:
                return m.group(0)
            replacement = roles[idx % len(roles)]
            idx += 1
            return f"**{replacement}:**"

        pattern = r'^\*\*([^*]+?):\*\*'
        lines = text.split('\n')
        fixed = []
        for line in lines:
            line = re.sub(pattern, replacer, line)
            fixed.append(line)
        return '\n'.join(fixed)

    def _run_vertex_stage(self, stage: str, topic: str, data: dict, roles: list = None) -> dict:
        from langchain_core.messages import HumanMessage, SystemMessage

        if stage == "generating_outline":
            response = self.model.invoke([
                SystemMessage(content="You are an expert podcast writer. Generate a detailed outline."),
                HumanMessage(content=f"Write a high-level outline for a 2-minute podcast about: {topic}")
            ])
            return {"outline": response.content}

        elif stage == "writing_script":
            role_line = ""
            if roles and len(roles) >= 2:
                role_line = f"CRITICAL: Use EXACTLY these speaker roles: {', '.join(roles)}. NEVER use 'Host 1', 'Host 2', or any other names. Each line MUST start with **RoleName:** where RoleName is EXACTLY one of: {', '.join(roles)}."
            prompt = f"Write a 2-minute podcast script about: {topic}. Outline: {data.get('outline', '')}. {role_line}"
            response = self.model.invoke([
                SystemMessage(content=f"You are a podcast script writer. Write an engaging script with multiple speakers. Content: {data.get('content', [])}"),
                HumanMessage(content=prompt)
            ])
            return {"draft": response.content, "revision_number": data.get("revision_number", 0) + 1}

        return self._run_demo_stage(stage, topic, data, roles)

agent = PodcastAgent()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html_path = BASE_DIR / "templates" / "index.html"
    content = html_path.read_text(encoding="utf-8")
    return HTMLResponse(content=content)

@app.get("/api/status")
async def status():
    return JSONResponse({"vertex_available": agent.use_vertex})

@app.post("/api/generate")
async def generate_podcast(request: Request):
    body = await request.json()
    topic = body.get("topic", "").strip()
    if not topic:
        return JSONResponse({"error": "Topic is required"}, status_code=400)
    roles = body.get("roles", [])

    async def event_stream():
        state = {
            "topic": topic, "outline": "", "content": [], "draft": "",
            "critique": "", "queries": [], "search_count": 0,
            "revision_number": 0, "max_searches": 3, "max_revisions": 2,
        }

        try:
            # Stage 1: Outline
            yield _sse("stage", {"stage": "generating_outline", "progress": 10})
            result = agent.run_stage("generating_outline", topic, state, roles)
            state.update(result)
            yield _sse("outline", {"outline": state["outline"]})
            await asyncio.sleep(0.2)

            # Stage 2: Research loop
            for i in range(state["max_searches"]):
                yield _sse("stage", {"stage": "researching", "progress": 20 + i * 12})
                result = agent.run_stage("researching", topic, state, roles)
                state["search_count"] = result.get("search_count", state["search_count"])
                if "content" in result:
                    state["content"] = state["content"] + list(result["content"]) if isinstance(result["content"], list) else state["content"]
                yield _sse("research", {"results": state["content"], "count": state["search_count"]})
                await asyncio.sleep(0.2)

            # Stage 3: Write script
            yield _sse("stage", {"stage": "writing_script", "progress": 60})
            result = agent.run_stage("writing_script", topic, state, roles)
            state.update(result)
            yield _sse("draft", {"draft": state["draft"]})
            await asyncio.sleep(0.2)

            # Stage 4: Critique
            yield _sse("stage", {"stage": "critiquing", "progress": 75})
            result = agent.run_stage("critiquing", topic, state, roles)
            state.update(result)
            yield _sse("critique", {"critique": state["critique"]})
            await asyncio.sleep(0.2)

            # Stage 5: Revise
            yield _sse("stage", {"stage": "revising", "progress": 90})
            result = agent.run_stage("revising", topic, state, roles)
            state.update(result)
            yield _sse("revision", {"draft": state["draft"]})
            await asyncio.sleep(0.2)

            # Complete
            yield _sse("stage", {"stage": "complete", "progress": 100})
            state["draft"] = PodcastAgent._fix_roles(state["draft"], roles)
            yield _sse("complete", {"final_draft": state["draft"]})

        except Exception as e:
            logger.exception("Generation error")
            yield _sse("error", {"message": str(e)})

    return StreamingResponse(event_stream(), media_type="text/event-stream")

def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
