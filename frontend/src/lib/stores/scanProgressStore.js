import { writable, get } from 'svelte/store';
import { serviceStatus } from './projectServiceStore';

export const scanProgress = writable(0);
export const scanPaused = writable(false);
export const currentService = writable(null);
export const isRealProgress = writable(false);

let intervalId = null;
let alreadyStopped = false;

export function startScanProgress(service) {
	if (intervalId !== null || get(serviceStatus).status === 'running') return;
	alreadyStopped = false;

	currentService.set(service);
	scanProgress.set(0);
	scanPaused.set(false);
	isRealProgress.set(false); // assume fake until proven otherwise

	serviceStatus.set({
		status: 'running',
		serviceType: service,
		startTime: new Date().toISOString()
	});

	intervalId = setInterval(() => {
		if (get(scanPaused) || get(isRealProgress)) return; // ✅ Don't simulate if real data

		scanProgress.update((val) => {
			if (val < 99) {
				const increment = [3, 5, 10][Math.floor(Math.random() * 3)];
				return Math.min(val + increment, 99);
			}
			return val;
		});
	}, 500);
}

export function togglePause() {
	scanPaused.update((val) => !val);
}


export function stopScanProgress(markComplete = false) {
	if (alreadyStopped) return;
	alreadyStopped = true;

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
		scanProgress.set(0);
	}

	console.log('[Scan] Progress simulation stopped');
	scanPaused.set(false);
	currentService.set(null);
}


