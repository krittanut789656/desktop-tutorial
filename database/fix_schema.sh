#!/bin/bash

# =====================================================
# ETF Backtester Database Fix Script
# Use this to troubleshoot and fix schema issues
# =====================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DB_HOST="${1:-localhost}"
DB_USER="${2:-root}"
DB_PASS="${3}"

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "ETF Backtester Database Fix & Diagnostic"
echo "=========================================="
echo ""

# Prepare MySQL connection
MYSQL_CMD="mysql -h ${DB_HOST} -u ${DB_USER}"
if [ -n "$DB_PASS" ]; then
    MYSQL_CMD="${MYSQL_CMD} -p${DB_PASS}"
else
    MYSQL_CMD="${MYSQL_CMD} -p"
fi

echo -e "${BLUE}Step 1: Running Diagnostics...${NC}"
echo ""

# Check if database exists
DB_EXISTS=$(echo "SHOW DATABASES LIKE 'etf_backtester_db';" | $MYSQL_CMD -N 2>/dev/null)

if [ -z "$DB_EXISTS" ]; then
    echo -e "${RED}✗ Database 'etf_backtester_db' does not exist${NC}"
    echo -e "${YELLOW}  This is likely the cause of your error${NC}"
else
    echo -e "${GREEN}✓ Database 'etf_backtester_db' exists${NC}"
fi

# Check if table exists
if [ -n "$DB_EXISTS" ]; then
    TABLE_EXISTS=$(echo "SHOW TABLES FROM etf_backtester_db LIKE 'ETF_Master';" | $MYSQL_CMD -N 2>/dev/null)

    if [ -z "$TABLE_EXISTS" ]; then
        echo -e "${RED}✗ Table 'ETF_Master' does not exist${NC}"
        echo -e "${YELLOW}  Schema was not created properly${NC}"
    else
        echo -e "${GREEN}✓ Table 'ETF_Master' exists${NC}"

        # Check table structure
        echo -e "${BLUE}  Checking table structure...${NC}"
        COLUMN_CHECK=$(echo "SHOW COLUMNS FROM etf_backtester_db.ETF_Master WHERE Field='Ticker_Symbol';" | $MYSQL_CMD -N 2>/dev/null)

        if [ -z "$COLUMN_CHECK" ]; then
            echo -e "${RED}  ✗ Column 'Ticker_Symbol' does not exist${NC}"
            echo -e "${YELLOW}  Table structure is incorrect${NC}"
        else
            echo -e "${GREEN}  ✓ Column 'Ticker_Symbol' exists${NC}"
        fi

        # Check record count
        RECORD_COUNT=$(echo "SELECT COUNT(*) FROM etf_backtester_db.ETF_Master;" | $MYSQL_CMD -N 2>/dev/null)
        echo -e "${GREEN}  ✓ Records in ETF_Master: ${RECORD_COUNT}${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "Recommended Actions:"
echo "=========================================="
echo ""

if [ -z "$DB_EXISTS" ] || [ -z "$TABLE_EXISTS" ]; then
    echo -e "${YELLOW}Issue Detected:${NC} Database or tables are missing"
    echo ""
    echo "Choose an option:"
    echo ""
    echo -e "${GREEN}Option 1: Automated Fix (Recommended)${NC}"
    echo "  This will recreate the database from scratch"
    echo ""
    read -p "  Run automated fix now? (y/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo -e "${BLUE}Recreating database...${NC}"

        # Run schema creation
        if $MYSQL_CMD < "${SCRIPT_DIR}/schema/01_create_schema.sql" 2>&1 | tee /tmp/schema_output.log; then
            echo -e "${GREEN}✓ Schema created successfully${NC}"

            # Run data loading
            echo ""
            echo -e "${BLUE}Loading ETF data...${NC}"
            if $MYSQL_CMD < "${SCRIPT_DIR}/data/02_load_etf_master.sql" 2>&1 | tee /tmp/data_output.log; then
                echo -e "${GREEN}✓ Data loaded successfully${NC}"

                # Verify
                FINAL_COUNT=$(echo "SELECT COUNT(*) FROM etf_backtester_db.ETF_Master;" | $MYSQL_CMD -N 2>/dev/null)
                echo ""
                echo "=========================================="
                echo -e "${GREEN}SUCCESS!${NC}"
                echo "=========================================="
                echo ""
                echo "Database: etf_backtester_db"
                echo "ETF Records: ${FINAL_COUNT}"
                echo ""
                echo "You can now run your queries!"
                echo ""
            else
                echo -e "${RED}✗ Failed to load data${NC}"
                echo "Check /tmp/data_output.log for details"
            fi
        else
            echo -e "${RED}✗ Failed to create schema${NC}"
            echo "Check /tmp/schema_output.log for details"
        fi
    else
        echo ""
        echo -e "${GREEN}Option 2: Manual Fix${NC}"
        echo "  Run these commands:"
        echo ""
        echo "  mysql -u ${DB_USER} -p < database/schema/01_create_schema.sql"
        echo "  mysql -u ${DB_USER} -p < database/data/02_load_etf_master.sql"
        echo ""
    fi
else
    echo -e "${GREEN}✓ No issues detected!${NC}"
    echo ""
    echo "Your database appears to be set up correctly."
    echo ""
    echo "If you're still getting errors:"
    echo "1. Make sure you're connected to the right database:"
    echo "   USE etf_backtester_db;"
    echo ""
    echo "2. Check your query syntax"
    echo ""
    echo "3. Run diagnostic script for more details:"
    echo "   mysql -u ${DB_USER} -p < database/diagnose.sql"
    echo ""
fi

echo ""
echo "For detailed troubleshooting, see:"
echo "  database/TROUBLESHOOTING.md"
echo ""
