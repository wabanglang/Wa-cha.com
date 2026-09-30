# Release-readiness evidence — 2026-09-30 UTC

## Measured

- Fresh clone of main was commit 90a4a9a2116d357d60fb9d5c74cd989654f88f91; its index.html checksum matched SHA256SUMS.txt.
- Live https://wa-cha.com/ redirected to https://www.wa-cha.com/ and returned HTTP 200. HTML SHA-256 was 07c13ecdf114da2778ddce5d3ac78ecb8ffcce2c25e23176236c9e40405191e8, different from the pinned source's 8f6505368e07d9b5466c53d2ec1a3f5775235185b80b3c07f5f9184c05a3dc75. No deployment-success claim follows.
- Live CSP and Referrer-Policy differed from netlify.toml. Live Permissions-Policy also differed by additional denied capabilities; that difference is not evidence of weaker permissions protection.
- Visual review found Watch scrolling content passing behind the fixed progress rail. This candidate confines scrolling below the rail and updates the checksum.
- Candidate index.html SHA-256 is 1725570c5492e43fab3009cc1ce0921ccd5b3456b11935b23e6231da00f9dfd4. Eight automated checks passed using Chromium 134.0.6998.35. The six layout/input checks cover all four formats: 24 workflow traversals total.

acceptance.json identifies the base HEAD, dirty working tree, and exact tested source hash. The tested candidate changes were not yet committed when those measurements were taken. production.json compares the live response with the original pinned commit.

## Still required

Obtain Netlify site/deploy access, verify the host's deploy-to-commit mapping, stage this candidate without replacing the existing public version, then run live identity/header and workflow checks against that custom-domain deployment before promotion. The host deploy ID remains unknown. No deployment was changed by this audit.

Synthetic keyboard/touch checks and document-width checks do not certify every physical device, assistive technology, focus sequence, swipe gesture, or circular-mask visual state. These remaining manual checks and live candidate acceptance must pass before release readiness is claimed. The added CI configuration is prepared but has not yet produced a GitHub Actions result.
