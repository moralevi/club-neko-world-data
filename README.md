# club-neko-world-data

Data files the **Club Neko — Neko District** VRChat world downloads at runtime.
Served from `raw.githubusercontent.com`, which VRChat String Loading trusts.

| File | Written by | Read by |
|---|---|---|
| `access.json` | Club Neko bot (role sync) | `NekoAccess` |
| `events.json` | Staff (manual), Phase 1 | Plaza event board |
| `leaderboard.json` | Bot (`/submit`), Phase 5 | Games room leaderboard wall (`NekoLeaderboard`) |
| `supporters.json` + `photos/` | Staff (manual) | Supporter wall on the front lawn (`NekoSupporterWall`) |
| `supporters.png` | GitHub Action (from `photos/`) | Supporter wall photos, via GitHub Pages |

## access.json

```json
{
  "version": 1,
  "updated": "2026-11-16T02:00:00Z",
  "staff":   ["Estrellalevi"],
  "vipPlus": [],
  "vip":     []
}
```

- Names are **VRChat display names**, matched case-insensitively.
- All five keys are required. If the file is missing a key, isn't valid JSON or
  has another `version`, the world ignores it and keeps the last good list.
- A name in several lists gets the highest rank.
- The world always treats its hard-coded owner name as Owner, whatever this file says.
- Changes reach new instances within about 5 minutes (the raw CDN cache) and
  running instances on their next 5-minute re-check, so ~10 minutes worst case.

## events.json

Shown on the plaza event board. Edit it on GitHub and the board updates within about 15 minutes
(the board re-checks every 10 minutes, plus the raw CDN cache).

```json
{
  "version": 1,
  "updated": "2026-11-16T04:00:00Z",
  "next": { "title": "Neon Night", "when": "Sat 22 Nov · 8pm GMT", "dj": "Somebody", "details": "Optional, max 160 chars" },
  "announcements": ["Up to 5 short lines"]
}
```

- `when` is shown exactly as written, so include a time zone.
- Remove `next` entirely when nothing is scheduled.

## leaderboard.json

Written by the bot after each accepted `/submit` (top 10 per stat, best first). Don't edit it by hand: the bot
rebuilds it from its own database. The world re-downloads it every 5 minutes.

```json
{
  "version": 1,
  "updated": "2026-11-16T22:00:00Z",
  "stats": {
    "pool_wins":      [{ "name": "Estrellalevi", "value": 12 }],
    "darts_best":     [],
    "bowling_best":   [],
    "airhockey_wins": []
  }
}
```

## Checks

`.github/workflows/validate.yml` validates each file against `schemas/` on push.

## supporters.json (supporter wall)

The board on the front lawn, facing the fountain. Left: a photo spotlight (8 at a time, turning every 10 seconds).
Right: names by tier. **VIP+ and VIP names from `access.json` are shown automatically**, so this file is only for
extra people, captions and photos.

```json
{
  "version": 1,
  "updated": "2026-11-17T07:00:00Z",
  "message": "Optional subtitle, max 80 chars",
  "supporters": [
    { "name": "Somebody", "tier": "vipplus", "caption": "Optional, max 40 chars", "photo": "somebody.png" },
    { "name": "Someone Else", "tier": "special", "caption": "Made the cat statues" }
  ]
}
```

- `tier` is `vipplus`, `vip`, `supporter` (the default) or `special` (shown as "Special thanks").
- Bump `updated` whenever you change the file: the world only re-downloads the photos when it changes.
- Spotlight order is file order. People in the instance right now are highlighted in gold.

### Photos

1. Put the picture in `photos/` (png, jpg or webp, any size; it is centre-cropped to a square).
2. Set that entry's `"photo"` to the file name.
3. Push. The **Build supporter photos** action rebuilds `supporters.png` (an 8 x 8 grid, one 256 px cell per
   entry with a photo, in file order; up to 64) and commits it.

VRChat only downloads images from trusted hosts and `raw.githubusercontent.com` isn't one, so the world loads
`supporters.png` from **GitHub Pages**: `https://moralevi.github.io/club-neko-world-data/supporters.png`.
Pages must be on for this repo (Settings > Pages > Deploy from a branch > `main` / root). `.nojekyll` makes Pages
serve the files as they are. Players with "Allow Untrusted URLs" off still see photos, because `*.github.io` is trusted.

Local build: `pip install pillow` then `python tools/build_supporter_photos.py`.
