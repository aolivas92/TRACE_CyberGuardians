/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	console.log("POST handler in +server.js for /credGenAI/config");

	try {
		const formData = await request.formData();
		const wordlistFile = formData.get("wordlist");

		if (!wordlistFile) {
			return new Response(
				JSON.stringify({ message: "No wordlist file provided." }),
				{ status: 400, headers: { "Content-Type": "application/json" } }
			);
		}

		const wordlistBuffer = await wordlistFile.arrayBuffer();

		const backendUrl = "http://127.0.0.1:8000/api/credGenAI/config";
		const formToSend = new FormData();
		formToSend.append("wordlist", new Blob([wordlistBuffer]), wordlistFile.name);

		const response = await fetch(backendUrl, {
			method: "POST",
			body: formToSend,
		});

		if (!response.ok) {
			const errorText = await response.text();
			return new Response(
				JSON.stringify({ message: "Backend error", details: errorText }),
				{ status: response.status, headers: { "Content-Type": "application/json" } }
			);
		}

		const result = await response.json();
		return new Response(JSON.stringify(result), {
			status: 200,
			headers: { "Content-Type": "application/json" },
		});

	} catch (err) {
		console.error("Error in wordlist POST:", err);
		return new Response(
			JSON.stringify({ message: "Internal server error", error: err.message }),
			{ status: 500, headers: { "Content-Type": "application/json" } }
		);
	}
}