import { fail } from '@sveltejs/kit';
import { validateField } from '$lib/validation/validationRules.js';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const rawFormData = await request.formData();
		const wordlistFile = rawFormData.get("wordlist");

		// ✅ DEBUG: log what you’re receiving
		console.log("🧾 wordlistFile:", wordlistFile);
		console.log("📏 file size:", wordlistFile?.size);
		console.log("wordlistFile instanceof File:", wordlistFile instanceof File);

		const formData = Object.fromEntries(rawFormData.entries());
		delete formData.wordlist; // prevent File object from being returned

		const errors = [];

		if (!wordlistFile || !(wordlistFile instanceof File) || wordlistFile.size === 0) {
			console.warn("❌ No file received or file is empty.");
			return fail(400, {
				error: true,
				message: "Please upload a valid wordlist file.",
				values: formData
			});
		}

		// ✅ Validate the file
		const wordlistValidation = validateField("wordlist", wordlistFile);
		if (wordlistValidation.error) {
			return fail(400, {
				error: true,
				fieldErrors: {
					wordlist: {
						error: true,
						message: wordlistValidation.message
					}
				},
				values: formData
			});
		}		

		// (Optional) validate other fields
		for (const [id, value] of Object.entries(formData)) {
			const { error, message } = validateField(id, value);
			if (error) {
				errors.push(`${id}: ${message}`);
			}
		}

		// ❌ Fail early if any errors
		if (errors.length > 0) {
			console.warn("❌ Validation errors:", errors);
			return fail(400, {
				error: true,
				fieldErrors: {
					wordlist: {
						error: true,
						message: "Wordlist is required."
					}
				},
				values: formData
			});
		}

		// ✅ Only return success if valid
		console.log("✅ All validations passed — redirect OK");
		return {
			success: true,
			values: formData
		};
	}
};