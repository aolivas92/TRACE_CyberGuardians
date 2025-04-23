import { describe, it, expect, vi, beforeEach } from 'vitest';
import { handleInputChange, validateAllFields } from '$test/crawlerFormUtils.js';

vi.mock('$lib/validation/fieldValidatorFactory.js', () => ({
	validateField: vi.fn((id, value) => {
		if (id === 'target-url' && !value?.startsWith('http')) {
			return { error: true, message: 'Invalid URL' };
		}
		if (id === 'depth' && isNaN(parseInt(value))) {
			return { error: true, message: 'Depth must be a number' };
		}
		return { error: false };
	}),
}));

describe('crawlerFormUtils', () => {
	let formData;
	let fieldErrors;
	let inputFields;

	beforeEach(() => {
		formData = {};
		fieldErrors = {};
		inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'depth', required: false }
		];
	});

	it('should handle valid input changes correctly', () => {
		handleInputChange('target-url', 'http://example.com', formData, fieldErrors);
		expect(formData['target-url']).toBe('http://example.com');
		expect(fieldErrors['target-url']).toEqual({ error: false });
	});

	it('should handle invalid input changes correctly', () => {
		handleInputChange('target-url', 'ftp://invalid', formData, fieldErrors);
		expect(fieldErrors['target-url']).toEqual({ error: true, message: 'Invalid URL' });
	});

	it('should validate all fields and return true for valid input', () => {
		formData['target-url'] = 'http://example.com';
		formData['depth'] = '5';
		const isValid = validateAllFields(inputFields, formData, fieldErrors);
		expect(isValid).toBe(true);
		expect(fieldErrors['target-url']).toEqual({ error: false });
		expect(fieldErrors['depth']).toEqual({ error: false });
	});

	it('should validate all fields and return false for invalid input', () => {
		formData['target-url'] = 'invalid-url';
		const isValid = validateAllFields(inputFields, formData, fieldErrors);
		expect(isValid).toBe(false);
		expect(fieldErrors['target-url'].error).toBe(true);
	});
});