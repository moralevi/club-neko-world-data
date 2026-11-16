# club-neko-world-data

Data files the **Club Neko — Neko District** VRChat world downloads at runtime.
Served from `raw.githubusercontent.com`, which VRChat String Loading trusts.

| File | Written by | Read by |
|---|---|---|
| `access.json` | Club Neko bot (role sync) | `NekoAccess` |
| `events.json` | Staff (manual), Phase 1 | Plaza event board |
| `leaderboard.json` | Bot (`/submit`), Phase 5 | Plaza leaderboard wall |
| `gallery.json` + images | Staff (manual), Phase 6 | Art Loft gallery |

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

## Checks

`.github/workflows/validate.yml` validates each file against `schemas/` on push.
