import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/validationRules.js';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();

		// Separate out the wordlist file
		const wordlist = rawFormData.get('wordlist');
		const formData = Object.fromEntries(rawFormData.entries());

		// Avoid serialization issues by excluding file from returned data
		delete formData.wordlist;

    console.log('📥 Received wordlist:', wordlist?.name);
		console.log('📦 File size:', wordlist?.size);
		console.log('🧾 Form fields:', formData);

		const fieldErrors = {};

		// Validate non-file fields
		for (const [id, value] of Object.entries(formData)) {
			const result = validateField(id, value);
			if (result.error) {
				fieldErrors[id] = { error: true, message: result.message };
			}
		}

		// Validate wordlist file
		const fileValidation = validateField('wordlist', wordlist);
		if (fileValidation.error) {
			fieldErrors.wordlist = {
				error: true,
				message: fileValidation.message
			};
		}

		// Additional required field checks (in case validation missed them)
		const requiredFields = ['target-url', 'parameters'];
		for (const field of requiredFields) {
			if (!formData[field]) {
				fieldErrors[field] = {
					error: true,
					message: `${field.replace('-', ' ')} is required.`
				};
			}
		}

		// Stop and report all validation errors
		if (Object.keys(fieldErrors).length > 0) {
			console.warn('❌ Validation errors:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: formData
			});
		}

		// All validations passed — prepare backend form
		const fuzzerPayload = new FormData();
		fuzzerPayload.append('target_url', formData['target-url']);
		fuzzerPayload.append('parameters', formData['parameters']);
		fuzzerPayload.append('wordlist', wordlist);

		if (formData['headers']) fuzzerPayload.append('headers', formData['headers']);
		if (formData['proxy']) fuzzerPayload.append('proxy', formData['proxy']);
		if (formData['body-template']) fuzzerPayload.append('body_template', formData['body-template']);

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
