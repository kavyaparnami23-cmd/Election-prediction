import logging
import os
from datetime import datetime

# Create logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create log file with timestamp
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="[ %(asctime)s ] %(levelname)s - %(message)s"
)

logger = logging.getLogger("ElectionPulseAI")


# ---------------------- Testing ----------------------
if __name__ == "__main__":
    logger.info("Logger initialized successfully.")
    logger.warning("This is a warning message.")
    logger.error("This is a sample error message.")

    print("=" * 50)
    print("Logger is working successfully.")
    print(f"Log file created at: {LOG_PATH}")
    print("=" * 50)