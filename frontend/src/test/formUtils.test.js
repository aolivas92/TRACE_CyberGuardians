import { describe, it, expect, vi, beforeEach } from 'vitest';
import { handleInputChange, validateAllFields } from '$test/formUtils.js';

vi.mock('$lib/validation/fieldValidatorFactory.js', () => ({
	validateField: vi.fn((id, value) => {
		if (id === 'target-url' && !value?.startsWith('http')) {
			return { error: true, message: 'Invalid URL' };
		}
		if (id === 'wordlist' && value == null) {
			return { error: true, message: 'File required' };
		}
		return { error: false };
	}),
}));

describe('Form Utils', () => {
	let formData, fieldErrors, selectedFileRef, inputFields;

	beforeEach(() => {
		formData = {};
		fieldErrors = {};
		selectedFileRef = { value: null };
		inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'attempt-limit', required: true },
		];
	});

	it('handles input change for text field', () => {
		handleInputChange('target-url', 'http://example.com', formData, fieldErrors, selectedFileRef);
		expect(formData['target-url']).toBe('http://example.com');
		expect(fieldErrors['target-url']).toEqual({ error: false });
	});

	it('handles input change for wordlist file', () => {
		const fakeFile = new File(['test'], 'wordlist.txt');
		handleInputChange('wordlist', fakeFile, formData, fieldErrors, selectedFileRef);
		expect(selectedFileRef.value).toBe(fakeFile);
		expect(fieldErrors.wordlist).toEqual({ error: false });
	});

	it('validates all fields correctly', () => {
		formData['target-url'] = 'http://site.com';
		formData['attempt-limit'] = '10';
		const isValid = validateAllFields(formData, fieldErrors, inputFields, new File(['test'], 'wordlist.txt'));
		expect(isValid).toBe(true);
	});
});