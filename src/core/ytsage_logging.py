"""
YTSage logging configuration using loguru.

This module provides centralized logging configuration for the entire YTSage application.
It replaces the inefficient print statements with structured logging using loguru.
"""

import os
import sys
from pathlib import Path

# Try to import loguru, but handle case where it might not be available
try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    # Create a dummy logger class that does nothing
    class DummyLogger:
        def info(self, *args, **kwargs): pass
        def debug(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
        def critical(self, *args, **kwargs): pass
        def remove(self, *args, **kwargs): pass
        def add(self, *args, **kwargs): pass
        def bind(self, *args, **kwargs): return self
        @property
        def _core(self):
            class Core:
                handlers = []
            return Core()
    
    logger = DummyLogger()


def setup_logging():
    """
    Configure loguru logging for YTSage application.
    
    Sets up multiple log levels and outputs:
    - Console output for INFO and above
    - File output for DEBUG and above  
    - Separate error log file for ERROR and above
    """
    
    if not LOGURU_AVAILABLE:
        return logger
    
    # Remove default logger to avoid duplicate output
    try:
        logger.remove()
    except Exception:
        pass
    
    # Get the application data directory with fallbacks
    try:
        if sys.platform == 'win32':
            localappdata = os.environ.get('LOCALAPPDATA')
            if localappdata:
                log_dir = Path(localappdata) / 'YTSage' / 'logs'
            else:
                # Fallback for PyInstaller or when LOCALAPPDATA is not set
                log_dir = Path.home() / 'AppData' / 'Local' / 'YTSage' / 'logs'
        elif sys.platform == 'darwin':
            log_dir = Path.home() / 'Library' / 'Application Support' / 'YTSage' / 'logs'
        else:
            log_dir = Path.home() / '.local' / 'share' / 'YTSage' / 'logs'
    except Exception:
        # Ultimate fallback - use current directory
        log_dir = Path.cwd() / 'logs'
    
    # Create log directory if it doesn't exist
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # If we can't create the log directory, fall back to current directory
        log_dir = Path.cwd()
        try:
            log_dir.mkdir(exist_ok=True)
        except Exception:
            pass  # If we still can't create it, we'll just log to console
    
    # Console handler - INFO and above, with colors
    # Check if stdout is available (it might be None in PyInstaller windowed apps)
    stdout_available = sys.stdout is not None
    
    if stdout_available:
        try:
            logger.add(
                sys.stdout,
                level="INFO",
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                colorize=True,
                catch=True
            )
        except Exception:
            # Fallback to basic console logging without colors
            try:
                logger.add(
                    sys.stdout,
                    level="INFO",
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
                    catch=True
                )
            except Exception:
                stdout_available = False
    
    # If stdout is not available, try stderr or skip console logging entirely
    if not stdout_available:
        try:
            if sys.stderr is not None:
                logger.add(
                    sys.stderr,
                    level="WARNING",  # Only warnings and errors to stderr
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
                    catch=True
                )
        except Exception:
            # If even stderr fails, we'll rely only on file logging
            pass
    
    # Only add file handlers if we successfully created a log directory
    if log_dir and log_dir.exists():
        try:
            # Main log file - DEBUG and above, with rotation
            logger.add(
                log_dir / "ytsage.log",
                level="DEBUG", 
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                rotation="10 MB",  # Rotate when file reaches 10MB
                retention="7 days",  # Keep logs for 7 days
                compression="zip",  # Compress old logs
                catch=True
            )
            
            # Error log file - ERROR and above only
            logger.add(
                log_dir / "ytsage_errors.log",
                level="ERROR",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                rotation="5 MB",
                retention="30 days",  # Keep error logs longer
                compression="zip",
                catch=True
            )
        except Exception as e:
            # If file logging fails, just log to console
            logger.warning(f"Could not set up file logging: {e}")
    
    # Log startup message if we have any handlers
    if logger._core.handlers:
        logger.info("YTSage logging system initialized")
        if log_dir and log_dir.exists():
            logger.debug(f"Log directory: {log_dir}")
        else:
            logger.warning("File logging disabled - could not create log directory")
    
    # If no handlers were successfully added, add a null handler to prevent errors
    if not logger._core.handlers:
        # Add a minimal handler that just discards messages
        # This prevents loguru from complaining about no handlers
        import tempfile
        try:
            # Try to add a temporary file handler as last resort
            temp_log = Path(tempfile.gettempdir()) / "ytsage_temp.log"
            logger.add(temp_log, level="ERROR", catch=True)
        except Exception:
            # If even that fails, we're in a very restricted environment
            # loguru should handle this gracefully with its internal fallbacks
            pass
    
    return logger


def get_logger(name: str = None):
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module/component requesting the logger
        
    Returns:
        Configured logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger


# Initialize logging when module is imported - with maximum safety
_setup_complete = False

def safe_setup():
    """Safely initialize logging with multiple fallback strategies."""
    global _setup_complete
    if _setup_complete:
        return logger
    
    try:
        setup_logging()
        _setup_complete = True
    except Exception:
        # If all else fails, create an even simpler logger that just prints
        if LOGURU_AVAILABLE:
            try:
                logger.remove()
            except Exception:
                pass
        
        # At this point, just ensure we have something that won't crash
        _setup_complete = True
    
    return logger

# Try to set up logging, but don't let it crash the module import
try:
    safe_setup()
except Exception:
    # Ultimate fallback - the module will still import successfully
    pass

# Export the main logger for convenience
__all__ = ['logger', 'get_logger', 'setup_logging']
