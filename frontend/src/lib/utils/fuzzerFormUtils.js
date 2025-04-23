import { validateField } from '$lib/validation/fieldValidatorFactory.js';

export function handleInputChange(id, value, formData, fieldErrors, fileRef) {
	if (id === 'wordlist') {
		fileRef.selectedFile = value;
		fieldErrors.wordlist = validateField('wordlist', value);
	} else {
		formData[id] = value;
		const result = validateField(id, value);
		fieldErrors[id] = result;
	}
}

export function validateAllFields(inputFields, formData, fieldErrors, selectedFile) {
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