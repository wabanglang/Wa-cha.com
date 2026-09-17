# Wa-cha.com

Canonical deployable source for **Wa-cha!^*+ — Idea to Action**.

## Run locally

Open `index.html` directly. No install, build process, network connection, or server is required.

## Product flow

`idea → constraints → success → output → finished instruction → next action`

The interface includes watch (`φ`), mobile (`Ψ`), and desktop (`Ω`) preview modes; keyboard and touch controls; reduced-motion support; local-only draft persistence; and offline operation.

## Deploy

The repository is ready for zero-build static hosting. `netlify.toml` publishes the repository root and applies baseline security headers.

## Verification

Before promoting a commit, verify:

- the complete workflow produces a finished instruction, next action, and completion check;
- the page opens from a fresh clone with networking disabled;
- watch, mobile, and desktop modes have no unintended horizontal overflow;
- all controls work by keyboard and touch;
- `prefers-reduced-motion: reduce` removes animation;
- the deployed production URL serves the exact promoted commit.

The public protocol and research framing remain in [`WA-CHA-PROTOCOL.md`](WA-CHA-PROTOCOL.md).
