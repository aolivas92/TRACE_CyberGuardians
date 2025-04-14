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

		// Validate fields
		for (const [id, value] of Object.entries(formData)) {
			const result = validateField(id, value);
			if (result.error) {
				fieldErrors[id] = { error: true, message: result.message };
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

		// Required field fallback
		const requiredFields = ['target-url', 'parameters', 'http-method'];
		for (const field of requiredFields) {
			if (!formData[field]) {
				fieldErrors[field] = {
					error: true,
					message: `${field.replace('-', ' ')} is required.`
				};
			}
		}

		if (Object.keys(fieldErrors).length > 0) {
			console.warn('Validation errors:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: formData
			});
		}



		// Construct FormData for backend, only including defined values
		const fuzzerPayload = new FormData();

		// Step 1: Construct the JSON config
		const configForBackend = {
			target_url: formData['target-url'],
			http_method: formData['http-method'],
			parameters: formData['parameters'].split(',').map(p => p.trim()),
			headers: formData['headers'] ? JSON.parse(formData['headers']) : undefined,
			cookies: formData['cookies'] ? JSON.parse(formData['cookies']) : undefined,
			proxy: formData['proxy'] || undefined,
			body_template: formData['body-template'] ? JSON.parse(formData['body-template']) : undefined,
			// payload_file will be handled separately
		};
		
		// Step 2: Append the JSON string as one field
		fuzzerPayload.append('config', JSON.stringify(configForBackend));
		
		// Step 3: Attach the wordlist file as `payload_file`
		fuzzerPayload.append('payload_file', wordlist);
		
		


		try {
			const response = await fetch('http://127.0.0.1:8000/api/fuzzer', {
				method: 'POST',
				headers: {
					Accept: "application/json"
				},
				body: fuzzerPayload
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
				message: 'Fuzzer scan started successfully!',
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
	}
};
