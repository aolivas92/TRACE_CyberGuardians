import { writable } from 'svelte/store';

function createServiceStatusStore() {
	const stored = typeof localStorage !== 'undefined' ? localStorage.getItem('serviceStatus') : null;

	const initial = stored
		? JSON.parse(stored)
		: {
				status: 'idle', // "idle" | "running" | "complete"
				serviceType: null,
				startTime: null
			};

	const store = writable(initial);

	store.subscribe((value) => {
		if (typeof localStorage !== 'undefined') {
			localStorage.setItem('serviceStatus', JSON.stringify(value));
			console.log('[Store] serviceStatus changed:', value);
		}
	});

	return store;
}

export const serviceStatus = createServiceStatusStore();
