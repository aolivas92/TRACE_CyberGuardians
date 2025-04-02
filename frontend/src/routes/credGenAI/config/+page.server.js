import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/validationRules.js';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();

		// Extract wordlist separately
		const wordlistFile = rawFormData.get('wordlist');
		const formData = Object.fromEntries(rawFormData.entries());
		delete formData.wordlist;

		console.log('📥 Received wordlist:', wordlistFile?.name);
		console.log('📦 File size:', wordlistFile?.size);
		console.log('🧾 Form fields:', formData);

		const fieldErrors = {};

		// Validate file
		const fileValidation = validateField('wordlist', wordlistFile);
		if (fileValidation.error || !(wordlistFile instanceof File) || wordlistFile.size === 0) {
			fieldErrors.wordlist = {
				error: true,
				message: fileValidation.message || 'Please upload a valid wordlist file.'
			};
		}

		// Validate text/number fields
		for (const [id, value] of Object.entries(formData)) {
			const result = validateField(id, value);
			if (result.error) {
				fieldErrors[id] = {
					error: true,
					message: result.message
				};
			}
		}

		// Return early if validation failed
		if (Object.keys(fieldErrors).length > 0) {
			console.warn('❌ Validation errors in credgenAI:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: formData
			});
		}

		// Transform data with undefined for missing optional fields
		const transformedData = {
			username_length: formData['username-length'] ? Number(formData['username-length']) : undefined,
			password_length: formData['password-length'] ? Number(formData['password-length']) : undefined,
			username_caps: formData['username-caps'] === 'on' ? true : undefined,
			username_numbers: formData['username-numbers'] === 'on' ? true : undefined,
			username_symbols: formData['username-symbols'] === 'on' ? true : undefined,
			password_caps: formData['password-caps'] === 'on' ? true : undefined,
			password_numbers: formData['password-numbers'] === 'on' ? true : undefined,
			password_symbols: formData['password-symbols'] === 'on' ? true : undefined
		};

		// Assemble payload using FormData
		const credgenPayload = new FormData();
		for (const [key, value] of Object.entries(transformedData)) {
			if (value !== undefined) {
				credgenPayload.append(key, value);
			}
		}
		credgenPayload.append('wordlist', wordlistFile);

		try {
			const response = await fetch('http://127.0.0.1:8000/api/credgen', {
				method: 'POST',
				body: credgenPayload
			});

			const json = await response.json().catch(e => {
				console.warn('⚠️ Failed to parse JSON:', e.message);
				return {};
			});

			if (!response.ok) {
				console.error('❌ Backend error:', json);
				return fail(response.status, {
					error: true,
					message: `Backend error: ${response.statusText}`,
					values: formData
				});
			}

			console.log('✅ Backend response:', json);
			return {
				success: true,
				message: 'AI credential generation launched.',
				values: formData
			};
		} catch (err) {
			console.error('🔥 Uncaught server error:', err);
			return fail(500, {
				error: true,
				message: 'Internal server error',
				values: formData
			});
		}
	}
};
