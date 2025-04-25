import { describe, it, expect, vi } from 'vitest';
import { saveCheckpointForJob, createCsvContent } from '../bruteForceRunUtils';

describe('bruteForceRunUtils', () => {
	it('should return false and show error when jobId is missing', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const result = saveCheckpointForJob(null, [{ id: 1 }], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No job ID found.');
	});

	it('should return false and show error when data is empty', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const result = saveCheckpointForJob('abc123', [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No results to checkpoint.');
	});

	it('should save data to localStorage and return true when valid', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const jobId = 'abc123';
		const data = [{ id: 1, url: 'http://test.com', status: 200 }];

		const setItem = vi.spyOn(localStorage.__proto__, 'setItem');
		const result = saveCheckpointForJob(jobId, data, toast);

		expect(result).toBe(true);
		expect(setItem).toHaveBeenCalledWith(`checkpoint_${jobId}`, JSON.stringify(data));
		expect(toast.success).toHaveBeenCalled();
	});

	it('should create CSV content from result data', () => {
        const input = [
            { id: 1, url: 'http://example.com', status: 200, payload: 'admin', length: 123, error: null },
            { id: 2, url: 'http://test.com', status: 404, payload: 'login', length: 456, error: 'Not Found' }
        ];
    
        const csv = createCsvContent(input);
        expect(csv).toContain('"admin"');
        expect(csv).toContain('"login"');
        expect(csv).toContain('404');
        expect(csv.startsWith('ID,URL,Status Code')).toBe(true);
    });    
});