import { writable, get } from 'svelte/store';
import { serviceStatus } from './projectServiceStore';

export const scanProgress = writable(0);
export const scanPaused = writable(false);
export const currentService = writable(null);

let intervalId = null;

export function startScanProgress(service) {
	// If something is already running, don't start a new one
	if (intervalId !== null || get(serviceStatus).status === 'running') return;

	currentService.set(service);
	scanProgress.set(0);
	scanPaused.set(false);

	// Set service as running
	serviceStatus.set({
		status: 'running',
		serviceType: service,
		startTime: new Date().toISOString()
	});

	intervalId = setInterval(() => {
		if (get(scanPaused)) return;

		scanProgress.update((val) => {
			if (val < 100) {
				const increment = [3, 5, 10][Math.floor(Math.random() * 3)];
				const next = Math.min(val + increment, 100);

				if (next >= 100) {
					stopScanProgress(true);
				}
				return next;
			}
			return val;
		});
	}, 500);
}

export function togglePause() {
	scanPaused.update((val) => !val);
}

export function stopScanProgress(markComplete = false) {
	if (intervalId) {
		clearInterval(intervalId);
		intervalId = null;
	}

	const service = get(currentService);

	if (markComplete && service) {
		serviceStatus.set({
			status: 'complete',
			serviceType: service,
			startTime: null
		});
	} else {
		serviceStatus.set({
			status: 'idle',
			serviceType: null,
			startTime: null
		});
	}

	scanProgress.set(0);
	scanPaused.set(false);
	currentService.set(null);
}

