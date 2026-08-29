# DMEXCO 2026 — Conference Agenda + AI Schedule Builder

A single-file browser tool for browsing the DMEXCO 2026 conference agenda, letting
Claude pick sessions that match your interests, and building a personal two-day
schedule with gap analysis.

## Contents

| Path | What it is |
| --- | --- |
| `index.html` | The whole app — no build step, no dependencies |
| `dmexco-2026-conference-agenda.json` | Scraped agenda (439 sessions incl. speakers) |
| `scraper/` | Scripts that produced the JSON from the Swapcard GraphQL API |

## Running

The page fetches the JSON, so it needs to be served (a `file://` open won't work):

```bash
python3 -m http.server 8765
# open http://localhost:8765/
```

## Features

**Three views** (pills at the top):

- **All sessions** — full agenda, grouped by day, with search + day/stage/type filters.
- **AI picks** — paste your own Claude API key; the whole catalogue goes to
  `api.anthropic.com/v1/messages` in one request and Claude returns a ranked list of
  matches with a one-line reason each. The key is sent straight from your browser
  (`anthropic-dangerous-direct-browser-access`) and only stored in `localStorage` if
  you tick "remember key". Roughly $0.10–0.35 per run depending on model.
- **My schedule** — a timeline of the two conference days (23–24 Sep). Every session
  has a **+ Add to schedule** button; one session per time slot, overlaps prompt you
  to swap. Between picks it shows **`Free HH:MM–HH:MM`** gap blocks that expand to the
  still-unpicked sessions in that window. State persists in `localStorage`.

**Schedule-aware AI** — once your schedule has anything in it, the AI request also
includes your current picks and the computed free slots. Claude then avoids proposing
overlaps, aims suggestions at the open windows (each pick tagged with the slot it
fills), and favours sessions that complement rather than duplicate what you've chosen.

### API key notes

Most keys need **no** Workspace ID — a legacy `sk-ant-api03-…` key or any key created
*scoped to a workspace* carries its own workspace. Only a Personal / service-account
key that isn't workspace-scoped needs the `anthropic-workspace-id` header (the tool has
a field for it).

## Regenerating the agenda JSON

`community.dmexco.com` is a Swapcard-hosted event app. The agenda is available from the
public GraphQL endpoint with no authentication:

```bash
cd scraper
python3 paginate.py     # -> all_plannings.json   (all sessions, paginated)
python3 speakers.py     # -> speakers.json        (speakers per session, batched)
python3 build.py         # -> ../dmexco-2026-conference-agenda.json
```

Event / view IDs are hard-coded at the top of `paginate.py` and `speakers.py`.
