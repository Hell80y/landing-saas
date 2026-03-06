interface SocialProof {
  quote: string;
  author: string;
}

export function SocialProofBlock({ items }: { items?: SocialProof[] }) {
  const quotes =
    items ??
    [
      { quote: 'Our conversion rate doubled after switching.', author: 'Mara, Founder' },
      { quote: 'The fastest launch workflow we have used.', author: 'Andrei, PM' }
    ];

  return (
    <section className="rounded-xl border border-zinc-700 bg-zinc-900 p-8">
      <h3 className="text-2xl font-semibold">Social Proof</h3>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        {quotes.map((item) => (
          <blockquote key={item.author} className="rounded-lg border border-zinc-800 p-4">
            <p className="text-zinc-200">“{item.quote}”</p>
            <footer className="mt-2 text-sm text-zinc-400">— {item.author}</footer>
          </blockquote>
        ))}
      </div>
    </section>
  );
}
