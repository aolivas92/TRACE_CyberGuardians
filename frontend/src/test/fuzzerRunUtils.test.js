import { describe, it, expect, vi, beforeEach } from 'vitest';
import { saveCheckpoint, exportFuzzerResults } from '$test/fuzzerRunUtils';

describe('fuzzerRunUtils', () => {
	let toast;

	beforeEach(() => {
		localStorage.clear();
		toast = {
			success: vi.fn(),
			error: vi.fn()
		};
	});

	it('saves checkpoint to localStorage and returns true', () => {
		const jobId = 'abc123';
		const data = [{ id: 1, payload: 'test' }];
		const result = saveCheckpoint(jobId, data, toast);

		expect(result).toBe(true);
		expect(localStorage.getItem(`checkpoint_${jobId}`)).toContain('test');
		expect(toast.success).toHaveBeenCalled();
	});

	it('returns false if no job ID is provided', () => {
		const result = saveCheckpoint(null, [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No job ID found.');
	});

	it('returns false if data is empty', () => {
		const result = saveCheckpoint('abc123', [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No results to checkpoint.');
	});

	it('exports fuzzer results as CSV', async () => {
		const mockFetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({
				results: [{ id: 1, response: '200 OK', payload: 'admin', length: 100, error: '' }]
			})
		});

		const csv = await exportFuzzerResults('job123', mockFetch);
		expect(csv).toContain('ID,Response,Payload,Length,Error');
		expect(csv).toContain('"admin"');
	});

	it('throws if no job ID is provided', async () => {
		await expect(() => exportFuzzerResults(null)).rejects.toThrow('No job ID found.');
	});

	it('throws if fetch fails', async () => {
		const badFetch = vi.fn().mockResolvedValue({ ok: false });
		await expect(() => exportFuzzerResults('job123', badFetch)).rejects.toThrow('Failed to fetch fuzzer results.');
	});
});