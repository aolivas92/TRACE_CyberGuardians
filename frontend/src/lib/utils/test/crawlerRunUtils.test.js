import { describe, it, expect, vi } from 'vitest';
import { saveCrawlerCheckpoint, buildCrawlerCsv } from '../crawlerRunUtils';

describe('crawlerRunUtils', () => {
	it('should not save checkpoint without jobId', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const result = saveCrawlerCheckpoint(null, [{ url: 'x' }], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No job ID found.');
	});

	it('should not save checkpoint if data is empty', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const result = saveCrawlerCheckpoint('abc123', [], toast);
		expect(result).toBe(false);
		expect(toast.error).toHaveBeenCalledWith('No results to checkpoint.');
	});

	it('should save checkpoint when valid jobId and data are provided', () => {
		const toast = { error: vi.fn(), success: vi.fn() };
		const setItemSpy = vi.spyOn(localStorage.__proto__, 'setItem');
		const jobId = 'abc123';
		const data = [{ url: 'http://example.com', title: 'Home' }];

		const result = saveCrawlerCheckpoint(jobId, data, toast);
		expect(result).toBe(true);
		expect(setItemSpy).toHaveBeenCalledWith(`checkpoint_${jobId}`, JSON.stringify(data));
		expect(toast.success).toHaveBeenCalled();
	});

	it('should build correct CSV from crawler results', () => {
		const results = [
			{
				url: 'http://test.com',
				parentUrl: 'http://home.com',
				title: 'Test Page',
				wordCount: 100,
				charCount: 500,
				linksFound: 5,
				error: null
			}
		];

		const csv = buildCrawlerCsv(results);
		expect(csv.startsWith('URL,Parent URL,Title')).toBe(true);
		expect(csv).toContain('"http://test.com"');
		expect(csv).toContain('"Test Page"');
		expect(csv).toContain('100');
	});
});