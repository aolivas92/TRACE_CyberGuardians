import { writable } from 'svelte/store';
import { serviceStatus } from './projectServiceStore';

export const scanProgress = writable(0);
export const scanPaused = writable(false);
export const crawlerResults = writable([]);
export const crawlerLogs = writable([]);
export const jobId = writable(null);

let intervalId = null;
let socket = null;

export function startScanProgress(currentJobId) {
	if (intervalId !== null) return;
	jobId.set(currentJobId);

	// Connect to WebSocket if job ID provided
	if (currentJobId) {
		connectWebSocket(currentJobId);
	} else {
		// Fallback to mock progress for testing
		startMockProgress();
	}
}

function startMockProgress() {
	// For the mock progress, we'll mimic the backend behavior
	// Random duration between 10-30 seconds to reach 99%
	const duration = Math.random() * 20000 + 10000; // 10-30 seconds in milliseconds
	const startTime = Date.now();
	let lastUpdateTime = 0;
	
	console.log(`Mock progress will take ${duration/1000} seconds to reach 99%`);
	
	intervalId = setInterval(() => {
		let isPaused;
		scanPaused.subscribe((v) => (isPaused = v))();

		if (isPaused) return; // Don't increment if paused

		const elapsed = Date.now() - startTime;
		
		scanProgress.update((value) => {
			// Only update if we haven't reached 100%
			if (value < 100) {
				// Calculate percentage based on elapsed time, capping at 99%
				if (elapsed >= duration) {
					// Let it sit at 99% for a bit before completing
					if (Date.now() - lastUpdateTime > 3000) {
						// After 3 seconds at 99%, complete the job
						clearInterval(intervalId);
						intervalId = null;
						
						serviceStatus.set({
							status: 'complete',
							serviceType: 'crawler',
							startTime: null
						});
						
						// Return 100% as the final value
						return 100;
					}
					return 99;
				} else {
					// Smooth progress calculation from 0% to 99%
					const progress = Math.min(Math.floor((elapsed / duration) * 99), 99);
					lastUpdateTime = progress === 99 ? Date.now() : lastUpdateTime;
					return progress;
				}
			}
			return value;
		});
	}, 200); // Update more frequently for smoother animation
}

function connectWebSocket(id) {
	if (socket) {
		socket.close();
	}

	const wsUrl = `ws://127.0.0.1:8000/ws/crawler/${id}`;
	console.log('🔌 Connecting to WebSocket:', wsUrl);
	socket = new WebSocket(wsUrl);

	socket.onopen = () => {
		console.log('🟢 WebSocket connected for job:', id);
		// Request logs when connection opens
		const command = { type: 'command', command: 'get_logs' };
		console.log('📤 Sending command:', command);
		socket.send(JSON.stringify(command));
	};

	socket.onmessage = (event) => {
		try {
			const data = JSON.parse(event.data);
			console.log('📥 WebSocket message received:', data);
			
			if (data.type === 'status') {
				// Update status and progress
				console.log(`ℹ️ Status update: ${data.data.status} (${data.data.progress || 0}%)`);
				scanProgress.set(data.data.progress || 0);
				
				if (data.data.status === 'completed' || data.data.progress === 100) {
					console.log('✅ Job completed based on status message');
					serviceStatus.set({
						status: 'complete',
						serviceType: 'crawler',
						startTime: null
					});
					
					// Fetch full results when completed
					fetchCrawlerResults(id);
				}
			} else if (data.type === 'progress') {
				// Handle progress updates specifically
				scanProgress.set(data.data.progress || 0);
				console.log(`📊 Progress update: ${data.data.progress}% (${data.data.urls_processed}/${data.data.total_urls} URLs)`);
				
				if (data.data.progress >= 100) {
					console.log('✅ Job completed based on progress');
					serviceStatus.set({
						status: 'complete',
						serviceType: 'crawler',
						startTime: null
					});
				}
			} else if (data.type === 'complete') {
				// Handle job completion
				console.log('🏁 Crawler job completed successfully!');
				scanProgress.set(100);
				serviceStatus.set({
					status: 'complete',
					serviceType: 'crawler',
					startTime: null
				});
				
				// Fetch full results
				fetchCrawlerResults(id);
			} else if (data.type === 'logs') {
				// Update logs
				console.log(`📝 Received ${data.data.logs?.length || 0} log entries`);
				crawlerLogs.set(data.data.logs || []);
			} else if (data.type === 'log') {
				// Handle individual log messages
				console.log(`📄 Log: ${data.data.message}`);
				crawlerLogs.update(logs => [...logs, data.data.message]);
			} else if (data.type === 'error') {
				console.error('❌ WebSocket error:', data.data.message);
			}
		} catch (e) {
			console.error('🔥 Error parsing WebSocket message:', e);
		}
	};

	socket.onclose = () => {
		console.log(`🔴 WebSocket disconnected for job: ${id}`);
	};

	socket.onerror = (error) => {
		console.error('⚠️ WebSocket error:', error);
	};
}

async function fetchCrawlerResults(id) {
	console.log('🔄 Fetching final crawler results for job:', id);
	try {
		const response = await fetch(`http://127.0.0.1:8000/api/crawler/${id}/results`);
		if (response.ok) {
			const data = await response.json();
			console.log(`📊 Received ${data.results?.length || 0} crawler results`);
			crawlerResults.set(data.results || []);
		} else {
			console.warn('⚠️ Failed to fetch results:', response.status, response.statusText);
		}
	} catch (e) {
		console.error('🔥 Error fetching crawler results:', e);
	}
}

export function stopScanProgress() {
	if (intervalId) {
		clearInterval(intervalId);
		intervalId = null;
	}
	
	if (socket) {
		socket.close();
		socket = null;
	}
	
	scanProgress.set(0);
	scanPaused.set(false);
	jobId.set(null);
}
