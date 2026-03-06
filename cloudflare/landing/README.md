# Cloudflare Landing Runtime

This worker serves generated landing pages from Cloudflare KV without any database calls.

## Route behavior

- Accepts `GET` and `HEAD` requests only.
- Route format must be `/{slug}`.
- Looks up `CombinedSpec` in KV using key format: `landing:{slug}`.
- Renders HTML from the fetched spec.
- Caches responses in Cloudflare edge cache (`caches.default`) and sets cache headers.

## Performance

To support a sub-50ms edge target:

- no database/network hops beyond local KV
- `caches.default` read before KV read
- aggressive `s-maxage` and `stale-while-revalidate` caching headers

## KV write example

```bash
wrangler kv key put --binding LANDING_KV "landing:demo" '{"meta":{"title":"Demo"},"content":{"heroTitle":"Hello from KV"}}'
```
