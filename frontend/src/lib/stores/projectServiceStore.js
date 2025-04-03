import { writable } from 'svelte/store';

function createServiceStatusStore() {
	const stored = typeof localStorage !== 'undefined' ? localStorage.getItem('serviceStatus') : null;

	// Define the initial state
	const defaultState = {
		status: 'idle', // "idle" | "running" | "complete"
		serviceType: null,
		startTime: null
	};

	// Use stored value if available, otherwise use default
	const initial = stored ? JSON.parse(stored) : defaultState;

	// Create the store with initial value
	const store = writable(initial);

	// Subscribe to changes and update localStorage
	store.subscribe((value) => {
		if (typeof localStorage !== 'undefined') {
			console.log('[Store] serviceStatus changed:', value);
			localStorage.setItem('serviceStatus', JSON.stringify(value));
		}
	});

	// Add a reset method to clear the store state
	const reset = () => {
		store.set(defaultState);
	};

	return {
		...store,
		reset
	};
}

export const serviceStatus = createServiceStatusStore();
