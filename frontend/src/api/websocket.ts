// Mock websocket for demonstration
export class MockWebSocket {
  private callbacks: Record<string, Function[]> = {};
  private intervalId: any;

  connect() {
    this.intervalId = setInterval(() => {
      this.emit('fusion_update', {
        timestamp: new Date().toISOString(),
        confidence: 0.7 + Math.random() * 0.25,
        uncertainty: 0.02 + Math.random() * 0.05,
        method: 'Dempster-Shafer',
        sourceWeights: {
          'camera-1': 0.3 + Math.random() * 0.2,
          'radar-1': 0.3 + Math.random() * 0.2,
          'lidar-1': 0.2 + Math.random() * 0.2
        }
      });
      
      if (Math.random() > 0.8) {
        this.emit('alert', {
          id: Math.random().toString(36).substr(2, 9),
          timestamp: new Date().toISOString(),
          severity: ['low', 'medium', 'high', 'critical'][Math.floor(Math.random() * 4)],
          source: 'System Monitor',
          message: 'Confidence variance detected in sector 7G',
          acknowledged: false
        });
      }
    }, 2000);
  }

  disconnect() {
    clearInterval(this.intervalId);
  }

  on(event: string, callback: Function) {
    if (!this.callbacks[event]) this.callbacks[event] = [];
    this.callbacks[event].push(callback);
  }

  emit(event: string, data: any) {
    if (this.callbacks[event]) {
      this.callbacks[event].forEach(cb => cb(data));
    }
  }
}
