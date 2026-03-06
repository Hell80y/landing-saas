'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Landing } from '@/lib/types';

export default function LandingsPage() {
  const [landings, setLandings] = useState<Landing[]>([]);
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      setLandings(await api.listLandings());
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function createLanding(event: FormEvent) {
    event.preventDefault();
    if (!name.trim()) return;

    try {
      await api.createLanding({ name });
      setName('');
      await refresh();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Landings</h2>
        <p className="text-zinc-400">Manage all landing pages.</p>
      </div>

      <form onSubmit={createLanding} className="flex gap-3 rounded-xl border border-zinc-800 bg-zinc-900 p-4">
        <input
          className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2"
          placeholder="New landing name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button className="rounded-lg bg-green-500 px-4 py-2 font-semibold text-black">Create landing</button>
      </form>

      {error && <p className="text-red-400">{error}</p>}

      <div className="grid gap-3">
        {landings.map((landing) => (
          <Link
            key={landing.id}
            href={`/landings/${landing.id}`}
            className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 transition hover:border-zinc-600"
          >
            <div className="flex items-center justify-between">
              <h3 className="font-medium">{landing.name}</h3>
              <span className="text-xs uppercase text-zinc-400">{landing.status}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
