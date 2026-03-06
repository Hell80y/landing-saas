export interface CombinedSpec {
  meta?: {
    title?: string;
    description?: string;
    [key: string]: unknown;
  };
  design?: {
    brandColor?: string;
    backgroundColor?: string;
    textColor?: string;
    [key: string]: unknown;
  };
  content?: {
    heroTitle?: string;
    heroSubtitle?: string;
    ctaLabel?: string;
    [key: string]: unknown;
  };
  page?: Record<string, unknown>;
  commerce?: Record<string, unknown>;
  tracking?: Record<string, unknown>;
  [key: string]: unknown;
}

export interface Env {
  LANDING_KV: KVNamespace;
}
