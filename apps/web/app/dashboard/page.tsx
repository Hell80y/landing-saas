'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Landing } from '@/lib/types';

export default function DashboardPage() {
  const [landings, setLandings] = useState<Landing[]>([]);
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void loadLandings();
  }, []);

  async function loadLandings() {
    try {
      setLoading(true);
      const data = await api.listLandings();
      setLandings(data);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function onCreateLanding(event: FormEvent) {
    event.preventDefault();
    if (!name.trim()) return;

    try {
      await api.createLanding({ name });
      setName('');
      await loadLandings();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="space-y-8">
      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <p className="mt-2 text-sm text-zinc-400">Create and manage landing pages from one place.</p>
      </section>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <h3 className="text-lg font-semibold">Create landing</h3>
        <form onSubmit={onCreateLanding} className="mt-4 flex gap-3">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2"
            placeholder="Landing name"
          />
          <button type="submit" className="rounded-lg bg-green-500 px-4 py-2 font-semibold text-black">
            Create
          </button>
        </form>
      </section>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Recent landings</h3>
          <Link href="/landings" className="text-sm text-green-400">
            View all
          </Link>
        </div>
        {loading && <p className="mt-4 text-zinc-400">Loading...</p>}
        {error && <p className="mt-4 text-red-400">{error}</p>}
        <ul className="mt-4 space-y-2">
          {landings.slice(0, 5).map((landing) => (
            <li key={landing.id} className="rounded-lg border border-zinc-800 p-3">
              <Link href={`/landings/${landing.id}`} className="flex items-center justify-between">
                <span>{landing.name}</span>
                <span className="text-xs uppercase text-zinc-400">{landing.status}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
