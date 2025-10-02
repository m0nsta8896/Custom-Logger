# Custom Logger
Version: 1.5.2
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

Parameter           | Type               | Default                    | Description                                                                                            |
:------------------ | :----------------- | :------------------------- | :----------------------------------------------------------------------------------------------------- |
timezone            | datetime.timezone  | (Required)                 | The timezone object (e.g., from pytz) to use for all timestamps and date calculations.                 |
logs_dir            | str                | "logs"                     | The name of the directory where log files will be saved.                                               |
retention_days      | int                | 7                          | Number of days to keep logs before they are automatically deleted on startup.                          |
log_format          | str                | "log_%d-%m-%Y.txt"         | Filename format for the daily log files.                                                               |
timestamp_format    | str                | "%H:%M:%S"                 | The time format used inside the log file for each line.                                                |
log_to_file         | bool               | True                       | A switch to enable or disable logging to a file.                                                       |
log_to_console      | bool               | True                       | A switch to enable or disable printing output to the console.                                          |
line_format         | str                | "[{timestamp}] {message}"  | A customizable f-string like format for log lines. It uses {timestamp} and {message} as placeholders.  |
file_encoding       | str                | "utf-8"                    | Allows you to specify the file encoding for the log files.                                             |
cleanup_on_startup  | bool               | True                       | A switch to control whether the log cleanup process runs when setup() is called.                       |

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
```python
Logging initiated for Thursday, 02 October 2025
––––––––––––––––––––––––––––––––––––––––––––––––––
[09:26:49] Hello World!
[09:26:49] Traceback (most recent call last):
[09:26:49]   File "/Projects/.Projects/CustomLogger/example.py", line 22, in <module>
[09:26:49]     myapp()
[09:26:49]   File "/Projects/.Projects/CustomLogger/example.py", line 15, in myapp
[09:26:49]     value = 1 / 0
[09:26:49]             ~~^~~
[09:26:49] ZeroDivisionError: division by zero
[09:26:49] Shutting down logger...
```