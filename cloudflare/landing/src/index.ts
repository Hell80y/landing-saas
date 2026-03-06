import { renderLandingHtml } from './template';
import type { CombinedSpec, Env } from './types';

const LANDING_PREFIX = 'landing:';
const HTML_HEADERS = {
  'content-type': 'text/html; charset=UTF-8',
  'cache-control': 'public, max-age=60, s-maxage=600, stale-while-revalidate=300',
};

const extractSlug = (url: URL): string | null => {
  const path = url.pathname.replace(/^\/+|\/+$/g, '');

  if (!path || path.includes('/')) {
    return null;
  }

  return path;
};

const notFound = (): Response =>
  new Response('Landing not found', {
    status: 404,
    headers: {
      'content-type': 'text/plain; charset=UTF-8',
      'cache-control': 'public, max-age=30',
    },
  });

const badRequest = (): Response =>
  new Response('Route must be /{slug}', {
    status: 400,
    headers: {
      'content-type': 'text/plain; charset=UTF-8',
      'cache-control': 'no-store',
    },
  });

export default {
  async fetch(request: Request, env: Env, context: ExecutionContext): Promise<Response> {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method Not Allowed', {
        status: 405,
        headers: { allow: 'GET, HEAD' },
      });
    }

    const url = new URL(request.url);
    const slug = extractSlug(url);

    if (!slug) {
      return badRequest();
    }

    const cache = caches.default;
    const cacheKey = new Request(url.toString(), request);

    const cachedResponse = await cache.match(cacheKey);
    if (cachedResponse) {
      return cachedResponse;
    }

    const kvKey = `${LANDING_PREFIX}${slug}`;
    const storedSpec = await env.LANDING_KV.get<CombinedSpec>(kvKey, 'json');

    if (!storedSpec || typeof storedSpec !== 'object') {
      return notFound();
    }

    const html = renderLandingHtml(storedSpec, slug);
    const response = new Response(html, { status: 200, headers: HTML_HEADERS });

    context.waitUntil(cache.put(cacheKey, response.clone()));

    return request.method === 'HEAD' ? new Response(null, response) : response;
export interface Env {
  COMBINED_SPEC_KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const cache = caches.default;
    const cacheKey = new Request(url.toString(), request);

    const cached = await cache.match(cacheKey);
    if (cached) {
      return cached;
    }

    const slug = url.pathname.replace(/^\//, "") || "index";
    const spec = await env.COMBINED_SPEC_KV.get(slug, "json");

    const response = Response.json(
      {
        status: "scaffold",
        slug,
        hasSpec: spec !== null,
      },
      {
        headers: {
          "cache-control": "public, max-age=60",
        },
      },
    );

    ctx.waitUntil(cache.put(cacheKey, response.clone()));
    return response;
  },
};
