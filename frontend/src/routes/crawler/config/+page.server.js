import { fail } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();
		const formData = Object.fromEntries(rawFormData.entries());

		console.log("📥 Received form data:", formData);

		// Server-side validation
		if (!formData['target-url'] || formData['target-url'].trim() === '') {
			return fail(400, {
				error: true,
				message: 'Target URL is required.',
				values: formData
			});
		}

		// Transform
		const transformedData = {
			target_url: formData["target-url"],
			depth: formData["depth"] ? Number(formData["depth"]) : undefined,
			max_pages: formData["max-pages"] ? Number(formData["max-pages"]) : undefined,
			user_agent: formData["user-agent"] ? formData["user-agent"] : undefined,
			delay: formData["delay"] ? Number(formData["delay"]) : undefined,
			proxy: formData["proxy"] ? Number(formData["proxy"]) : undefined
		};

		try {
			const response = await fetch("http://127.0.0.1:8000/api/crawler", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json"
				},
				body: JSON.stringify(transformedData)
			});

			// Parse response body safely
			let json;
			try {
				json = await response.json();
				console.log("✅ Backend response:", json);
			} catch (e) {
				console.warn("⚠️ Could not parse JSON:", e.message);
			}

			// Only redirect if backend succeeded
			if (!response.ok) {
				return fail(response.status, {
					error: true,
					message: `Backend error: ${response.statusText}`,
					values: formData
				});
			}

      return {
        success: true,
        message: "All good!",
        values: formData
      };

		} catch (error) {
			console.error("🔥 Uncaught server error:", error);

			return fail(500, {
				error: true,
				message: "Internal server error",
				values: formData
			});
		}
	}
};
