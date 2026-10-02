# AI Social Automation — FREE v2

This version avoids paid video-generation APIs.

Flow:
1. Topic is taken from `data/topics.txt`
2. Gemini Free Tier creates title, script, description and hashtags
3. Python/Pillow creates 9:16 visual slides
4. FFmpeg turns the slides into an MP4
5. Optional Edge TTS creates voice narration
6. GitHub Actions can run it daily for free in a PUBLIC repository
7. The finished MP4 and metadata are saved as an Actions artifact

Important:
- This is AI-assisted short-video generation, not cinematic text-to-video.
- YouTube/Instagram automatic publishing is intentionally OFF in the free version.
  Official API publishing needs account authorization/API setup.
- Never put passwords, cookies, or session tokens in the repository.
