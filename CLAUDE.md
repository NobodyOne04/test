# test

A 2019 one-page restaurant website (FC Lokomotiv), static HTML + LESS + jQuery. Russian content.

## Commands
- View: open `www/index.html`, or `cd www && python3 -m http.server 8000`.
- Styles: edit `www/public/less/*.less`, then compile to `www/public/css/main.css`
  (`npx lessc www/public/less/main.less www/public/css/main.css`); there is no build script.
- No tests.

## Layout
- `www/`: the site (`index.html`, `public/{css,less,js,font,img}`).
- `trunk/`, `branches/{img,js}`: SVN-style folder copies from the exercise; the `css` git
  branch holds one more such copy. Not used by `www/`.
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- `www/public/css/main.css` is generated from LESS: change the LESS, then recompile.
- Large images (1-2 MB slides) are in git; don't add more big binaries.
- Archived exercise: docs or small fixes only unless asked.
