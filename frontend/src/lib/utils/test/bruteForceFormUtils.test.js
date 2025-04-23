import { describe, it, expect, vi } from 'vitest';
import { handleInputChange, validateAllFields } from '../bruteForceFormUtils.js';

vi.mock('$lib/validation/fieldValidatorFactory.js', () => ({
    validateField: (id, value) => {
      if (id === 'target-url' && !value?.startsWith('http')) {
        return { error: true, message: 'Invalid URL' };
      }
      if (id === 'attempt-limit' && (value === '' || value == null)) {
        return { error: true, message: 'Attempt limit is required' };
      }
      if (id === 'wordlist' && !value) {
        return { error: true, message: 'File is required' };
      }
      return { error: false, message: '' };
    }
  }));  

describe('bruteForceFormUtils', () => {
	it('should update formData and fieldErrors correctly', () => {
		const formData = {};
		const fieldErrors = {};
		handleInputChange('target-url', 'https://example.com', formData, fieldErrors);

		expect(formData['target-url']).toBe('https://example.com');
		expect(fieldErrors['target-url'].error).toBe(false);
	});

	it('should validate missing required fields', () => {
		const inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'attempt-limit', required: true }
		];
		const formData = {
			'target-url': 'ftp://invalid-url',
			'attempt-limit': ''
		};
		const fieldErrors = {};
		const selectedFile = null;

		const result = validateAllFields(inputFields, formData, selectedFile, fieldErrors);

		expect(result).toBe(false);
		expect(fieldErrors['target-url'].error).toBe(true);
		expect(fieldErrors['attempt-limit'].error).toBe(true);
		expect(fieldErrors['wordlist'].error).toBe(true);
	});

	it('should pass validation with correct data', () => {
		const inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'attempt-limit', required: true }
		];
		const formData = {
			'target-url': 'https://example.com',
			'attempt-limit': '5'
		};
		const selectedFile = new File(["test"], "test.txt", { type: "text/plain" });
		const fieldErrors = {};

		const result = validateAllFields(inputFields, formData, selectedFile, fieldErrors);

		expect(result).toBe(true);
		expect(fieldErrors['target-url'].error).toBe(false);
		expect(fieldErrors['wordlist'].error).toBe(false);
	});
});