// src/lib/services/crawlerSocket.js
import { serviceStatus } from '$lib/stores/projectServiceStore';
import { scanProgress, stopScanProgress, isRealProgress, startScanProgress } from '$lib/stores/scanProgressStore';
import { serviceResults } from '$lib/stores/serviceResultsStore.js';

let socket = null;

export function connectToCrawlerWebSocket(jobId, retry = 0) {
	const maxRetries = 5;

	// Prevent duplicate connections
	if (socket && socket.readyState !== WebSocket.CLOSED) {
		console.warn('[WebSocket] Already connected. Skipping duplicate connection.');
		return;
	}

	socket = new WebSocket(`ws://localhost:8000/ws/crawler/${jobId}`);

	socket.onopen = () => {
		console.log('[WebSocket] Connected to crawler job:', jobId);
	};

	socket.onmessage = (event) => {
		const message = JSON.parse(event.data);
		const { type, data } = message;

		switch (type) {
			case 'status':
				if (data.status === 'running') {
					startScanProgress('crawler');
				}
				serviceStatus.set({
					status: data.status === 'completed' ? 'complete' : data.status,
					serviceType: 'crawler',
					startTime: data.started_at || new Date().toISOString()
				});
				break;

			case 'new_row':
				serviceResults.update((r) => ({
					...r,
					crawler: [...r.crawler, data.row]
				}));
				break;

			case 'progress':
				isRealProgress.set(true);
				scanProgress.set(Math.min(data.progress, 99));
				break;

			case 'complete':
				scanProgress.set(100);
				stopScanProgress(true);
				serviceStatus.set({
					status: 'complete',
					serviceType: 'crawler',
					startTime: null
				});
				break;

			case 'error':
				serviceStatus.set({
					status: 'idle',
					serviceType: null,
					startTime: null
				});
				console.error('[Crawler Error]', data.message);
				break;

			case 'log':
				console.log(`[Crawler Log] ${data.message}`);
				break;
		}
	};

	socket.onerror = (e) => {
		console.error('[WebSocket Error]', e);

		if (retry < maxRetries) {
			console.log(`[WebSocket] Retrying connection (${retry + 1}/${maxRetries})...`);
			setTimeout(() => connectToCrawlerWebSocket(jobId, retry + 1), 1000);
		}
	};

	socket.onclose = () => {
		console.log('[WebSocket] Connection closed');
		socket = null;
	};
}

export function closeCrawlerWebSocket() {
	if (socket) {
		socket.close();
		socket = null;
	}
}
