import { writable, get } from 'svelte/store';
import { serviceStatus } from './projectServiceStore';

export const scanProgress = writable(0);
export const scanPaused = writable(false);
export const currentService = writable(null);

// Internal flags to prevent duplicate or lingering intervals
let intervalId = null;
let alreadyStopped = false;

/**
 * Starts tracking the scan progress for a specific service.
 * This also sets the service status to "running" and records the start time.
 *
 * @param {string} service - Name of the service being run (e.g., 'crawler').
 */
export function startScanProgress(service) {
	// Prevent starting progress tracking if it's already running
	if (intervalId !== null || get(serviceStatus).status === 'running') return;

	alreadyStopped = false;

	// Set the current active service and reset tracking state
	currentService.set(service);
	scanProgress.set(0);
	scanPaused.set(false);

	// Update the shared service status store
	serviceStatus.set({
		status: 'running',
		serviceType: service,
		startTime: new Date().toISOString()
	});

	console.log('[Scan] Progress simulation started for service:', service);
}

/**
 * Stops tracking the scan progress and resets everything.
 * Optionally marks the service as "complete" if `markComplete` is true.
 *
 * @param {boolean} markComplete - Whether to mark the service as complete instead of idle.
 */
export function stopScanProgress(markComplete = false) {
	// Prevent duplicate stop attempts
	if (alreadyStopped) return;
	alreadyStopped = true;

	// Stop any active interval timer
	if (intervalId) {
		clearInterval(intervalId);
		intervalId = null;
	}

	const service = get(currentService);

	// Update the status based on whether the scan completed or was interrupted
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
