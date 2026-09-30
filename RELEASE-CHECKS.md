# Release checks

The application remains zero-build and dependency-free. Node/Playwright are development-only acceptance tools; Python 3.11+ runs the live verifier.

## Reproduce acceptance

1. Clone and check out the exact candidate commit.
2. Run `npm ci --ignore-scripts` and `npx playwright install --with-deps chromium`.
3. Run `sha256sum -c SHA256SUMS.txt` and `npm run test:release`.

The suite opens local index.html with network disabled and exercises the actual Layout Lab iframe at Watch 240×240, Phone 390×844, and Desktop 1200×750. It traverses all four output formats using synthetic keyboard and touch activation, checks output/completion criteria/next action, downloads, copy feedback, editing, horizontal document overflow, persistence, validation, motion reduction, and preview exit. Reports and screenshots are written to release-results. Synthetic Chromium results do not certify physical watches or every assistive technology/browser. Manually check focus order, all controls, swipe navigation, clipping inside the circular mask, and real device behavior before publication.

## Production gate

Keep the existing preview/public version until candidate acceptance passes. Record the host's immutable deploy ID and full commit mapping before promotion. The verifier accepts an operator-supplied deploy ID; independently confirm that mapping in the host UI/API.

Run `python tools/production-check.py --url https://www.wa-cha.com/ --commit FULL_COMMIT_SHA --deploy-id HOST_DEPLOY_ID`.

The command fetches live bytes, records redirects/status/hash/headers, and fails if the HTML or configured security headers differ from the pinned commit. A passing byte check proves the index artifact matches; it does not independently prove host metadata or the entire repository tree was deployed. Do not silently normalize a mismatch. Document any host transformation and verify it reproducibly.

Run `RELEASE_URL=https://www.wa-cha.com/ RELEASE_RESULTS_DIR=release-results/live npm run test:release` for the same workflow checks on the live custom-domain copy, then record manual results and host metadata alongside the generated report. Local acceptance alone is insufficient. GitHub Actions automatically runs source acceptance; workflow_dispatch optionally runs production verification followed by live workflow acceptance. A failed or unavailable check must remain labeled rather than becoming a release-success claim.
