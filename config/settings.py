import os

# Database Configuration
DB_DIR = "data/db"
DB_PATH = os.path.join(DB_DIR, "bank.db")
DB_BACKUP_PATH = os.path.join(DB_DIR, "backups/bank_backup.db")

# Data Directories
TRANSACTION_LOG_DIR = "data/transactions"
USER_DATA_DIR = "data/users"
BACKUP_DIR = "data/backups"

# Log Directories
LOG_DIR = "logs"
RECEIPT_DIR = os.path.join(LOG_DIR, "receipts")
AUDIT_LOG_DIR = os.path.join(LOG_DIR, "audit")

# Application Settings
APP_NAME = "BankApp"
APP_VERSION = "1.0.0"
DEBUG = False
