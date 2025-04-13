import { serviceStatus } from '$lib/stores/projectServiceStore';
import { scanProgress, stopScanProgress, startScanProgress, scanPaused} from '$lib/stores/scanProgressStore';
import { serviceResults } from '$lib/stores/serviceResultsStore.js';
import { get } from 'svelte/store';

let socket = null;

/**
 * Establishes a WebSocket connection to the backend credGenAI using the job ID.
 * Automatically retries connection if it fails (up to maxRetries).
 */
export function connectToCredGenAIWebSocket(jobId, retry = 0) {
  const maxRetries = 5;

  // Prevent duplicate connections if one is already open
  if (socket && socket.readyState !== WebSocket.CLOSED) {
    console.warn('[WebSocket] Already connected. Skipping duplicate connection.');
    return;
  }

  // Open a WebSocket connection to the backend endpoint
  socket = new WebSocket(`ws://localhost:8000/ws/credGenAI/${jobId}`);

  // Triggered when the connection is successfully established
  socket.onopen = () => {
    console.log('[WebSocket] Connected to credGenAI job:', jobId);
  };

  // Triggered whenever a message is received from the backend
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    const { type, data } = message;

    switch (type) {
      // Updates job status in the serviceStatus store
      case 'status': {
        const mappedStatus = data.status;
        switch (mappedStatus) {
          case 'complete': {
            break;
          }
          case 'paused': {
            scanPaused.set(true);
            break;
          }
          case 'running': {
            scanPaused.set(false);
            break;
          }
        }
      
        serviceStatus.set({
          status: mappedStatus,
          serviceType: 'credGenAI',
          startTime: data.started_at || new Date().toISOString()
        });
        break;
      }
      
      // Updates the credGenAI result table with a new scanned row
      case 'new_row':
        serviceResults.update((r) => ({
          ...r,
          credGenAI: [...r.credGenAI, data.row]
        }));
        break;

      // Updates the progress of the credGenAI job
      case 'progress':
        if (!get(scanPaused)) {
          startScanProgress('credGenAI');
          scanProgress.set(Math.min(data.progress, 99));
        }
        break;

      // Marks the scan as complete and finalizes UI
      case 'complete':
        scanProgress.set(100);
        stopScanProgress(true);
        serviceStatus.set({
          status: 'complete',
          serviceType: 'credGenAI',
          startTime: null
        });
        break;

      // Handles errors and resets UI state
      case 'error':
        serviceStatus.set({
          status: 'idle',
          serviceType: null,
          startTime: null
        });
        console.error('[CredGenAI Error]', data.message);
        break;

      // Logs backend messages to console for debugging
      case 'log':
        console.log(`[CredGenAI Log] ${data.message}`);
        break;
    }
  };

  // Handles WebSocket connection errors and retries if needed
  socket.onerror = (e) => {
    console.error('[WebSocket Error]', e);

    if (retry < maxRetries) {
      console.log(`[WebSocket] Retrying connection (${retry + 1}/${maxRetries})...`);
      setTimeout(() => connectToCredGenAIWebSocket(jobId, retry + 1), 1000);
    }
  };

  // Cleans up socket reference when connection is closed
  socket.onclose = () => {
    console.log('[WebSocket] Connection closed');
    socket = null;
  };
}

/**
 * Manually closes the WebSocket connection.
 */
export function closeCredGenAIWebSocket() {
  const status = get(serviceStatus).status;

  if (status === 'paused' || status === 'running') {
    console.log('[WebSocket] Not closing — scan still active or paused.');
    return;
  }

  if (socket) {
    socket.close();
    socket = null;
    console.log('[WebSocket] Closed manually.');
  }
}
