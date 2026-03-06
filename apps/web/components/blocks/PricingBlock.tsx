interface Pricing {
  plan: string;
  price: string;
  features: string[];
}

export function PricingBlock({ items }: { items?: Pricing[] }) {
  const plans =
    items ??
    [
      { plan: 'Starter', price: '$29', features: ['1 landing', 'AI generation', 'Basic analytics'] },
      { plan: 'Growth', price: '$79', features: ['10 landings', 'A/B variants', 'Priority publish'] }
    ];

  return (
    <section className="rounded-xl border border-zinc-700 bg-zinc-900 p-8">
      <h3 className="text-2xl font-semibold">Pricing</h3>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        {plans.map((plan) => (
          <article key={plan.plan} className="rounded-lg border border-zinc-800 p-4">
            <h4 className="text-xl font-semibold">{plan.plan}</h4>
            <p className="mt-2 text-2xl font-bold">{plan.price}</p>
            <ul className="mt-3 space-y-1 text-sm text-zinc-300">
              {plan.features.map((feature) => (
                <li key={feature}>• {feature}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
