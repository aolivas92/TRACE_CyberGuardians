import { validateField } from '$lib/validation/fieldValidatorFactory.js';

/**
 * Updates formData and fieldErrors when an input changes.
 */
export function handleInputChange(id, value, formData, fieldErrors) {
	formData[id] = value;
	const result = validateField(id, value);
	fieldErrors[id] = result;
}

/**
 * Validates all fields and updates fieldErrors accordingly.
 */
export function validateAllFields(inputFields, formData, fieldErrors) {
	let isValid = true;

	inputFields.forEach((field) => {
		const value = formData[field.id];
		const result = validateField(field.id, value);
		fieldErrors[field.id] = result;

		if (field.required && (!value || result.error)) {
			isValid = false;
		}
	});

	return isValid;
}