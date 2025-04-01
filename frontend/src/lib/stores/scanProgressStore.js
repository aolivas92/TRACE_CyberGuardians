import { writable } from 'svelte/store';
import { serviceStatus } from './projectServiceStore';

export const scanProgress = writable(0);
export const scanPaused = writable(false);

let intervalId = null;

export function startScanProgress() {
	if (intervalId !== null) return;

	intervalId = setInterval(() => {
		let isPaused;
		scanPaused.subscribe((v) => (isPaused = v))();

		if (isPaused) return; // Don't increment if paused

		scanProgress.update((value) => {
			if (value < 100) {
				const increment = [3, 5, 10][Math.floor(Math.random() * 3)];
				const next = Math.min(value + increment, 100);

				if (next >= 100) {
					clearInterval(intervalId);
					intervalId = null;

					serviceStatus.set({
						status: 'complete',
						serviceType: 'crawler',
						startTime: null
					});
				}
				return next;
			}
			return value;
		});
	}, 500);
}

export function stopScanProgress() {
	if (intervalId) clearInterval(intervalId);
	intervalId = null;
	scanProgress.set(0);
	scanPaused.set(false);
}
