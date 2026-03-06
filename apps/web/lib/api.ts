import { Landing } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {})
    },
    cache: 'no-store'
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API request failed (${response.status}): ${errorText}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  listLandings: () => request<Landing[]>('/landings'),
  getLanding: (id: string) => request<Landing>(`/landings/${id}`),
  createLanding: (payload: { name: string }) =>
    request<Landing>('/landings', { method: 'POST', body: JSON.stringify(payload) }),
  updateLanding: (id: string, payload: Partial<Landing>) =>
    request<Landing>(`/landings/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  generateContent: (id: string) => request<Landing>(`/landings/${id}/generate`, { method: 'POST' }),
  publishLanding: (id: string) => request<Landing>(`/landings/${id}/publish`, { method: 'POST' })
};
