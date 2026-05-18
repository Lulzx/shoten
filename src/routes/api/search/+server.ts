import { error, json } from '@sveltejs/kit';
import { searchBooks } from '$lib/server/libgen';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url, setHeaders }) => {
  const q = url.searchParams.get('q')?.trim() ?? '';
  const page = Math.max(1, Number(url.searchParams.get('page') ?? '1') || 1);

  if (!q) return json({ results: [], page, hasMore: false });

  try {
    const { results, hasMore } = await searchBooks(q, page);
    setHeaders({ 'cache-control': 'public, max-age=300, s-maxage=600' });
    return json({ results, page, hasMore });
  } catch (err) {
    console.error('search failed', err);
    throw error(502, 'upstream book index is unreachable');
  }
};
