import asyncio, os, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

def font(size, bold=True):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def make_slide(text, path, index):
    img = Image.new("RGB", (W, H), (18 + index*7 % 35, 18, 30 + index*11 % 50))
    d = ImageDraw.Draw(img)
    title_font = font(64)
    body_font = font(52)
    d.text((70, 90), "AI SHORT", font=title_font, fill="white")
    lines = wrap(d, text, body_font, W-140)
    y = 560
    for line in lines[:8]:
        d.text((70, y), line, font=body_font, fill="white")
        y += 75
    d.text((70, H-150), "Follow for more", font=font(42), fill="white")
    img.save(path)

def split_script(script):
    parts = [p.strip() for p in re.split(r'(?<=[.!?])\s+', script) if p.strip()]
    return parts[:8] or [script]

async def tts(text, out):
    try:
        import edge_tts
        voice = os.getenv("VOICE", "en-IN-PrabhatNeural")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out)
        return True
    except Exception:
        return False

def build_video(content, output):
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        scenes = split_script(content["script"])
        imgs = []
        for i, scene in enumerate(scenes):
            p = td / f"scene_{i:02d}.png"
            make_slide(scene, p, i)
            imgs.append(p)

        concat = td / "concat.txt"
        duration = 4.0
        concat.write_text("\n".join([f"file '{p}'\nduration {duration}" for p in imgs] + [f"file '{imgs[-1]}'"]), encoding="utf-8")

        silent = td / "silent.mp4"
        subprocess.run([
            "ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),
            "-vf","scale=1080:1920,format=yuv420p",
            "-r","30","-pix_fmt","yuv420p",str(silent)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        audio = td / "voice.mp3"
        voice_ok = asyncio.run(tts(content["script"], str(audio)))

        if voice_ok:
            subprocess.run([
                "ffmpeg","-y","-i",str(silent),"-i",str(audio),
                "-map","0:v:0","-map","1:a:0","-shortest",
                "-c:v","copy","-c:a","aac","-b:a","128k",str(out)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            silent.replace(out)
