interface KVNamespace {
  get<T = string>(key: string, type: 'text'): Promise<T | null>;
  get<T = unknown>(key: string, type: 'json'): Promise<T | null>;
}

interface ExecutionContext {
  waitUntil(promise: Promise<unknown>): void;
}

interface CacheStorage {
  default: Cache;
}
