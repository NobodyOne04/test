# test

A one-page website for the **FC Lokomotiv restaurant complex** (Ресторанный комплекс ФК
«Локомотив»), made in 2019 as a front-end and git practice project. The page is in Russian.

> The previous README described a different project (a Go "Work Time Management" service);
> none of that code is in this repo, so it was replaced.

## View it

Open `www/index.html` in a browser, or serve the folder:

```sh
cd www && python3 -m http.server 8000      # http://localhost:8000
```

The reservation form posts to `index.php`, which isn't in the repo, so booking doesn't work
offline. The map needs a Google Maps key.

## Page

Sections: header (`#section-head`), info, gallery (FlexSlider carousel), reservation form, and
contacts with a map.

## Layout

| Path | What |
|---|---|
| `www/index.html` | the page |
| `www/public/less/` | styles in LESS (`main.less` imports reset, font, btn, layout) |
| `www/public/css/main.css` | the compiled CSS the page loads |
| `www/public/js/main.js` | menu, slider setup, AJAX reservation form |
| `www/public/js/lib/` | jQuery FlexSlider |
| `www/public/font/`, `img/` | Exo 2 web fonts, icons, slides |
| `trunk/`, `branches/` | SVN-style copies from the exercise (unminified jQuery and Maps scripts; `img`, `js` variants) |

Decisions: [docs/adr](docs/adr/README.md).
