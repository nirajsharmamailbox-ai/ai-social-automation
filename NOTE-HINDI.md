# FREE VERSION — Simple Note

## Ye version kya karega?
Har run par:
- ek naya topic lega
- Gemini se title + script + description + hashtags banayega
- script ko short scenes mein todkar 9:16 video banayega
- optional AI voice add karega
- final MP4 ready karega

## Kya free hai?
- Gemini ke supported Free Tier models se text generation free quota mein ho sakti hai.
- GitHub Actions public repository mein standard runners ke liye free hai.
- FFmpeg/Python open-source hain.

## Kya abhi automatic nahi hai?
YouTube aur Instagram par direct auto-publish ko is version mein ON nahi kiya gaya hai. Isse pehle official authorization/API setup chahiye. Is version ka goal pehle zero-cost content machine ko working banana hai.

## Phone se kaise use karna hai?
Best route:
1. GitHub account banao/login karo.
2. Is project ko public repository mein upload karo.
3. GitHub Settings > Secrets and variables > Actions mein `GEMINI_API_KEY` add karo.
4. Actions tab mein workflow run karo.
5. Run complete hone par `video-output` artifact download karo.
6. MP4 ko YouTube Shorts/Instagram Reel mein upload karo.

## Important
API key ko code mein mat likhna. Sirf GitHub Secret use karna.
