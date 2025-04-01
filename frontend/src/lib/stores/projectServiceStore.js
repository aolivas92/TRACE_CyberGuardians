import { writable } from 'svelte/store';

export const serviceStatus = writable({
  running: false,
  serviceType: 'crawler',
  startTime: null,
});
