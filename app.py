import json, os
from pathlib import Path
from datetime import datetime, timezone
from ai_content import generate_content
from video_builder import build_video

TOPICS = Path("data/topics.txt")
HISTORY = Path("data/posts.json")
OUT = Path(os.getenv("OUTPUT_DIR", "output"))

def main():
    topics = [x.strip() for x in TOPICS.read_text(encoding="utf-8").splitlines() if x.strip()]
    history = json.loads(HISTORY.read_text(encoding="utf-8"))
    used = {x.get("topic") for x in history}
    topic = next((x for x in topics if x not in used), None)

    if not topic:
        print("No unused topic. Add more topics to data/topics.txt")
        return

    content = generate_content(topic)
    OUT.mkdir(exist_ok=True)
    video = OUT / "latest.mp4"
    build_video(content, video)

    meta = OUT / "latest.json"
    meta.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")

    history.append({
        "topic": topic,
        "title": content["title"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "video": str(video),
        "status": "ready"
    })
    HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    print("READY:", video)

if __name__ == "__main__":
    main()
