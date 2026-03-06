interface FinalCta {
  title?: string;
  description?: string;
  buttonText?: string;
}

export function FinalCTABlock({ item, primaryColor }: { item?: FinalCta; primaryColor?: string }) {
  return (
    <section className="rounded-xl border border-zinc-700 bg-zinc-900 p-8 text-center">
      <h3 className="text-2xl font-semibold">{item?.title ?? 'Ready to launch?'}</h3>
      <p className="mt-2 text-zinc-300">
        {item?.description ?? 'Generate and publish your conversion-ready landing page now.'}
      </p>
      <button
        className="mt-5 rounded-lg px-5 py-3 font-semibold text-black"
        style={{ backgroundColor: primaryColor ?? '#22c55e' }}
      >
        {item?.buttonText ?? 'Launch now'}
      </button>
    </section>
  );
}
