import { describe, it, expect, vi, beforeEach } from 'vitest';
import { handleInputChange, validateAllFields } from '$test/fuzzerFormUtils';

vi.mock('$lib/validation/fieldValidatorFactory.js', () => ({
	validateField: vi.fn((id, value) => {
		if (id === 'target-url' && (!value || !value.startsWith('http'))) {
			return { error: true, message: 'Invalid URL' };
		}
		if (id === 'wordlist' && !value) {
			return { error: true, message: 'Missing file' };
		}
		return { error: false };
	}),
}));

describe('fuzzerFormUtils', () => {
	let formData;
	let fieldErrors;
	let selectedFileRef;
	let inputFields;

	beforeEach(() => {
		formData = {};
		fieldErrors = {};
		selectedFileRef = { value: null };
		inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'parameters', required: true },
			{ id: 'headers', required: false }
		];
	});

	it('handleInputChange should validate and update formData', () => {
		handleInputChange('target-url', 'http://test.com', formData, fieldErrors, selectedFileRef);
		expect(formData['target-url']).toBe('http://test.com');
		expect(fieldErrors['target-url']).toEqual({ error: false });
	});

	it('handleInputChange should update selectedFileRef when wordlist is selected', () => {
		const fakeFile = new File(['fuzz'], 'wordlist.txt');
		handleInputChange('wordlist', fakeFile, formData, fieldErrors, selectedFileRef);
		expect(selectedFileRef.value).toBe(fakeFile);
		expect(fieldErrors.wordlist).toEqual({ error: false });
	});

	it('validateAllFields returns true when all required fields and file are valid', () => {
		formData['target-url'] = 'http://test.com';
		formData['parameters'] = 'username, password';
		selectedFileRef.value = new File(['payload'], 'fuzz.txt');

		const isValid = validateAllFields(inputFields, formData, fieldErrors, selectedFileRef);
		expect(isValid).toBe(true);
	});

	it('validateAllFields returns false when required field is invalid', () => {
		formData['target-url'] = ''; // invalid
		formData['parameters'] = 'username, password';
		selectedFileRef.value = new File(['payload'], 'fuzz.txt');

		const isValid = validateAllFields(inputFields, formData, fieldErrors, selectedFileRef);
		expect(isValid).toBe(false);
		expect(fieldErrors['target-url'].error).toBe(true);
	});

	it('validateAllFields returns false when wordlist file is missing', () => {
		formData['target-url'] = 'http://test.com';
		formData['parameters'] = 'username, password';
		selectedFileRef.value = null;

		const isValid = validateAllFields(inputFields, formData, fieldErrors, selectedFileRef);
		expect(isValid).toBe(false);
		expect(fieldErrors.wordlist.error).toBe(true);
	});
});