# Shoten

A quiet search engine for books and audiobooks.

Originally built in 2020 with Svelte 3 + Carbon + a Heroku/FastAPI backend. Ported in 2026 to a single SvelteKit app that runs entirely on Cloudflare.

## Stack

- **SvelteKit 2** + **Svelte 5** (runes)
- **Tailwind CSS v4** (CSS-first config in `src/app.css`)
- **bits-ui** primitives, **lucide-svelte** icons, **mode-watcher** for dark mode
- **Bun** for install / scripts
- **Cloudflare Pages** for hosting, with the `/api/*` routes running as Workers via `@sveltejs/adapter-cloudflare`

Search is wired to Library Genesis mirrors directly from the edge. No separate backend service.

## Develop

```sh
bun install
bun run dev          # http://localhost:5173
bun run check        # svelte-check + types
```

## Deploy to Cloudflare Pages

```sh
bun run build
bunx wrangler pages deploy .svelte-kit/cloudflare
```

Or connect the GitHub repo on Cloudflare Pages and set:

- **Build command:** `bun run build`
- **Build output:** `.svelte-kit/cloudflare`
- **Compatibility flags:** `nodejs_compat`

## Project layout

```
src/
  app.css                  Tailwind v4 + theme tokens
  app.html                 dark-mode FOUC guard
  lib/
    types.ts               shared Book / SearchResponse types
    server/libgen.ts       libgen mirror search (runs at the edge)
  routes/
    +layout.svelte         ModeWatcher
    +page.svelte           search UI
    api/search/+server.ts  JSON search endpoint
legacy/                    archived Svelte 3 / Carbon / Routify version
```

## License

CC0-1.0 — public domain.
