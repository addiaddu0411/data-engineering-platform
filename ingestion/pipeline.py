from ingestion.csv_ingestion import load_csv
from ingestion.cleaning import DataCleaner
from ingestion.utils.validator import DataValidator
from ingestion.utils.logger import get_logger
from warehouse.db_loader import insert_data

def run_pipeline(file_path):
    logger = get_logger("ETL_PIPELINE")

    logger.info("Starting FULL ETL + WAREHOUSE pipeline")

    # 1. INGESTION
    logger.info("Step 1: Loading data")
    df = load_csv(file_path)

    if df is None:
        logger.error("Ingestion failed")
        return

    # 2. CLEANING
    logger.info("Step 2: Cleaning data")
    cleaner = DataCleaner(df)
    df = cleaner.run_all()

    # 3. VALIDATION
    logger.info("Step 3: Validating data")
    validator = DataValidator(df)

    try:
        validator.run_all()
        logger.info("Validation successful")
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return

    # 4. WAREHOUSE LOAD (MISSING PIECE FIXED)
    logger.info("Step 4: Loading into PostgreSQL warehouse")

    try:
        insert_data(df)
        logger.info("Data successfully inserted into PostgreSQL")
    except Exception as e:
        logger.error(f"Warehouse load failed: {e}")
        return

    logger.info("PIPELINE COMPLETED END-TO-END SUCCESSFULLY")


if __name__ == "__main__":
    file_path = "/mnt/c/Users/Abhishek Pandey/Desktop/pollution_us_2000_2016.csv"
    run_pipeline(file_path)
