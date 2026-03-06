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
