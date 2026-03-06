import type { CombinedSpec } from './types';

const escapeHtml = (value: string): string =>
  value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');

const toText = (value: unknown, fallback: string): string =>
  typeof value === 'string' && value.trim().length > 0 ? value : fallback;

export const renderLandingHtml = (spec: CombinedSpec, slug: string): string => {
  const title = escapeHtml(toText(spec.meta?.title, `Landing ${slug}`));
  const description = escapeHtml(toText(spec.meta?.description, 'Generated landing page'));
  const brandColor = escapeHtml(toText(spec.design?.brandColor, '#2563eb'));
  const backgroundColor = escapeHtml(toText(spec.design?.backgroundColor, '#ffffff'));
  const textColor = escapeHtml(toText(spec.design?.textColor, '#0f172a'));
  const heroTitle = escapeHtml(toText(spec.content?.heroTitle, title));
  const heroSubtitle = escapeHtml(toText(spec.content?.heroSubtitle, description));
  const ctaLabel = escapeHtml(toText(spec.content?.ctaLabel, 'Get started'));

  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${title}</title>
    <meta name="description" content="${description}" />
    <style>
      :root {
        --brand-color: ${brandColor};
        --bg-color: ${backgroundColor};
        --text-color: ${textColor};
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Inter, system-ui, -apple-system, sans-serif;
        color: var(--text-color);
        background: var(--bg-color);
      }
      main {
        min-height: 100vh;
        display: grid;
        place-items: center;
        padding: 2rem;
      }
      section {
        max-width: 720px;
        text-align: center;
      }
      h1 { font-size: clamp(2rem, 5vw, 3rem); margin: 0 0 1rem; }
      p { line-height: 1.6; margin: 0 0 2rem; }
      a {
        display: inline-block;
        background: var(--brand-color);
        color: white;
        text-decoration: none;
        border-radius: 0.75rem;
        font-weight: 600;
        padding: 0.85rem 1.5rem;
      }
    </style>
  </head>
  <body>
    <main>
      <section>
        <h1>${heroTitle}</h1>
        <p>${heroSubtitle}</p>
        <a href="#cta">${ctaLabel}</a>
      </section>
    </main>
    <script type="application/json" id="combined-spec">${escapeHtml(JSON.stringify(spec))}</script>
  </body>
</html>`;
};
