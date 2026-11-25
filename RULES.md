# Wah Di Word? Instagram autopilot

A scheduled run happens twice a week (Jamaica time, UTC-5) and queues posts in Buffer. 11 posts a week:

| Run | Schedules |
|---|---|
| **Tuesday 6:17pm** | Thu 8am + 7pm, Fri 8am + **7pm REEL**, Sat 8am + 7pm (6 posts) |
| **Saturday 6:17pm** | Sun 8am + **7pm REEL**, Mon 8am, Tue 8am, Wed 8am (5 posts) |

Always list Buffer's scheduled posts first and skip any slot that already has a post. Buffer's free plan holds 10 scheduled posts at once.

## How to run
1. `git clone --depth 1 https://github.com/WahDiWord/wahdiword-posts` (this repo).
2. Read `log.json` (every past post) so nothing repeats. Read `direction.md` for the owner's latest instructions. They override this file.
3. Pictures: write `weeks/<first-date>.json` (format in the `kit/make.py` header; evening ids end in `-pm`). Render: `python3 kit/make.py weeks/<first-date>.json posts/<first-date>`, then delete the .html files it leaves. Look at every picture. Text must not overlap Tilly, run off the edge, or be hard to read.
   Reels: write `weeks/reel-<date>-pm.json` (format in the `kit/reel.py` header) and run `python3 kit/reel.py weeks/reel-<date>-pm.json posts/reels/<date>-pm.mp4` (about 1 minute). Check frames at 1s, 4s, 8.5s and 11s with ffmpeg before posting. Good reel ideas: Guess di word (tiles flip to the answer), How yuh seh (English title, patwah answer flips in), a patwah lesson, a game feature. Rotate bed 1, 2, 3.
5. Commit and push the PNGs, then schedule each one in Buffer with `create_post`:
   - channel: Instagram @wahdiword, id `6b07179f8541f09ecba0326b`
   - schedulingType automatic, mode customScheduled, dueAt `YYYY-MM-DDT08:00:00-05:00`
   - pictures: metadata `{"instagram":{"type":"post","shouldShareToFeed":true}}`, image url `https://raw.githubusercontent.com/WahDiWord/wahdiword-posts/main/posts/<first-date>/<id>.png` with altText
   - reels: metadata `{"instagram":{"type":"reel","shouldShareToFeed":true}}`, assets `[{"video":{"url":"https://raw.githubusercontent.com/WahDiWord/wahdiword-posts/main/posts/reels/<date>-pm.mp4"}}]`
   - evening posts: dueAt `YYYY-MM-DDT19:00:00-05:00`
6. Add the new posts to `log.json`, commit, push.
7. Buffer's free plan holds 10 scheduled posts at once. If a post is refused for that reason, schedule what fits and finish the rest next run.

## Rules (from the owner, never break)
- No em dashes anywhere (captions, pictures, alt text).
- Family-friendly only. No cursing, nothing rude, nothing political.
- Never mention 876Homes.
- Only use skins that are in the game (files in `assets/tilly`). Never show unreleased skins.
- **Never post a Daily Word answer.** Teach words only from the Island Tour or Island Nights lists, or common greetings and sayings. Check every word with `python3 kit/check_word.py "WORD ONE" "WORD TWO"` before using it. BLOCKED means it is a Daily Word: never use it. Also never post words from the Daily Word dictionary in memory.
- Patwah spelling as the game uses it. Keep the voice warm, funny and Jamaican.
- Until the owner says the game is live: "Coming soon to Google Play" in every caption and `"footer": "Coming soon"`. After launch: "Download free on Google Play" and footer "Out now".
- A "Guess di word" post reveals its answer at the top of the next day's caption.
- Mix each week (11 posts, 2 are reels): about 3 patwah lessons, 1 "How yuh seh...", 1 "Guess di word", 1 game feature (Daily Word, streaks, Island Tour, Island Nights, Big Word Sunday, skins, challenges, friends and boards), 1 Tilly or skin spotlight, 1 fun engagement post (this or that, tag a friend, fill in the blank).
- Rotate themes and Tilly skins/poses so no two days in a row look alike.
- 6 to 10 hashtags, always #WahDiWord.

## Game facts that are safe to post
- One new patwah word every day, same word for everybody, 6 guesses.
- Island Tour: 14 parishes, starting in Westmoreland and ending in St. Elizabeth. Island Nights is the night chapter.
- Big Word Sunday: a longer word on Sundays.
- Streaks with freezes. Rare skins are earned: Fire (100-day streak), Diamond (365-day streak), Galaxy (finish all 14 parishes), Lava (50 Big Word Sundays), Island King (#1 on the weekly board).
- Tilly is the mascot, a tile with lots of skins and poses.
