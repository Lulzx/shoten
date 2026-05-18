import type { Book } from '$lib/types';

const MIRRORS = ['https://libgen.li', 'https://libgen.gs'];
const PAGE_SIZE = 25;
const FETCH_TIMEOUT_MS = 12_000;

interface EditionRow {
  title?: string;
  author?: string;
  publisher?: string;
  year?: string;
  files?: Record<string, { f_id: string; md5: string }>;
}

interface FileRow {
  md5: string;
  extension?: string;
  filesize?: string;
}

async function fetchWithFallback(path: string): Promise<Response> {
  let lastError: unknown;
  for (const base of MIRRORS) {
    try {
      const res = await fetch(base + path, {
        headers: {
          'user-agent': 'shoten/2.0 (+https://github.com/lulzx/shoten)',
          accept: 'text/html,application/json;q=0.9'
        },
        signal: AbortSignal.timeout(FETCH_TIMEOUT_MS)
      });
      if (res.ok) return res;
      lastError = new Error(`${base} → ${res.status}`);
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError ?? new Error('all libgen mirrors failed');
}

function parseEditionIds(html: string): string[] {
  const ids = new Set<string>();
  const re = /edition\.php\?id=(\d+)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(html)) !== null) ids.add(m[1]);
  return [...ids].slice(0, PAGE_SIZE);
}

function humanSize(bytes: string | undefined): string {
  const n = Number(bytes);
  if (!Number.isFinite(n) || n <= 0) return '';
  const units = ['B', 'KB', 'MB', 'GB'];
  let i = 0;
  let v = n;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(v < 10 ? 1 : 0)} ${units[i]}`;
}

function cleanAuthor(author: string): string {
  if (!author) return '';
  return author.split(';').map((s) => s.trim()).filter(Boolean).slice(0, 2).join(', ');
}

export async function searchBooks(
  query: string,
  page: number
): Promise<{ results: Book[]; hasMore: boolean }> {
  const q = encodeURIComponent(query.trim());
  if (!q) return { results: [], hasMore: false };

  const searchPath = `/index.php?req=${q}&page=${page}`;
  const html = await fetchWithFallback(searchPath).then((r) => r.text());
  const editionIds = parseEditionIds(html);
  if (editionIds.length === 0) return { results: [], hasMore: false };

  const fields = 'title,author,publisher,year,files';
  const editionsPath = `/json.php?object=e&ids=${editionIds.join(',')}&addkeys=files&fields=${fields}`;
  const editions = (await fetchWithFallback(editionsPath).then((r) => r.json())) as Record<
    string,
    EditionRow
  >;

  const fileIds: string[] = [];
  const editionToFileId = new Map<string, string>();
  for (const [eid, ed] of Object.entries(editions)) {
    const firstFile = ed.files && Object.values(ed.files)[0];
    if (firstFile?.f_id) {
      fileIds.push(firstFile.f_id);
      editionToFileId.set(eid, firstFile.f_id);
    }
  }

  let files: Record<string, FileRow> = {};
  if (fileIds.length > 0) {
    const filesPath = `/json.php?object=f&ids=${fileIds.join(',')}&fields=md5,extension,filesize`;
    files = (await fetchWithFallback(filesPath).then((r) => r.json())) as Record<string, FileRow>;
  }

  const results: Book[] = [];
  for (const eid of editionIds) {
    const ed = editions[eid];
    if (!ed) continue;
    const fid = editionToFileId.get(eid);
    const file = fid ? files[fid] : undefined;
    if (!file?.md5) continue;
    results.push({
      id: eid,
      title: ed.title || 'Untitled',
      author: cleanAuthor(ed.author ?? ''),
      publisher: ed.publisher ?? '',
      year: ed.year && ed.year !== '0' ? ed.year : '',
      size: humanSize(file.filesize),
      extension: (file.extension ?? '').toLowerCase(),
      md5: file.md5,
      download: `https://libgen.li/ads.php?md5=${file.md5}`
    });
  }

  return { results, hasMore: editionIds.length >= PAGE_SIZE };
}
