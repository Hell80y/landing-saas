interface HeroBlockProps {
  headline?: string;
  subheadline?: string;
  cta?: string;
  primaryColor?: string;
}

export function HeroBlock({ headline, subheadline, cta, primaryColor }: HeroBlockProps) {
  return (
    <section className="rounded-xl border border-zinc-700 bg-zinc-900 p-8 text-center">
      <h2 className="text-3xl font-bold">{headline ?? 'Build your best landing page in minutes'}</h2>
      <p className="mx-auto mt-3 max-w-2xl text-zinc-300">
        {subheadline ?? 'Generate conversion-ready content and publish instantly.'}
      </p>
      <button
        className="mt-6 rounded-lg px-5 py-3 font-semibold text-black"
        style={{ backgroundColor: primaryColor ?? '#22c55e' }}
      >
        {cta ?? 'Get Started'}
      </button>
    </section>
  );
}
