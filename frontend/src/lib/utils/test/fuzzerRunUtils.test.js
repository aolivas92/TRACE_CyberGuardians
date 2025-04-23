import { describe, it, expect, vi } from 'vitest';
import { saveFuzzerCheckpoint, buildFuzzerCsv } from '../fuzzerRunUtils';

describe('fuzzerRunUtils', () => {
	it('should not save checkpoint without jobId', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const result = saveFuzzerCheckpoint(null, [{ id: 1 }], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No job ID found.');
	});

	it('should not save checkpoint if data is empty', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const result = saveFuzzerCheckpoint('abc123', [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No results to checkpoint.');
	});

	it('should save checkpoint when valid data and jobId are given', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const setItem = vi.spyOn(localStorage.__proto__, 'setItem');
		const jobId = 'abc123';
		const data = [{ id: 1, payload: 'admin' }];

		const result = saveFuzzerCheckpoint(jobId, data, toast);
		expect(result).toBe(true);
		expect(setItem).toHaveBeenCalledWith(`checkpoint_${jobId}`, JSON.stringify(data));
		expect(toast.success).toHaveBeenCalled();
	});

	it('should build correct CSV string from fuzzer results', () => {
		const input = [
			{ id: 1, response: 200, payload: 'admin', length: 123, error: null },
			{ id: 2, response: 500, payload: 'root', length: 456, error: 'Server Error' }
		];
		const csv = buildFuzzerCsv(input);

		expect(csv.startsWith('ID,Response,Payload,Length,Error')).toBe(true);
		expect(csv).toContain('"admin"');
		expect(csv).toContain('"Server Error"');
		expect(csv).toContain('456');
	});
});