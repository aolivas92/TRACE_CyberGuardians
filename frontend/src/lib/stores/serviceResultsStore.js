// src/lib/stores/serviceResultsStore.js
import { writable } from 'svelte/store';

export const serviceResults = writable({
	crawler: [],
});
