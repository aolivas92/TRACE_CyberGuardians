import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/validationRules.js';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();
		const formData = Object.fromEntries(rawFormData.entries());

		console.log('🧾 Form fields:', formData);

		const fieldErrors = {};

		// Validate all fields using validationRules
		for (const [id, value] of Object.entries(formData)) {
			const result = validateField(id, value);
			if (result.error) {
				fieldErrors[id] = {
					error: true,
					message: result.message
				};
			}
		}

		// Additional required field checks
		if (!formData['target-url']) {
			fieldErrors['target-url'] = {
				error: true,
				message: 'Target URL is required.'
			};
		}

		// If any errors exist, fail with structured feedback
		if (Object.keys(fieldErrors).length > 0) {
			console.warn('❌ Validation errors in crawler:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: formData
			});
		}

		// Transform field names to match backend API
		const transformedData = {
			target_url: formData['target-url'],
			depth: formData['depth'] ? Number(formData['depth']) : undefined,
			max_pages: formData['max-pages'] ? Number(formData['max-pages']) : undefined,
			delay: formData['delay'] ? Number(formData['delay']) : undefined,
			proxy: formData['proxy'] ? Number(formData['proxy']) : undefined,
			user_agent: formData['user-agent'] || undefined,
			excluded_urls: formData['excluded-urls'] || undefined,
			crawl_date: formData['crawl-date'] || undefined,
			crawl_time: formData['crawl-time'] || undefined
		};

		try {
			const response = await fetch('http://127.0.0.1:8000/api/crawler', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify(transformedData)
			});

			const json = await response.json().catch((e) => {
				console.warn('⚠️ Could not parse JSON response:', e.message);
				return {};
			});

			if (!response.ok) {
				console.error('❌ Backend responded with error:', json);
				return fail(response.status, {
					error: true,
					message: `Backend error: ${response.statusText}`,
					values: formData
				});
			}

			console.log('✅ Crawler backend response:', json);
			return {
				success: true,
				message: 'Crawler launched successfully.',
				values: formData
			};
		} catch (error) {
			console.error('🔥 Uncaught server error:', error);
			return fail(500, {
				error: true,
				message: 'Internal server error',
				values: formData
			});
		}
	}
};
