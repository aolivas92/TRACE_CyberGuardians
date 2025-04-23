import { describe, it, expect, vi, beforeEach } from 'vitest';
import { saveCheckpoint, exportResults } from '$test/crawlerRunUtils';

describe('crawlerRunUtils', () => {
	let toast;

	beforeEach(() => {
		localStorage.clear();
		toast = {
			success: vi.fn(),
			error: vi.fn()
		};
	});

	it('saveCheckpoint stores data in localStorage and returns true', () => {
		const jobId = 'abc123';
		const data = [{ url: 'http://example.com' }];
		const result = saveCheckpoint(jobId, data, toast);

		expect(result).toBe(true);
		expect(localStorage.getItem('checkpoint_abc123')).not.toBeNull();
		expect(toast.success).toHaveBeenCalled();
	});

	it('saveCheckpoint returns false if no jobId', () => {
		const result = saveCheckpoint(null, [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No job ID found.');
	});

	it('saveCheckpoint returns false if data is empty', () => {
		const result = saveCheckpoint('abc123', [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No results to checkpoint.');
	});

	it('exportResults returns valid CSV string', async () => {
		const mockFetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({
				results: [{
					url: 'http://example.com',
					parentUrl: '',
					title: 'Home',
					wordCount: 100,
					charCount: 500,
					linksFound: 5,
					error: ''
				}]
			})
		});

		const csv = await exportResults('abc123', mockFetch);
		expect(csv).toContain('URL,Parent URL,Title,Word Count,Character Count,Links Found,Error');
		expect(csv).toContain('"http://example.com"');
	});

	it('exportResults throws if jobId is missing', async () => {
		await expect(() => exportResults(null)).rejects.toThrow('No job ID found');
	});

	it('exportResults throws if fetch fails', async () => {
		const badFetch = vi.fn().mockResolvedValue({ ok: false });
		await expect(() => exportResults('abc123', badFetch)).rejects.toThrow('Failed to fetch crawler results');
	});
});