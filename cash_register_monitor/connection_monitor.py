import socket
import threading
import time
from typing import Callable, Optional
from datetime import datetime


class ConnectionMonitor:
    def __init__(self, ip: str = "192.168.1.155", port: int = 4999, interval: int = 5):
        self.ip = ip
        self.port = port
        self.interval = interval
        self.is_connected = False
        self.last_check_time = None
        self.monitoring = False
        self.monitor_thread = None
        self.connection_callback: Optional[Callable[[bool, datetime], None]] = None
        self.timeout = 3
        
    def set_connection_callback(self, callback: Callable[[bool, datetime], None]):
        """Set callback function to be called when connection status changes"""
        self.connection_callback = callback
    
    def test_connection(self) -> bool:
        """Test TCP connection to the cash register"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.ip, self.port))
                return result == 0
        except Exception:
            return False
    
    def update_settings(self, ip: str, port: int, interval: int):
        """Update connection settings"""
        self.ip = ip
        self.port = port
        self.interval = interval
    
    def _monitor_loop(self):
        """Main monitoring loop running in background thread"""
        while self.monitoring:
            try:
                current_status = self.test_connection()
                current_time = datetime.now()
                
                if current_status != self.is_connected:
                    self.is_connected = current_status
                    if self.connection_callback:
                        self.connection_callback(self.is_connected, current_time)
                
                self.last_check_time = current_time
                
                time.sleep(self.interval)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(self.interval)
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
            # Perform initial connection test
            self.is_connected = self.test_connection()
            self.last_check_time = datetime.now()
            if self.connection_callback:
                self.connection_callback(self.is_connected, self.last_check_time)
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1)
    
    def get_status(self) -> dict:
        """Get current connection status information"""
        return {
            'connected': self.is_connected,
            'last_check': self.last_check_time,
            'target': f"{self.ip}:{self.port}",
            'interval': self.interval
        }