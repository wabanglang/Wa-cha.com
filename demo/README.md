# WA-CHA!^*+ — Tatooine Demo v52

**Branch:** `Demo` (kept separate from `main`).

## Open the demo

Open [`demo/index.html`](./index.html) in a modern browser. Single-file offline HTML/CSS/inline SVG with no JavaScript or external assets. GitHub's source viewer does not execute the HTML; save/open the HTML or host this branch in an HTML-capable preview.

## LOG[S] → AIA

- [`logs/three_word_aia_instructions.json`](./logs/three_word_aia_instructions.json): 48 original AIA actions, each mapped to an exactly three-word inquiry label and an evidence-bound executable instruction. The three-word labels are concise derived indices, not lossless replacements for their full actions.
- [`logs/assembly_master_log_v52.md`](./logs/assembly_master_log_v52.md): v52 source verification, P.ASSEMBLY team-role results, known defects, and provenance.

## Behavioral and verification boundary

This is a CSS-only scripted visual combat demo. It features target-selection/attack state, reciprocal blaster visuals, impacts, scripted HP depletion, animated movement, and icon-only controls. It does **not** calculate true collisions, damage or mutable health. Chromium `set_content` testing previously passed at 320/390/900px regular and reduced-motion; GitHub Pages, Koder, ChatGPT embedded Preview and native iOS Safari playback are **not** verified. Mid-combat weapon lock is browser-UI CSS, not independent tamper-resistant game logic.

**Source provenance:** v52 `wa_cha_tatooine_v52_team_assembly.html`, recorded SHA-256 `34a5d659d083805cd6f49baf1c324b9019d03e27b23ed1477ff80c0b7e31573f`. The `Demo` branch is not a production promotion or deployment.
