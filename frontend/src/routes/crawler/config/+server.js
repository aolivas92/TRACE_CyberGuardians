export async function POST({ request }) {
  try {
      const formData = await request.json();
      console.log("Received data in SvelteKit server:", formData);

      // Send data to FastAPI backend
      const response = await fetch("http://127.0.0.1:8000/api/crawler", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
      });

      const result = await response.json();
      console.log("Response from backend:", result);

      return new Response(JSON.stringify(result), {
          status: response.status,
          headers: { "Content-Type": "application/json" },
      });
  } catch (error) {
      console.error("Error processing request:", error);
      return new Response(JSON.stringify({ error: "Internal server error" }), {
          status: 500,
          headers: { "Content-Type": "application/json" },
      });
  }
}
