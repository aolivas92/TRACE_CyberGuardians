import { validateField } from '$lib/validation/fieldValidatorFactory.js';

export function handleInputChange(id, value, formData, fieldErrors, selectedFileRef) {
	if (id === 'wordlist') {
		selectedFileRef.value = value;
		fieldErrors.wordlist = validateField('wordlist', selectedFileRef.value);
	} else {
		formData[id] = value;
		const fieldResult = validateField(id, value);
		fieldErrors[id] = fieldResult;
	}
}

export function validateAllFields(formData, fieldErrors, inputFields, selectedFile) {
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