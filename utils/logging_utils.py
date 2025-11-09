import logging
import logging.handlers
from datetime import datetime
import os
from typing import Optional

class SecureLogger:
    """Enhanced logging utility for the secure distributed file system"""

    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        # Create formatters
        self.file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )
        self.console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        # Setup loggers
        self.security_logger = self._setup_logger('security', 'security.log')
        self.system_logger = self._setup_logger('system', 'system.log')
        self.error_logger = self._setup_logger('error', 'error.log')
        self.access_logger = self._setup_logger('access', 'access.log')

    def _setup_logger(self, name: str, filename: str) -> logging.Logger:
        """Setup a logger with file and console handlers"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        # File handler with rotation (daily, keep 30 days)
        log_path = os.path.join(self.log_dir, filename)
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_path,
            when='midnight',
            interval=1,
            backupCount=30
        )
        file_handler.setFormatter(self.file_formatter)
        logger.addHandler(file_handler)

        # Console handler for important messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only warnings and above to console
        console_handler.setFormatter(self.console_formatter)
        logger.addHandler(console_handler)

        return logger

    def log_security_event(self, event: str, user: Optional[str] = None,
                          ip_address: Optional[str] = None, details: Optional[dict] = None):
        """Log security-related events"""
        message = f"SECURITY: {event}"
        if user:
            message += f" | User: {user}"
        if ip_address:
            message += f" | IP: {ip_address}"
        if details:
            message += f" | Details: {details}"

        self.security_logger.info(message)

    def log_file_operation(self, operation: str, filename: str, user: str,
                          file_size: Optional[int] = None, success: bool = True):
        """Log file operations"""
        status = "SUCCESS" if success else "FAILED"
        message = f"FILE_{operation.upper()}: {filename} | User: {user} | Status: {status}"
        if file_size:
            message += f" | Size: {file_size} bytes"

        if success:
            self.access_logger.info(message)
        else:
            self.error_logger.error(message)

    def log_system_event(self, event: str, component: str = "system", details: Optional[dict] = None):
        """Log system-level events"""
        message = f"SYSTEM: {event} | Component: {component}"
        if details:
            message += f" | Details: {details}"

        self.system_logger.info(message)

    def log_error(self, error: str, component: str = "unknown",
                 exception: Optional[Exception] = None, user: Optional[str] = None):
        """Log errors"""
        message = f"ERROR: {error} | Component: {component}"
        if user:
            message += f" | User: {user}"
        if exception:
            message += f" | Exception: {str(exception)}"

        self.error_logger.error(message)

    def log_node_event(self, node_id: str, event: str, status: Optional[str] = None):
        """Log node-related events"""
        message = f"NODE: {node_id} | Event: {event}"
        if status:
            message += f" | Status: {status}"

        self.system_logger.info(message)

    def log_auth_attempt(self, username: str, success: bool,
                        ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Log authentication attempts"""
        status = "SUCCESS" if success else "FAILED"
        message = f"AUTH: {username} | Status: {status}"
        if ip_address:
            message += f" | IP: {ip_address}"
        if user_agent:
            message += f" | User-Agent: {user_agent}"

        if success:
            self.access_logger.info(message)
        else:
            self.security_logger.warning(message)

    def log_encryption_event(self, operation: str, filename: str,
                           algorithm: str = "AES-256", success: bool = True):
        """Log encryption/decryption operations"""
        status = "SUCCESS" if success else "FAILED"
        message = f"ENCRYPTION: {operation.upper()} | File: {filename} | Algorithm: {algorithm} | Status: {status}"

        if success:
            self.access_logger.info(message)
        else:
            self.error_logger.error(message)

# Global logger instance
secure_logger = SecureLogger()

class ErrorHandler:
    """Centralized error handling utility"""

    @staticmethod
    def handle_file_operation_error(operation: str, filename: str,
                                  error: Exception, user: Optional[str] = None) -> dict:
        """Handle file operation errors"""
        error_msg = f"File operation failed: {operation} on {filename}"
        secure_logger.log_error(error_msg, "file_operations", error, user)

        return {
            "error": error_msg,
            "details": str(error),
            "operation": operation,
            "filename": filename
        }

    @staticmethod
    def handle_auth_error(username: str, error: str) -> dict:
        """Handle authentication errors"""
        secure_logger.log_auth_attempt(username, False)
        secure_logger.log_security_event("Authentication failed", username, details={"error": error})

        return {
            "error": "Authentication failed",
            "details": error
        }

    @staticmethod
    def handle_encryption_error(operation: str, filename: str, error: Exception) -> dict:
        """Handle encryption/decryption errors"""
        secure_logger.log_encryption_event(operation, filename, success=False)
        secure_logger.log_error(f"Encryption error: {operation}", "encryption", error)

        return {
            "error": f"Encryption operation failed: {operation}",
            "details": str(error)
        }

    @staticmethod
    def handle_node_error(node_id: str, error: str) -> dict:
        """Handle node-related errors"""
        secure_logger.log_node_event(node_id, f"Error: {error}", "error")
        secure_logger.log_error(f"Node error: {node_id}", "node_management")

        return {
            "error": f"Node operation failed: {node_id}",
            "details": error
        }

# Global error handler
error_handler = ErrorHandler()