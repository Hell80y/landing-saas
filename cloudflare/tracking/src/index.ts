export default {
  async fetch(request: Request): Promise<Response> {
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    return Response.json({ status: "accepted" }, { status: 202 });
  },
};
