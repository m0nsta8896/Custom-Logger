import pytz
import traceback
from logger import Logging

# Initialize the Logging class
logging = Logging(
    timezone=pytz.timezone("Asia/Kolkata"),
    logs_dir="logs",
    log_format = "log_%d-%m.txt",
    timestamp_format = "%H:%M",
    retention_days = 7,
    log_to_file = True,
    log_to_console = True,
    line_format = "{timestamp} │ {message}",
    file_encoding = 'utf-8',
    cleanup_on_startup = False
)

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
        # i had to use this because python's race condition preventing
        # the error message from getting logged and printed before the
        # logging.shutdown() is executed
        traceback.print_exc()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")
    finally:
        # STEP 2: Now, shut down the logger after everything is done.
        print("Shutting down logger...")
        logging.shutdown()