import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/validationRules.js';

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
			console.warn('❌ Validation errors:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: formData
			});
		}

		// ✅ Transform data to match backend keys, set undefined for unfilled fields
		const transformedData = {
			target_url: formData['target-url'],
			parameters: formData['parameters'],
			http_method: formData['http-method'] || undefined,
			headers: formData['headers'] || undefined,
			proxy: formData['proxy'] || undefined,
			body_template: formData['body-template'] || undefined,
			wordlist
		};
		

		// Construct FormData for backend, only including defined values
		const fuzzerPayload = new FormData();
		for (const [key, value] of Object.entries(transformedData)) {
			if (value !== undefined && key !== 'wordlist') {
				fuzzerPayload.append(key, value);
			}
		}
		fuzzerPayload.append('wordlist', wordlist);

		try {
			const response = await fetch('http://127.0.0.1:8000/api/fuzzer', {
				method: 'POST',
				body: fuzzerPayload
			});

			const json = await response.json().catch((e) => {
				console.warn('⚠️ Failed to parse JSON:', e.message);
				return {};
			});

			if (!response.ok) {
				console.error('❌ Backend error:', response.statusText);
				return fail(response.status, {
					error: true,
					message: `Backend error: ${response.statusText}`,
					values: formData
				});
			}

			console.log('✅ Backend response:', json);
			return {
				success: true,
				message: 'Fuzzer launched successfully.',
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
