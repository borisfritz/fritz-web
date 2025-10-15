# fritz-web

A simple static site generator written in Python, based on the Boot.dev guided project.

It takes Markdown files from /content and static assets from /static, applies template.html, and generates a complete website. For local preview it writes to ./private; for publishing (e.g., GitHub Pages) it can write to ./docs.

Quick start

- Local preview (start a test web server):
  - WSL/Linux/macOS: bash ./main.sh
  - Then open http://localhost:8888

- Windows (PowerShell alternative):
  - ./run.ps1
  - Then open http://localhost:8888

Build for publishing

- GitHub Pages (outputs to ./docs with a base path /fritz-web/):
  - ./build.sh

Project layout

- /content: Markdown source (.md). Each page must start with a top-level heading, e.g., "# Title".
- /static: CSS, images, fonts, etc. Copied as-is to the output.
- template.html: HTML template with {{ Title }} and {{ Content }} placeholders.
- /private: Local preview output (created by ./main.sh).
- /docs: Publishable output (created by ./build.sh), suitable for GitHub Pages.

How it works

- src/main.py builds the site. Without arguments, it targets ./private and uses a base path "/".
- With a non-root base path (e.g., "/fritz-web/"), it writes to ./docs and rewrites href/src URLs to include that base path.
- main.sh runs the generator and starts a local HTTP server on port 8888 serving ./private.
- run.ps1 is the Windows/PowerShell equivalent for local preview.
- build.sh builds for GitHub Pages using a base path /fritz-web/ into ./docs.

Authoring tips

- Start each Markdown file with a single H1 ("# Page title"). The title is injected into the template.
- Use standard Markdown features; headings, lists, code blocks (``` fenced), and blockquotes are supported.
- Refer to assets with absolute-style paths (e.g., /images/pic.png). The generator will prefix them with the configured base path for published builds.

Notes & troubleshooting

- Change the port by editing the scripts (8888 → your port).
- The output folders (./private and ./docs) are re-created on each build.
- On Windows/WSL, file copy uses a safe method to avoid metadata permission issues.

PyCharm/JetBrains tips (optional)

- WSL interpreter: Add Interpreter > On WSL, pick your distro and Python 3; run bash ./main.sh.
- Windows interpreter: Use ./run.ps1 or create two run configs (one to run src/main.py, one to run the HTTP server with a working directory set to private).
