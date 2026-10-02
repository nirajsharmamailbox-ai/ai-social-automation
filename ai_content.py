import os, json, requests

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
API_KEY = os.getenv("GEMINI_API_KEY", "")

def _fallback(topic):
    return {
        "title": topic[:90],
        "script": f"{topic}. Here are three quick points you should know. First, focus on a strong opening. Second, keep every scene moving. Third, end with a clear reason to watch the next video.",
        "description": f"{topic}\n\n#shorts #reels #anime",
        "hashtags": ["#shorts", "#reels", "#anime", "#edit"]
    }

def generate_content(topic):
    if not API_KEY:
        return _fallback(topic)

    prompt = f"""Create a 30-45 second vertical short-video package about:
{topic}

Return ONLY valid JSON with:
title: string
script: string
description: string
hashtags: array of 4-8 strings

Rules:
- Hook in the first sentence.
- Simple spoken language.
- No fake facts or made-up statistics.
- Script should be suitable for a 30-45 second short.
"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    r = requests.post(
        url,
        params={"key": API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)
