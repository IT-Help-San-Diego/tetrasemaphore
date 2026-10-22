# CloudFront response-headers policies

Two policies serve this distribution (`E1EMF780M9UOHH`):

- `security-headers.json` — the default behavior (`/`): CORP `same-origin`, COEP `credentialless`. The document stays locked.
- `assets-headers.json` — the `/assets/*` behavior: CORP `cross-origin`, COEP `unsafe-none`. A public OG/coin image is meant to embed cross-origin; without this, link previews in messaging clients show no picture.

Both pin the same quoted CSP `style-src` hash (`style-src 'self' 'sha256-...'`). **On every edit to the site `<style>` block, recompute the hash and update BOTH files**, or browsers reject the style sheet. `verify.sh` fails the build on any unquoted or mismatched hash.

Measured TLS posture on the distribution (`TLSv1.3_2025`): `X25519MLKEM768` (ML-KEM hybrid key exchange) offered and negotiated over TLS 1.3; TLS 1.2, TLS 1.1, and TLS 1.0 handshake attempts refused.
