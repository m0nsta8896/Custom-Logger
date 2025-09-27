# Custom Logger
Version: 1.5.0
This single-file utility provides robust, automatic logging for any Python script. It captures all output from print() and sys.stderr (including uncaught exceptions and traceback details), redirects it to a timestamped, daily log file, and keeps the original console output intact. It is designed to be a "set-and-forget" logging solution, especially useful for long-running applications like bots.
## Key Features
 * Automatic Dual Output: Messages are simultaneously written to the console and a log file.
 * Daily Log Rotation: A new log file (log_DD-MM-YYYY.txt) is automatically created each day.
 * Timestamped Lines: Every logged line is prefixed with a [HH:MM:SS] timestamp.
 * Automatic Cleanup: On startup, the script automatically deletes log files older than the configured retention_days (default is 7).
 * Error Capture: Fully captures and logs all Python exceptions and tracebacks that would normally print to sys.stderr.
## How to Use
The logging process requires three simple steps: Import, Initialize, and Setup/Shutdown.
1. Import and Initialize
Create an instance of the Logging class, passing your desired configuration:

| Parameter | Type | Default | Description |
|---|---|---|---|
| timezone | datetime.timezone | (Required) | The timezone object to use for all timestamps and date calculations. |
| logs_dir | str | "logs" | Directory where log files will be stored. |
| retention_days | int | 7 | Number of days to keep logs before they are automatically cleaned up on startup. |
| log_format | str | "log_%d-%m-%Y.txt" | strftime format for the log filename (creates a new file per day). |
| timestamp_format | str | "%H:%M:%S" | strftime format for the timestamp prefix on each logged line. |
| line_format | str | [{timestamp}] {message} | A customizable format string for log lines, using {timestamp} and {message} placeholders. |
| log_to_file | bool | True | If False, disables writing to file but keeps console capture enabled. |
| log_to_console | bool | True | If False, disables printing output to the console (headless logging). |
| file_encoding | str | "utf-8" | File encoding for the log files. |
| cleanup_on_startup | bool | True | If False, disables the log cleanup process when setup() is called. |

```python
import pytz
import traceback
from logger import Logging

# Initialize the Logging class
logging = Logging(
    timezone=pytz.timezone("Asia/Kolkata"),
    logs_dir="logs",
    retention_days=30
)
```
2. Setup and Shutdown
Wrap your main application logic between the setup() and shutdown() methods.
 * logging.setup(): Must be called once at the very start of your application.
 * logging.shutdown(): Must be called before the script exits (e.g., in a finally block or on a termination signal).
```python
def myapp():
    print("Hello World!")
    # Intentional error:
    value = 1 / 0

if __name__ == "__main__":
    # STEP 1: Setup Logging
    logging.setup()
    
    try:
        myapp()
    except Exception:
        # traceback.print_exc() automatically prints the full traceback
        traceback.print_exc()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")
    finally:
        # STEP 2: Now, shut down the logger after everything is done.
        print("Shutting down logger...")
        logging.shutdown()
```
## Expected Output
```
============================================================
Logging initiated for Saturday, 27 September 2025
============================================================
[20:40:30] ============================================================
[20:40:30] Logging for Saturday, 27 September 2025 initiated.
[20:40:30] Output will be saved to files in: 'logs'
[20:40:30] ============================================================
[20:40:30] Hello World!
[20:40:30] Traceback (most recent call last):
[20:40:30]   File "/storage/emulated/0/Projects/.Projects/CustomLogger/example.py", line 23, in <module>
[20:40:30]     myapp()
[20:40:30]   File "/storage/emulated/0/Projects/.Projects/CustomLogger/example.py", line 16, in myapp
[20:40:30]     value = 1 / 0
[20:40:30]             ~~^~~
[20:40:30] ZeroDivisionError: division by zero
[20:40:30] Shutting down logger...
```
