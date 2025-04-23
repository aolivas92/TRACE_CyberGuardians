import { validateField } from '$lib/validation/fieldValidatorFactory.js';

export function handleInputChange(id, value, formData, fieldErrors) {
	formData[id] = value;
	const result = validateField(id, value);
	fieldErrors[id] = result;
}

export function validateAllFields(inputFields, formData, fieldErrors) {
	let isValid = true;

	inputFields.forEach((field) => {
		const result = validateField(field.id, formData[field.id]);
		fieldErrors[field.id] = result;

		if (field.required && (!formData[field.id] || result.error)) {
			isValid = false;
		}
	});

	return isValid;
}