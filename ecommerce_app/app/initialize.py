import datetime
import traceback
from app.shared.properties import properties
from app.shared.logging.logging_config import logger
logger.info("Server Started Successfully")

def initialize(property_file):
    try:
        print("Starting Ecommerce Initialization...")
        start_time = datetime.datetime.now()

        properties.load_properties(property_file)
        properties.initialize_sections()

        end_time = datetime.datetime.now()

        print(f"Initialization completed in {(end_time - start_time).total_seconds()} seconds")

    except Exception:
        print("Error during initialization")
        print(traceback.format_exc())
