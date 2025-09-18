import logging
import os
from datetime import datetime


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join("logs", "run.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    # CSV log header
    csv_path = os.path.join("logs", "run_log.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("timestamp,status,message\n")

    return logging.getLogger("ad_report_digest")


def csv_log(status: str, message: str):
    csv_path = os.path.join("logs", "run_log.csv")
    ts = datetime.utcnow().isoformat()
    with open(csv_path, "a", encoding="utf-8") as f:
        f.write(f"{ts},{status},{message}\n")
