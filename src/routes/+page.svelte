<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { toggleMode, mode } from 'mode-watcher';
  import { Search, Sun, Moon, ChevronLeft, ChevronRight, Loader2 } from 'lucide-svelte';
  import type { SearchResponse, Book } from '$lib/types';

  let query = $state('');
  let page = $state(1);
  let results = $state<Book[]>([]);
  let hasMore = $state(false);
  let loading = $state(false);
  let touched = $state(false);
  let input: HTMLInputElement | undefined = $state();

  let lastQuery = '';
  let lastPage = 0;

  async function run(opts: { resetPage?: boolean } = {}) {
    if (!query.trim()) return;
    if (opts.resetPage) page = 1;
    if (query === lastQuery && page === lastPage) return;

    loading = true;
    touched = true;
    try {
      const url = `/api/search?q=${encodeURIComponent(query)}&page=${page}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(await res.text());
      const data: SearchResponse = await res.json();
      results = data.results;
      hasMore = data.hasMore;
      lastQuery = query;
      lastPage = page;
      history.replaceState(null, '', `?q=${encodeURIComponent(query)}${page > 1 ? `&page=${page}` : ''}`);
    } catch (err) {
      console.error(err);
      results = [];
      hasMore = false;
    } finally {
      loading = false;
    }
  }

  function openReader(book: Book) {
    const url = `https://reader.vercel.app/book?id=${book.md5}`;
    window.open(url, '_blank', 'noopener');
  }

  async function go(next: number) {
    if (next < 1 || next === page) return;
    if (next > page && !hasMore) return;
    page = next;
    await run();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  onMount(async () => {
    const params = new URL(location.href).searchParams;
    const q = params.get('q');
    if (q) {
      query = q;
      page = Math.max(1, Number(params.get('page') ?? '1') || 1);
      await tick();
      await run();
    }
    input?.focus();
  });
</script>

<svelte:head>
  <title>{query ? `${query} · Shoten` : 'Shoten · book search'}</title>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap"
  />
</svelte:head>

<div class="min-h-screen flex flex-col">
  <header class="flex items-center justify-between px-6 py-4">
    <a href="/" class="font-display text-xl tracking-tight">shoten</a>
    <button
      type="button"
      onclick={toggleMode}
      aria-label="toggle theme"
      class="rounded-full p-2 hover:bg-muted transition-colors"
    >
      {#if mode.current === 'dark'}
        <Sun class="size-5" />
      {:else}
        <Moon class="size-5" />
      {/if}
    </button>
  </header>

  <main class="flex-1 px-6 pb-16 mx-auto w-full max-w-5xl">
    {#if !touched}
      <div class="pt-[12vh] pb-10 text-center">
        <h1 class="wordmark text-7xl md:text-9xl leading-none mb-4">Shoten</h1>
        <p class="text-muted-foreground text-sm md:text-base">
          a quiet corner of the web for finding books
        </p>
      </div>
    {/if}

    <form
      onsubmit={(e) => {
        e.preventDefault();
        run({ resetPage: true });
      }}
      class="relative max-w-2xl mx-auto"
      class:mt-6={touched}
    >
      <Search class="size-5 absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" />
      <input
        bind:this={input}
        bind:value={query}
        type="search"
        placeholder="search for a title, author, ISBN…"
        autocomplete="off"
        spellcheck="false"
        class="w-full rounded-2xl border border-border bg-muted/40 pl-12 pr-4 py-4 text-base outline-none focus:border-accent focus:bg-background transition-colors"
      />
      {#if loading}
        <Loader2 class="size-5 absolute right-4 top-1/2 -translate-y-1/2 animate-spin text-muted-foreground" />
      {/if}
    </form>

    {#if touched && !loading && results.length === 0}
      <p class="text-center text-muted-foreground mt-12 text-sm">no results · try a different query</p>
    {/if}

    {#if results.length > 0}
      <div class="mt-10">
        <p class="text-xs uppercase tracking-widest text-muted-foreground mb-4">
          {results.length} results{page > 1 ? ` · page ${page}` : ''}
        </p>

        <ul class="divide-y divide-border">
          {#each results as book (book.id)}
            <li>
              <button
                type="button"
                onclick={() => openReader(book)}
                class="w-full text-left py-4 px-2 -mx-2 rounded-lg hover:bg-muted transition-colors group"
              >
                <div class="flex items-baseline gap-2 flex-wrap">
                  <span class="font-medium text-foreground group-hover:text-accent transition-colors">
                    {book.title}
                  </span>
                  {#if book.author}
                    <span class="text-sm text-muted-foreground italic">{book.author}</span>
                  {/if}
                </div>
                <div class="mt-1.5 flex items-center gap-2 flex-wrap text-xs text-muted-foreground">
                  {#if book.publisher}
                    <span class="font-mono">{book.publisher}</span>
                  {/if}
                  {#if book.year}
                    <span class="rounded-full bg-muted px-2 py-0.5">{book.year}</span>
                  {/if}
                  {#if book.extension}
                    <span class="rounded-full bg-muted px-2 py-0.5 uppercase">{book.extension}</span>
                  {/if}
                  {#if book.size}
                    <span class="rounded-full bg-muted px-2 py-0.5">{book.size}</span>
                  {/if}
                </div>
              </button>
            </li>
          {/each}
        </ul>

        {#if page > 1 || hasMore}
          <nav class="mt-8 flex items-center justify-center gap-2 text-sm">
            <button
              type="button"
              onclick={() => go(page - 1)}
              disabled={page <= 1}
              class="rounded-full p-2 hover:bg-muted disabled:opacity-30 disabled:hover:bg-transparent transition-colors"
              aria-label="previous page"
            >
              <ChevronLeft class="size-4" />
            </button>
            <span class="text-muted-foreground tabular-nums">page {page}</span>
            <button
              type="button"
              onclick={() => go(page + 1)}
              disabled={!hasMore}
              class="rounded-full p-2 hover:bg-muted disabled:opacity-30 disabled:hover:bg-transparent transition-colors"
              aria-label="next page"
            >
              <ChevronRight class="size-4" />
            </button>
          </nav>
        {/if}
      </div>
    {/if}
  </main>

  <footer class="px-6 py-6 text-center text-xs text-muted-foreground">
    public domain · <a href="https://github.com/Lulzx/shoten" class="hover:text-foreground">source</a>
  </footer>
</div>
