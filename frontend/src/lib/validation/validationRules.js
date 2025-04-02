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
		case 'proxy':
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

		case 'username-length':
		case 'password-length':
			return validateLength(value);

		default:
			return { error: false, message: '' };
	}
}
