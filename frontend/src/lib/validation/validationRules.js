/**
 * Validates a target URL
 * @param {string} url - The URL to validate
 * @returns {Object} - Validation result with error flag and message
 */
export function validateTargetUrl(url) {
	if (!url?.trim()) {
		return { error: true, message: 'Target URL is required.' };
	}
	if (!/^https?:\/\/[^\s/$.?#].[^\s]*$/.test(url.trim())) {
		return { error: true, message: 'Please enter a valid URL.' };
	}
	return { error: false, message: '' };
}

/**
 * Validates numeric fields
 * @param {string|number} value - The numeric value to validate
 * @returns {Object} - Validation result with error flag and message
 */
export function validateNumeric(value) {
	if (value && (isNaN(value) || Number(value) < 0)) {
		return { error: true, message: 'Must be a non-negative number' };
	}
	return { error: false, message: '' };
}

/**
 * Validates excluded URLs
 * @param {string} value - Comma-separated list of URLs to validate
 * @returns {Object} - Validation result with error flag and message
 */
export function validateExcludedUrls(value) {
	if (!value) {
		return { error: false, message: '' };
	}

	// Normalize the value by ensuring URLs are comma-separated
	const normalizedValue = value.replace(/(https?:\/\/[^\s,]+)(?=https?:\/\/)/g, '$1,');

	const urls = normalizedValue.split(',').map((u) => u.trim());
	const invalids = urls.filter((url) => !/^https?:\/\/[^\s]+$/.test(url));

	if (invalids.length > 0) {
		return {
			error: true,
			message: 'Each value must be a valid URL starting with http(s)://'
		};
	}

	return { error: false, message: '' };
}

/**
 * Validates a date string
 * @param {string} value - The date string to validate
 * @returns {Object} - Validation result with error flag and message
 */
export function validateDate(value) {
	if (!value) {
		return { error: false, message: '' };
	}

	if (isNaN(Date.parse(value))) {
		return { error: true, message: 'Invalid date format.' };
	}

	return { error: false, message: '' };
}

/**
 * Validates a time string in HH:MM format
 * @param {string} value - The time string to validate
 * @returns {Object} - Validation result with error flag and message
 */
export function validateTime(value) {
	if (!value) {
		return { error: false, message: '' };
	}

	if (!/^\d{2}:\d{2}$/.test(value)) {
		return { error: true, message: 'Time must be in HH:MM format.' };
	}

	return { error: false, message: '' };
}

/**
 * Validates user agent string (no rules yet)
 * @returns {Object} - Validation result with error flag and message
 */
export function validateUserAgent() {
	return { error: false, message: '' };
}

/**
 * Validates the uploaded wordlist file
 * @param {File|null} file - The uploaded file
 * @returns {Object} - Validation result with error flag and message
 */
export function validateWordlistFile(file) {
	if (!file || file.size === 0) {
		return { error: true, message: 'Wordlist file is required.' };
	}

	if (!file.name.endsWith('.txt')) {
		return { error: true, message: 'Only .txt files are supported.' };
	}

	return { error: false, message: '' };
}


/**
 * Validates a length value for username or password fields.
 * It ensures the value is a number, is greater than zero, and is an integer.
 * @param {string|number} value - The length value to validate.
 * @returns {Object} - Validation result with error flag and message.
 */
export function validateLength(value) {
	if (!value) {
		return { error: false, message: '' };
	}
	if (isNaN(Number(value))) {
		return { error: true, message: 'Length must be a number.' };
	}
	if (Number(value) <= 0) {
		return { error: true, message: 'Length must be greater than zero.' };
	}
	if (!Number.isInteger(Number(value))) {
		return { error: true, message: 'Length must be an integer.' };
	}
	return { error: false, message: '' };
}

/**
 * Validates a string of parameters separated by commas.
 * It ensures that the input is not empty, trims whitespace, and checks for valid parameters.
 * @param {string} value - The input string containing parameters separated by commas.
 * @returns {Object} - Validation result with an error flag and a message.
 *                     If validation fails, `error` is true and `message` contains the error description.
 *                     If validation succeeds, `error` is false and `message` is an empty string.
 */
export function validateParameters(value) {
	if (!value?.trim()) {
		return { error: true, message: 'At least one parameter is required.' };
	}

	const params = value
		.split(',')
		.map((p) => p.trim())
		.filter(Boolean);
	if (params.length === 0) {
		return { error: true, message: 'Please provide valid parameters.' };
	}

	return { error: false, message: '' };
}

/**
 * Validates the headers input field.
 * Ensures the string follows a basic "key: value" format.
 * Empty values are considered valid since the field is optional.
 *
 * @param {string} value - The header string to validate.
 * @returns {Object} - Validation result with error flag and message.
 */
export function validateHeaders(value) {
	if (!value?.trim()) return { error: false, message: '' }; // optional

	// Basic check for key-value format
	if (!/^[^:]+:\s?.+/.test(value)) {
		return {
			error: true,
			message: 'Header must be in key: value format.'
		};
	}

	return { error: false, message: '' };
}

/**
 * Validates the proxy input field.
 * Ensures the string is a properly formatted HTTP or HTTPS URL.
 * Empty values are allowed since this field is optional.
 *
 * @param {string} value - The proxy URL to validate.
 * @returns {Object} - Validation result with error flag and message.
 */
export function validateProxy(value) {
	if (!value?.trim()) return { error: false, message: '' }; // optional

	if (!/^https?:\/\/[^\s]+$/.test(value)) {
		return { error: true, message: 'Proxy must be a valid http/https URL.' };
	}

	return { error: false, message: '' };
}

/**
 * Validates the body template field used for POST requests.
 * Ensures that the template includes the "payload" keyword as a placeholder.
 * Returns an error if "payload" is not found. Empty values are allowed.
 *
 * @param {string} value - The body template string to validate.
 * @returns {Object} - Validation result with error flag and message.
 */
export function validateBodyTemplate(value) {
	if (!value?.trim()) return { error: false, message: '' }; // optional

	// Basic heuristic: should contain payload placeholders
	if (!value.includes('payload')) {
		return {
			error: true,
			message: 'Template must include "payload" placeholders.'
		};
	}

	return { error: false, message: '' };
}

/**
 * Factory function to validate a field based on its ID
 * @param {string} id - The field ID
 * @param {*} value - The field value
 * @returns {Object} - Validation result with error flag and message
 */
export function validateField(id, value) {
	switch (id) {
		case 'target-url':
			return validateTargetUrl(value);

		case 'depth':
		case 'max-pages':
		case 'delay':
			return validateNumeric(value);

		case 'excluded-urls':
			return validateExcludedUrls(value);

		case 'crawl-date':
			return validateDate(value);

		case 'crawl-time':
			return validateTime(value);

		case 'user-agent':
			return validateUserAgent();

		case 'wordlist':
			return validateWordlistFile(value);

		case 'proxy':
			return validateProxy(value);

		case 'headers':
			return validateHeaders(value);

		case 'parameters':
			return validateParameters(value);

		case 'body-template':
			return validateBodyTemplate(value);

		case 'username-length':
		case 'password-length':
			return validateLength(value);

		default:
			return { error: false, message: '' };
	}
}
