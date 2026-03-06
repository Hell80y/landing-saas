const ALLOWED_EVENTS = new Set([
  "page_view",
  "scroll_depth",
  "cta_click",
  "checkout_started",
] as const);

type AllowedEvent =
  | "page_view"
  | "scroll_depth"
  | "cta_click"
  | "checkout_started";

interface TrackingEvent {
  event: AllowedEvent;
  timestamp: string;
  sessionId?: string;
  page?: string;
  metadata?: Record<string, string | number | boolean | null>;
}

interface Env {
  EVENTS_QUEUE?: Queue<TrackingEvent>;
  TRACKING_BUFFER?: KVNamespace;
  BACKEND_API_URL?: string;
  BACKEND_API_KEY?: string;
}

const isPlainObject = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const parseTrackingEvent = (input: unknown): TrackingEvent | null => {
  if (!isPlainObject(input)) {
    return null;
  }

  const { event, timestamp, sessionId, page, metadata } = input;

  if (typeof event !== "string" || !ALLOWED_EVENTS.has(event as AllowedEvent)) {
    return null;
  }

  if (typeof timestamp !== "string" || Number.isNaN(Date.parse(timestamp))) {
    return null;
  }

  if (sessionId !== undefined && typeof sessionId !== "string") {
    return null;
  }

  if (page !== undefined && typeof page !== "string") {
    return null;
  }

  if (metadata !== undefined) {
    if (!isPlainObject(metadata)) {
      return null;
    }

    const hasInvalidMetadataValue = Object.values(metadata).some(
      (value) =>
        ![
          "string",
          "number",
          "boolean",
        ].includes(typeof value) && value !== null,
    );

    if (hasInvalidMetadataValue) {
      return null;
    }
  }

  return {
    event,
    timestamp,
    ...(sessionId !== undefined ? { sessionId } : {}),
    ...(page !== undefined ? { page } : {}),
    ...(metadata !== undefined
      ? {
          metadata: metadata as Record<
            string,
            string | number | boolean | null
          >,
        }
      : {}),
  };
};

const persistEvent = async (event: TrackingEvent, env: Env): Promise<void> => {
  if (env.EVENTS_QUEUE) {
    await env.EVENTS_QUEUE.send(event);
    return;
  }

  if (env.TRACKING_BUFFER) {
    const id = crypto.randomUUID();
    await env.TRACKING_BUFFER.put(`event:${id}`, JSON.stringify(event), {
      expirationTtl: 60 * 60 * 24,
    });
  }
};

const forwardEvent = async (event: TrackingEvent, env: Env): Promise<void> => {
  if (!env.BACKEND_API_URL) {
    return;
  }

  const response = await fetch(`${env.BACKEND_API_URL.replace(/\/$/, "")}/events`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(env.BACKEND_API_KEY
        ? {
            authorization: `Bearer ${env.BACKEND_API_KEY}`,
          }
        : {}),
    },
    body: JSON.stringify(event),
  });

  if (!response.ok) {
    throw new Error(`Backend forwarding failed with status ${response.status}`);
  }
};

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const { pathname } = new URL(request.url);

    if (pathname !== "/e") {
      return new Response("Not Found", { status: 404 });
    }

    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    let body: unknown;

    try {
      body = await request.json();
    } catch {
      return Response.json({ error: "Invalid JSON payload" }, { status: 400 });
    }

    const event = parseTrackingEvent(body);

    if (!event) {
      return Response.json(
        {
          error:
            "Invalid event payload. Expected a supported event with ISO timestamp.",
        },
        { status: 400 },
      );
    }

    ctx.waitUntil(
      Promise.allSettled([persistEvent(event, env), forwardEvent(event, env)]).then(
        () => undefined,
      ),
    );

    return Response.json({ status: "accepted" }, { status: 202 });
  },
};
