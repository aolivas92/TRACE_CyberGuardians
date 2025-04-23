import { describe, it, expect, vi } from 'vitest';
import { handleInputChange, validateAllFields } from '../fuzzerFormUtils';

vi.mock('$lib/validation/fieldValidatorFactory.js', () => ({
	validateField: (id, value) => {
		if (id === 'target-url' && (!value || !value.startsWith('http'))) {
			return { error: true, message: 'Invalid URL' };
		}
		if (id === 'parameters' && (!value || value.trim() === '')) {
			return { error: true, message: 'Parameters required' };
		}
		if (id === 'wordlist' && !value) {
			return { error: true, message: 'Wordlist is required' };
		}
		return { error: false, message: '' };
	}
}));

describe('fuzzerFormUtils', () => {
	it('should update formData and validate input change for text field', () => {
		const formData = {};
		const fieldErrors = {};
		const fileRef = { selectedFile: null };

		handleInputChange('target-url', 'https://site.com', formData, fieldErrors, fileRef);

		expect(formData['target-url']).toBe('https://site.com');
		expect(fieldErrors['target-url'].error).toBe(false);
	});

	it('should validate and store selected file for wordlist', () => {
		const formData = {};
		const fieldErrors = {};
		const fileRef = { selectedFile: null };

		const mockFile = new File(['test'], 'test.txt', { type: 'text/plain' });
		handleInputChange('wordlist', mockFile, formData, fieldErrors, fileRef);

		expect(fileRef.selectedFile).toBe(mockFile);
		expect(fieldErrors['wordlist'].error).toBe(false);
	});

	it('should return false if required fields or wordlist are invalid', () => {
		const inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'parameters', required: true }
		];
		const formData = { 'target-url': '', 'parameters': '' };
		const fieldErrors = {};
		const selectedFile = null;

		const result = validateAllFields(inputFields, formData, fieldErrors, selectedFile);

		expect(result).toBe(false);
		expect(fieldErrors['target-url'].error).toBe(true);
		expect(fieldErrors['parameters'].error).toBe(true);
		expect(fieldErrors['wordlist'].error).toBe(true);
	});

	it('should return true if all required fields and wordlist are valid', () => {
		const inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'parameters', required: true }
		];
		const formData = {
			'target-url': 'https://example.com',
			'parameters': 'username,password'
		};
		const fieldErrors = {};
		const selectedFile = new File(['test'], 'payload.txt', { type: 'text/plain' });

		const result = validateAllFields(inputFields, formData, fieldErrors, selectedFile);

		expect(result).toBe(true);
		expect(fieldErrors['wordlist'].error).toBe(false);
	});
});