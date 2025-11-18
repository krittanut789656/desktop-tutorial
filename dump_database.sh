#!/bin/bash
#
# Dump ETF Backtesting Database
# This script exports the entire database to a .sql file
#

# Configuration
DB_NAME="etf_backtesting"
DB_USER="root"
DB_PASS="krittanut123456"  # Update this
OUTPUT_FILE="etf_backtesting_database.sql"

echo "========================================================================"
echo "ETF BACKTESTING SYSTEM - Database Dump"
echo "========================================================================"
echo ""
echo "Database: $DB_NAME"
echo "Output:   $OUTPUT_FILE"
echo ""

# Check if mysqldump is available
if ! command -v mysqldump &> /dev/null; then
    echo "❌ Error: mysqldump command not found"
    echo "Please install MySQL client tools"
    exit 1
fi

# Perform dump
echo "Dumping database..."
mysqldump \
    --user="$DB_USER" \
    --password="$DB_PASS" \
    --host=127.0.0.1 \
    --port=3306 \
    --databases "$DB_NAME" \
    --add-drop-database \
    --add-drop-table \
    --create-options \
    --disable-keys \
    --extended-insert \
    --quick \
    --set-charset \
    --triggers \
    --routines \
    --events \
    --comments \
    --dump-date \
    > "$OUTPUT_FILE" 2>&1

# Check result
if [ $? -eq 0 ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo ""
    echo "✅ Database dump completed successfully!"
    echo "   File: $OUTPUT_FILE"
    echo "   Size: $FILE_SIZE"
    echo ""
    echo "To restore this database on another system:"
    echo "  mysql -u root -p < $OUTPUT_FILE"
else
    echo ""
    echo "❌ Error during database dump"
    echo "Please check:"
    echo "  1. MySQL is running"
    echo "  2. Username and password are correct"
    echo "  3. Database '$DB_NAME' exists"
    echo "  4. You have sufficient permissions"
fi

echo "========================================================================"
