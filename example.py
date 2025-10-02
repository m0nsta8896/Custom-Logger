import os
import sys
import datetime
import threading
from typing import Optional

class Logging:
    def __init__(self,
        timezone: datetime.timezone,
        logs_dir: str = "logs",
        log_format: str = "log_%d-%m-%Y.txt",
        timestamp_format: str = "%H:%M:%S",
        retention_days: int = 7,
        log_to_file: bool = True,
        log_to_console: bool = True,
        line_format: str = "[{timestamp}] {message}",
        file_encoding: str = 'utf-8',
        cleanup_on_startup: bool = True
    ):
        self.logs_dir = logs_dir
        self.timezone = timezone
        self.log_format = log_format
        self.retention_days = retention_days
        self.timestamp_format = timestamp_format
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.line_format = line_format
        self.file_encoding = file_encoding
        self.cleanup_on_startup = cleanup_on_startup
    
    def setup(self):
        if self.log_to_file:
            os.makedirs(self.logs_dir, exist_ok=True)
            if self.cleanup_on_startup:
                self.cleanup_logs()
        if isinstance(sys.stdout, Logger):
            print("Logging is already set up.")
            return
        
        logger = Logger(
            log_directory=self.logs_dir,
            timezone=self.timezone,
            log_format=self.log_format,
            timestamp_format=self.timestamp_format,
            log_to_file=self.log_to_file,
            log_to_console=self.log_to_console,
            line_format=self.line_format,
            file_encoding=self.file_encoding
        )
        sys.stdout = logger
        sys.stderr = logger
    
    def shutdown(self):
        if isinstance(sys.stdout, Logger):
            logger_instance = sys.stdout
            sys.stdout = logger_instance.terminal
            sys.stderr = logger_instance.terminal
            logger_instance.close()
    
    def cleanup_logs(self):
        now = datetime.datetime.now(self.timezone)
        
        try:
            if not os.path.isdir(self.logs_dir):
                return
            cutoff_date = now.date() - datetime.timedelta(days=self.retention_days)
            with os.scandir(self.logs_dir) as entries:
                for entry in entries:
                    if entry.is_file():
                        try:
                            mod_time = entry.stat().st_mtime
                            file_date = datetime.datetime.fromtimestamp(mod_time, self.timezone).date()
                            if file_date < cutoff_date:
                                os.remove(entry.path)
                        except OSError as e:
                            print(f"Error accessing file {entry.name}: {e}. Skipping.")
        except Exception as e:
            print(f"Error during log cleanup: {e}")

class Logger:
    def __init__(self,
        log_directory: str,
        timezone: datetime.timezone,
        log_format: str,
        timestamp_format: str,
        log_to_file: bool,
        log_to_console: bool,
        line_format: str,
        file_encoding: str
    ):
        self.log_directory = log_directory
        self.timezone = timezone
        self.log_format = log_format
        self.timestamp_format = timestamp_format
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.line_format = line_format
        self.file_encoding = file_encoding
        
        self.terminal = sys.stdout
        self.lock = threading.Lock()
        self.log_file: Optional[open] = None
        self.current_log_path = None
        self.current_day = None
        self.buffer = ""
        
        if self.log_to_file:
            self._rotate_log_if_needed()
    
    def _get_expected_log_path(self):
        today_str = datetime.datetime.now(self.timezone).strftime(self.log_format)
        return os.path.join(self.log_directory, today_str)
    
    def _rotate_log_if_needed(self):
        if not self.log_to_file:
            return
        today = datetime.datetime.now(self.timezone).date()
        if today != self.current_day:
            if self.log_file:
                self.log_file.close()
                print(f"Closed log file for {self.current_day}", file=self.terminal)
            self.current_day = today
            self.current_log_path = self._get_expected_log_path()
            is_empty = not (os.path.exists(self.current_log_path) and os.path.getsize(self.current_log_path) > 0)
            self.log_file = open(self.current_log_path, "a", encoding=self.file_encoding)
            if is_empty:
                rollover_msg = f"Logging initiated for {datetime.datetime.now(self.timezone).strftime('%A, %d %B %Y')}\n{'–'*50}\n"
                self.write(rollover_msg, is_internal=True)
    
    def write(self, message: str, is_internal: bool = False):
        with self.lock:
            if is_internal:
                if self.log_to_console:
                    self.terminal.write(message)
                if self.log_file and self.log_to_file:
                    self.log_file.write(message)
                return
            
            if self.log_to_file:
                self._rotate_log_if_needed()
            if self.log_to_console:
                self.terminal.write(message)
            
            if self.log_to_file and self.log_file:
                self.buffer += message
                while '\n' in self.buffer:
                    line, self.buffer = self.buffer.split('\n', 1)
                    if line.strip():
                        timestamp = datetime.datetime.now(self.timezone).strftime(self.timestamp_format)
                        formatted_line = self.line_format.format(timestamp=timestamp, message=line)
                        self.log_file.write(f"{formatted_line}\n")
    
    def flush(self):
        self.terminal.flush()
        if self.log_file:
            self.log_file.flush()
    
    def close(self):
        if self.buffer.strip() and self.log_file:
            timestamp = datetime.datetime.now(self.timezone).strftime(self.timestamp_format)
            formatted_line = self.line_format.format(timestamp=timestamp, message=self.buffer.strip())
            self.log_file.write(f"{formatted_line}\n")
            self.buffer = ""
        
        if self.log_file:
            self.log_file.close()
            self.log_file = None

__version__ = '1.5.2'