# What is left (sign-ins only)

Everything else is built and checked. In order:

1. **GitHub** — sign in to github.com in Chrome (or create an empty public repo named `cape-coral-happy-hours`). Then tell Claude. Claude pushes this folder, turns on GitHub Pages (web version + privacy policy go live) and the weekly refresh starts saving.
2. **Expo** — create a free account at expo.dev, then Account settings → Access tokens → create one. In the GitHub repo: Settings → Secrets → Actions → new secret `EXPO_TOKEN`.
3. **First store build (one time, needs your Apple and Google sign-ins)** — Apple: App Store Connect → Users and Access → Integrations → create an API key and add it at expo.dev under the project's Credentials. Google: pay the $25 Play Console fee, create the app, and upload the first build by hand (Google requires the first upload to be manual).
4. Paste the text from `store/listing.md` into both store pages and submit for review.

After that nothing needs you: data updates reach phones through `data/restaurants.json`, and the weekly task maintains it.
