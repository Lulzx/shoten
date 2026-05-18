import type { Book } from '$lib/types';

const MIRRORS = ['https://libgen.is', 'https://libgen.rs', 'https://libgen.st'];
const PAGE_SIZE = 25;

interface LibgenRow {
  id: string;
  title: string;
  author: string;
  publisher: string;
  year: string;
  filesize: string;
  extension: string;
  md5: string;
}

async function fetchWithFallback(path: string): Promise<Response> {
  let lastError: unknown;
  for (const base of MIRRORS) {
    try {
      const res = await fetch(base + path, {
        headers: { 'user-agent': 'shoten/2.0 (+https://github.com/lulzx/shoten)' },
        signal: AbortSignal.timeout(8000)
      });
      if (res.ok) return res;
      lastError = new Error(`${base} → ${res.status}`);
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError ?? new Error('all libgen mirrors failed');
}

function parseIds(html: string): string[] {
  const ids = new Set<string>();
  const re = /<tr[^>]*>\s*<td[^>]*>(\d{3,})<\/td>/gi;
  let m: RegExpExecArray | null;
  while ((m = re.exec(html)) !== null) ids.add(m[1]);
  return [...ids];
}

function parseTotal(html: string): number {
  const m = html.match(/(\d+)\s+files\s+found/i);
  return m ? Number(m[1]) : 0;
}

function humanSize(bytes: string): string {
  const n = Number(bytes);
  if (!Number.isFinite(n) || n <= 0) return '—';
  const units = ['B', 'KB', 'MB', 'GB'];
  let i = 0;
  let v = n;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(v < 10 ? 1 : 0)} ${units[i]}`;
}

function toBook(row: LibgenRow): Book {
  return {
    id: row.id,
    title: row.title || 'Untitled',
    author: row.author || '',
    publisher: row.publisher || '',
    year: row.year && row.year !== '0' ? row.year : '',
    size: humanSize(row.filesize),
    extension: row.extension || '',
    md5: row.md5,
    download: `http://library.lol/main/${row.md5.toUpperCase()}`
  };
}

export async function searchBooks(
  query: string,
  page: number
): Promise<{ results: Book[]; count: number; pages: number }> {
  const safe = encodeURIComponent(query.trim());
  if (!safe) return { results: [], count: 0, pages: 0 };

  const searchPath = `/search.php?req=${safe}&res=${PAGE_SIZE}&view=simple&phrase=1&column=def&page=${page}`;
  const searchHtml = await fetchWithFallback(searchPath).then((r) => r.text());
  const ids = parseIds(searchHtml);
  const count = parseTotal(searchHtml);
  const pages = Math.max(1, Math.ceil(count / PAGE_SIZE));

  if (ids.length === 0) return { results: [], count, pages };

  const fields = 'id,title,author,year,extension,filesize,publisher,md5';
  const jsonPath = `/json.php?ids=${ids.join(',')}&fields=${fields}`;
  const rows = (await fetchWithFallback(jsonPath).then((r) => r.json())) as LibgenRow[];

  return { results: rows.map(toBook), count, pages };
}
