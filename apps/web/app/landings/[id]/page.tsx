'use client';

import { useParams } from 'next/navigation';
import { useEffect, useMemo, useState } from 'react';
import { ThemeRenderer } from '@/components/ThemeRenderer';
import { api } from '@/lib/api';
import { CombinedSpec, Landing } from '@/lib/types';

const defaultSpec: CombinedSpec = {
  meta: { title: 'New Landing' },
  design: { primaryColor: '#22c55e', backgroundColor: '#09090b', textColor: '#fafafa' },
  content: {},
  page: {
    blocks: ['HeroBlock', 'BenefitsBlock', 'SocialProofBlock', 'PricingBlock', 'FAQBlock', 'FinalCTABlock']
  }
};

export default function LandingDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;

  const [landing, setLanding] = useState<Landing | null>(null);
  const [name, setName] = useState('');
  const [specText, setSpecText] = useState(JSON.stringify(defaultSpec, null, 2));
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void loadLanding();
  }, [id]);

  async function loadLanding() {
    try {
      const data = await api.getLanding(id);
      setLanding(data);
      setName(data.name);
      setSpecText(JSON.stringify(data.combined_spec ?? defaultSpec, null, 2));
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  const parsedSpec = useMemo(() => {
    try {
      return JSON.parse(specText) as CombinedSpec;
    } catch {
      return null;
    }
  }, [specText]);

  async function onSave() {
    try {
      if (!parsedSpec) {
        throw new Error('CombinedSpec JSON is invalid.');
      }

      const updated = await api.updateLanding(id, {
        name,
        combined_spec: parsedSpec
      } as Partial<Landing>);
      setLanding(updated);
      setStatusMessage('Landing updated successfully.');
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function onGenerate() {
    try {
      const generated = await api.generateContent(id);
      setLanding(generated);
      setSpecText(JSON.stringify(generated.combined_spec, null, 2));
      setStatusMessage('Content generated successfully.');
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function onPublish() {
    try {
      const published = await api.publishLanding(id);
      setLanding(published);
      setStatusMessage('Landing published successfully.');
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <section className="space-y-4 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
        <h2 className="text-2xl font-semibold">Edit landing</h2>
        <label className="block text-sm">
          <span className="mb-1 block text-zinc-400">Landing name</span>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2"
          />
        </label>

        <label className="block text-sm">
          <span className="mb-1 block text-zinc-400">CombinedSpec</span>
          <textarea
            value={specText}
            onChange={(e) => setSpecText(e.target.value)}
            className="h-[420px] w-full rounded-lg border border-zinc-700 bg-zinc-950 p-3 font-mono text-xs"
          />
        </label>

        <div className="flex flex-wrap gap-3">
          <button onClick={onSave} className="rounded-lg bg-green-500 px-4 py-2 font-semibold text-black">
            Save changes
          </button>
          <button onClick={onGenerate} className="rounded-lg bg-blue-500 px-4 py-2 font-semibold text-black">
            Generate content
          </button>
          <button onClick={onPublish} className="rounded-lg bg-purple-500 px-4 py-2 font-semibold text-black">
            Publish landing
          </button>
        </div>

        <p className="text-sm text-zinc-400">Status: {landing?.status ?? 'loading'}</p>
        {statusMessage && <p className="text-sm text-green-400">{statusMessage}</p>}
        {error && <p className="text-sm text-red-400">{error}</p>}
      </section>

      <section>
        <h3 className="mb-3 text-lg font-semibold">Preview</h3>
        {parsedSpec ? (
          <ThemeRenderer spec={parsedSpec} />
        ) : (
          <p className="rounded-lg border border-red-700 bg-red-900/20 p-3 text-sm text-red-300">
            Invalid CombinedSpec JSON.
          </p>
        )}
      </section>
    </div>
  );
}
