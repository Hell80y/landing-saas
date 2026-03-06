interface FAQ {
  question: string;
  answer: string;
}

export function FAQBlock({ items }: { items?: FAQ[] }) {
  const faqItems =
    items ??
    [
      { question: 'Can I edit generated content?', answer: 'Yes, all sections are editable in dashboard.' },
      { question: 'Where is the landing hosted?', answer: 'Published landings are served from Cloudflare edge.' }
    ];

  return (
    <section className="rounded-xl border border-zinc-700 bg-zinc-900 p-8">
      <h3 className="text-2xl font-semibold">FAQ</h3>
      <div className="mt-4 space-y-3">
        {faqItems.map((item) => (
          <details key={item.question} className="rounded-lg border border-zinc-800 p-4">
            <summary className="cursor-pointer font-medium">{item.question}</summary>
            <p className="mt-2 text-sm text-zinc-300">{item.answer}</p>
          </details>
        ))}
      </div>
    </section>
  );
}
