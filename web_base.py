
import os
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS


load_dotenv()

MODEL = "llama-3.3-70b-versatile"

# ── Web search keywords that trigger this file ──────────────
WEB_KEYWORDS = [
    "latest", "today", "current", "news", "now",
    "price", "stock", "weather", "recent",
    "2024", "2025", "2026", "trending", "update",
    "just released", "announced", "breaking"
]


def is_web_query(question: str) -> bool:
    """
    Returns True if the question needs real-time web info.
    Called by main chatbot to decide which mode to use.
    """
    q = question.lower()
    return any(kw in q for kw in WEB_KEYWORDS)


def search_web(query: str, max_results: int = 4) -> list[dict]:
    """
    Search DuckDuckGo and return top results as list of dicts.
    Each dict has: title, body, href
    """
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "body":  r.get("body", ""),
                    "href":  r.get("href", ""),
                })
    except Exception as e:
        print(f"Search error: {e}")
    return results


def build_context(results: list[dict]) -> str:
    """Convert search results into a readable context block."""
    if not results:
        return ""
    chunks = []
    for i, r in enumerate(results, 1):
        chunks.append(
            f"[{i}] {r['title']}\n{r['body']}\nSource: {r['href']}"
        )
    return "\n\n".join(chunks)


def web_search_answer(
    question: str,
    history: list = None,
    system_prompt: str = "You are a helpful AI assistant.",
    stream: bool = True
) -> str:
    """
    Full pipeline:
      1. DuckDuckGo searches the web
      2. Results injected into Groq prompt
      3. Groq summarizes and answers
      4. Streams response token by token

    Args:
        question     : user's question
        history      : past conversation (list of dicts)
        system_prompt: AI personality
        stream       : True = print tokens as they arrive

    Returns:
        Full response string
    """
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # ── Step 1: Search the web ────────────────────────────────
    print(f"\n🌐 Searching the web for: {question}")
    results = search_web(question)

    if not results:
        return "❌ No web results found. Try rephrasing your question."

    # ── Step 2: Build context from search results ─────────────
    context = build_context(results)

    # ── Step 3: Build system prompt with search context ───────
    rag_system_prompt = (
        f"{system_prompt}\n\n"
        "You have access to real-time web search results below. "
        "Answer the user's question using ONLY these results. "
        "Be concise, mention key facts, and cite source numbers like [1], [2].\n\n"
        f"WEB SEARCH RESULTS:\n{context}"
    )

    # ── Step 4: Build messages — history passed natively ──────
    history = history or []
    messages = (
        [{"role": "system", "content": rag_system_prompt}]
        + history[-6:]                              # last 3 turns (6 messages)
        + [{"role": "user", "content": question}]  # current question
    )

    # ── Step 5: Send to Groq ──────────────────────────────────
    response_stream = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.5,
        stream=stream,
    )

    # ── Step 6: Collect streamed tokens ───────────────────────
    full_response = ""
    if stream:
        for chunk in response_stream:
            token = chunk.choices[0].delta.content or ""
            print(token, end="", flush=True)
            full_response += token
        print()  # newline after stream ends
    else:
        full_response = response_stream.choices[0].message.content

    return full_response
