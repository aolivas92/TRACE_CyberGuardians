import { describe, it, expect, vi, beforeEach } from 'vitest';
import { saveCheckpoint, exportResults } from '$test/bruteForceActions';

describe('bruteForceActions', () => {
	beforeEach(() => {
		localStorage.clear();
	});

	it('saveCheckpoint saves data and returns true', () => {
		const mockToast = {
			success: vi.fn(),
			error: vi.fn()
		};

		const jobId = '123';
		const data = [{ id: 1, status: 200 }];
		const result = saveCheckpoint(jobId, data, mockToast);

		expect(result).toBe(true);
		expect(localStorage.getItem('checkpoint_123')).not.toBeNull();
		expect(mockToast.success).toHaveBeenCalled();
	});

	it('saveCheckpoint returns false when jobId is missing', () => {
		const mockToast = { success: vi.fn(), error: vi.fn() };
		const result = saveCheckpoint(null, [], mockToast);

		expect(result).toBe(false);
		expect(mockToast.error).toHaveBeenCalledWith('No job ID found.');
	});

	it('exportResults returns correct CSV', async () => {
		const jobId = 'test-job';
		const mockFetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({
				results: [{ id: 1, url: '/admin', status: 200, payload: 'admin', length: 123, error: '' }]
			})
		});

		const csv = await exportResults(jobId, mockFetch);
		expect(csv).toContain('ID,URL,Status Code,Payload,Length,Error');
		expect(csv).toContain('"/admin"');
	});

	it('exportResults throws if fetch fails', async () => {
		const jobId = 'test-job';
		const mockFetch = vi.fn().mockResolvedValue({ ok: false });

		await expect(() => exportResults(jobId, mockFetch)).rejects.toThrow('Failed to fetch brute force results');
	});
});