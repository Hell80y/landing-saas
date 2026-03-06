interface Benefit {
  title: string;
  description: string;
}

export function BenefitsBlock({ items }: { items?: Benefit[] }) {
  const benefits =
    items ??
    [
      { title: 'Fast generation', description: 'AI drafts your copy and structure in seconds.' },
      { title: 'Flexible editing', description: 'Customize each section and CTA based on your audience.' },
      { title: 'One-click publish', description: 'Ship production pages directly to edge runtime.' }
    ];

  return (
    <section className="rounded-xl border border-zinc-700 bg-zinc-900 p-8">
      <h3 className="text-2xl font-semibold">Benefits</h3>
      <div className="mt-4 grid gap-4 md:grid-cols-3">
        {benefits.map((benefit) => (
          <article key={benefit.title} className="rounded-lg border border-zinc-800 p-4">
            <h4 className="font-semibold">{benefit.title}</h4>
            <p className="mt-2 text-sm text-zinc-300">{benefit.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
