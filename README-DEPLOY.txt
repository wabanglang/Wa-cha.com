WA-CHA.COM — PRIVATE WORKBENCH v3

READY-TO-DEPLOY CONTENTS
- index.html: the complete single-file Wa-cha application
- netlify.toml: static hosting and security-header configuration
- SHA256SUMS.txt: integrity checksum for index.html

FASTEST DEPLOYMENT
1. Unzip this folder.
2. Upload the entire unzipped folder to your static host, with index.html at the web root.
3. Point Wa-cha.com to that deployment using your host's domain controls.
4. Keep the existing private preview until the custom-domain version passes testing.

NETLIFY
Drag the unzipped folder into Netlify Deploys, or publish it as the root of a connected repository. The included netlify.toml requires no build command.

LAYOUT TESTING
Use the fixed LAYOUT LAB control in the live page to switch among:
- Watch: 240 × 240 circular viewport
- Phone: 390 × 844 viewport
- Desktop: 1200 × 750 viewport

Each view is an interactive instance of the same application—not a screenshot. Choose Exit preview to return to the natural device-responsive layout.

RUNTIME
No server, database, package installation, external font, tracker, or API key is required. Drafts and Qoin counts remain in the visitor's browser storage.

PUBLICATION SAFETY
Do not replace the current public Wa-cha.com site until the deployed custom-domain copy has passed the full idea → gaps → success → format → result workflow in all three Layout Lab views.
