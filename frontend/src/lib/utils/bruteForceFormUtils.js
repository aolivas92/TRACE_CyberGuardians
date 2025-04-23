import { validateField } from '$lib/validation/fieldValidatorFactory.js';

export function handleInputChange(id, value, formData, fieldErrors) {
	if (id === 'wordlist') {
		fieldErrors.wordlist = validateField('wordlist', value);
		return { selectedFile: value };
	} else {
		formData[id] = value;
		const fieldResult = validateField(id, value);
		fieldErrors[id] = fieldResult;
	}
	return {};
}

export function validateAllFields(inputFields, formData, selectedFile, fieldErrors) {
	let isValid = true;

	inputFields.forEach((field) => {
		const value = formData[field.id];
		const result = validateField(field.id, value);
		fieldErrors[field.id] = result;

		if (field.required && (!value || result.error)) {
			isValid = false;
		}
	});

	const fileResult = validateField('wordlist', selectedFile);
	fieldErrors.wordlist = fileResult;
	if (fileResult.error) {
		isValid = false;
	}

	return isValid;
}