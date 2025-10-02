import pytz
import traceback
from logger import Logging

# Initialize the Logging class
logging = Logging(
    timezone=pytz.timezone("Asia/Kolkata"),
    logs_dir="logs",
    retention_days=30
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
        traceback.print_exc()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")
    finally:
        # STEP 2: Now, shut down the logger after everything is done.
        print("Shutting down logger...")
        logging.shutdown()