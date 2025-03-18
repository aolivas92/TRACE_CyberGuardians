export async function POST({ request }) {
  try {
      const data = await request.json();
      console.log("Received data in Svelte Server:", data);

      // Forward the request to the Python backend
      const response = await fetch("http://127.0.0.1:5000/api/crawler/config", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
      });

      const result = await response.json();
      return new Response(JSON.stringify(result), { status: response.status });
  } catch (error) {
      console.error("Error processing request:", error);
      return new Response(JSON.stringify({ error: "Failed to process request" }), { status: 500 });
  }
}
