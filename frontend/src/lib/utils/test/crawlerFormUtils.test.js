import { describe, it, expect, vi } from 'vitest';
import { handleInputChange, validateAllFields } from '../crawlerFormUtils';

vi.mock('$lib/validation/fieldValidatorFactory.js', () => ({
	validateField: (id, value) => {
		if (id === 'target-url' && (!value || !value.startsWith('http'))) {
			return { error: true, message: 'Invalid URL' };
		}
		if (id === 'depth' && (value === '' || value === null)) {
			return { error: true, message: 'Depth required' };
		}
		return { error: false, message: '' };
	}
}));

describe('crawlerFormUtils', () => {
	it('should handle input change and validate field', () => {
		const formData = {};
		const fieldErrors = {};
		handleInputChange('target-url', 'http://example.com', formData, fieldErrors);

		expect(formData['target-url']).toBe('http://example.com');
		expect(fieldErrors['target-url'].error).toBe(false);
	});

	it('should fail validation if required field is empty or invalid', () => {
		const inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'depth', required: true }
		];
		const formData = { 'target-url': '', 'depth': null };
		const fieldErrors = {};

		const result = validateAllFields(inputFields, formData, fieldErrors);
		expect(result).toBe(false);
		expect(fieldErrors['target-url'].error).toBe(true);
		expect(fieldErrors['depth'].error).toBe(true);
	});

	it('should pass validation if all required fields are valid', () => {
		const inputFields = [
			{ id: 'target-url', required: true },
			{ id: 'depth', required: true }
		];
		const formData = {
			'target-url': 'https://juice-shop.herokuapp.com',
			'depth': '5'
		};
		const fieldErrors = {};

		const result = validateAllFields(inputFields, formData, fieldErrors);
		expect(result).toBe(true);
		expect(fieldErrors['target-url'].error).toBe(false);
		expect(fieldErrors['depth'].error).toBe(false);
	});
});