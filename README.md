# Cape Coral Happy Hours

Every licensed restaurant and bar in Cape Coral, FL, with its happy hour where one has been found.

| Path | What it is |
|---|---|
| `index.html` | Web version (works on any phone browser; "Add to Home Screen" makes it an icon). Served free by GitHub Pages. |
| `app/` | iPhone + Android app (Expo / React Native, one codebase, plain JavaScript). |
| `data/restaurants.json` | The list. Both the web version and the apps download this file on launch, so editing it updates every phone with no app update. |
| `scripts/build_data.py` | Rebuilds `data/restaurants.json`. The researched happy hours live in the `HH` table inside it. Run: `python3 scripts/build_data.py` then copy the result to `app/restaurants.json`. |
| `scripts/state_license_extract.json` | Cape Coral rows from Florida DBPR food-service license/inspection records (public record). |
| `.github/workflows/build.yml` | Cloud build of the store apps on Expo's servers. Needs an `EXPO_TOKEN` repo secret. |

## Data format
`id, name, address, phone, category, happyHour {status, times, deals, source, confidence}, lastChecked`

- `status`: `listed` (happy hour found), `unconfirmed` (serves alcohol or might; nothing found yet), `none_expected` (counter-service, coffee, ice cream, fast food).
- `confidence`: `high` = restaurant's own site, `medium` = recent listing site or press, `low` = older or single weak source.

## Where the list came from
- Restaurants: Florida DBPR license records (seating and non-seating food service; food trucks, caterers and hotel banquet rooms left out), plus bars named on happy-hour sites that hold no food license.
- Happy hours: restaurant websites, swflhappyhour.com, discoverhappyhours.com, whereat.io, local press. Each entry names its source.

## Keeping it fresh
1. Weekly scheduled Claude task: researches `unconfirmed` places, re-checks `listed` ones, applies open GitHub issues labelled as updates, edits the `HH` table, rebuilds, commits.
2. "Suggest an update" in the app opens a pre-filled GitHub issue.

## Costs
GitHub hosting and Expo's free build tier cost nothing. Store fees: Apple Developer $99/yr, Google Play $25 once.
