import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/fieldValidatorFactory.js';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();

		const wordlist = rawFormData.get('wordlist');
		const formData = Object.fromEntries(rawFormData.entries());
		delete formData.wordlist;

		console.log('📥 Received wordlist:', wordlist?.name);
		console.log('📦 File size:', wordlist?.size);
		console.log('🧾 Form fields:', formData);

		const fieldErrors = {};

		// Validate all input fields
		for (const [id, value] of Object.entries(formData)) {
			const { error, message } = validateField(id, value);
			if (error) {
				fieldErrors[id] = { error: true, message };
			}
		}

		// Validate wordlist
		const fileValidation = validateField('wordlist', wordlist);
		if (fileValidation.error) {
			fieldErrors.wordlist = {
				error: true,
				message: fileValidation.message
			};
		}

		// Validate presence of required fields
		const requiredFields = ['target-url', 'attempt-limit'];
		for (const field of requiredFields) {
			if (!formData[field]) {
				fieldErrors[field] = {
					error: true,
					message: `${field.replace(/-/g, ' ')} is required.`
				};
			}
		}

		// If any validation errors, return
		if (Object.keys(fieldErrors).length > 0) {
			console.warn('Validation errors:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: formData
			});
		}

		// Map input field names to backend keys
		const transformedData = {
			target_url: formData["target-url"],
			attempt_limit: formData["attempt-limit"] ? Number(formData["attempt-limit"]) : undefined,
			top_level_directory: formData["top-level-directory"] ? formData["top-level-directory"] : undefined,
			hide_status_codes: formData["hide-status-codes"] ? formData["hide-status-codes"] : undefined,
			show_status_codes: formData["show-status-codes"] ? formData["show-status-codes"] : undefined,
			filter_content_length: formData["filter-content-length"] ? formData["filter-content-length"] : undefined,
			wordlist
		};

		const bruteForcePayload = new FormData();
		for (const [key, value] of Object.entries(transformedData)) {
			if (value !== undefined && key !== 'wordlist') {
				bruteForcePayload.append(key, value);
			}
		}
		bruteForcePayload.append('wordlist', wordlist);

		try {
			const response = await fetch('http://127.0.0.1:8000/api/bruteForce', {
				method: 'POST',
				headers: {
					Accept: 'application/json'
				},
				body: bruteForcePayload
			});

			let json;
			try {
				json = await response.json();
				console.log("Backend response:", json);
			} catch (e) {
				console.warn("Could not parse JSON:", e.message);
			}

			if (!response.ok) {
				return fail(response.status, {
					error: true,
					message: `Backend error: ${response.statusText}`,
					values: formData
				});
			}

			return {
				success: true,
				message: 'Brute Force scan started successfully!',
				values: formData,
				job_id: json?.job_id
			};
		} catch (error) {
			console.error('Uncaught server error:', error);
			return fail(500, {
				error: true,
				message: 'Internal server error',
				values: formData
			});
		}

		
		// FOR TESTING ONLY
		// console.log('Skipping actual backend request for testing...');
		// console.log('Payload that would have been sent:', bruteForcePayload);
		
		// return {
		// 	success: true,
		// 	message: 'Simulated brute force launch successful (no backend call made).',
		// 	values: formData
		// };
	}
};
