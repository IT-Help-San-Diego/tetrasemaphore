# CloudFront response-headers policies

Two policies serve this distribution:

- `security-headers.json` — the default behavior (`/`): CORP `same-origin`, COEP `credentialless`. The document stays locked.
- `assets-headers.json` — the `/assets/*` behavior: CORP `cross-origin`, COEP `unsafe-none`. A public OG/coin image is *meant* to embed cross-origin; without this, iMessage/Messages/Slack link previews silently show no picture.

Both pin the same CSP `style-src` hash. **On every edit to the site `<style>` block, recompute the hash and update BOTH files**, or the pages render blank. See `verify.sh` (it fails the build on a stale hash).
