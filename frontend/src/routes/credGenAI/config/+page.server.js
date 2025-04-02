import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/validationRules.js';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();

		// Extract wordlist and convert the rest of the form into a serializable object
		const wordlistFile = rawFormData.get('wordlist');
		const allFields = Object.fromEntries(rawFormData.entries());
		delete allFields.wordlist;

		console.log('📥 Received wordlist:', wordlistFile?.name);
		console.log('📦 File size:', wordlistFile?.size);
		console.log('🧾 Form fields:', allFields);

		const fieldErrors = {};

		// Validate the wordlist file
		if (!(wordlistFile instanceof File) || wordlistFile.size === 0) {
			fieldErrors.wordlist = {
				error: true,
				message: 'Please upload a valid wordlist file.'
			};
		} else {
			const result = validateField('wordlist', wordlistFile);
			if (result.error) {
				fieldErrors.wordlist = {
					error: true,
					message: result.message
				};
			}
		}

		// Validate all other fields
		for (const [id, value] of Object.entries(allFields)) {
			const result = validateField(id, value);
			if (result.error) {
				fieldErrors[id] = {
					error: true,
					message: result.message
				};
			}
		}

		// Fail if any validation errors
		if (Object.keys(fieldErrors).length > 0) {
			console.warn('❌ Validation errors in credgenAI:', fieldErrors);
			return fail(400, {
				error: true,
				fieldErrors,
				values: allFields
			});
		}

		// All validations passed
		console.log('✅ All validations passed for credgenAI');
		return {
			success: true,
			values: allFields
		};
	}
};
