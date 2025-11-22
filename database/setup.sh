#!/bin/bash

# =====================================================
# ETF Backtester Database Setup Script
# DADS 4002 Course Project
# =====================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
DB_HOST="${1:-localhost}"
DB_USER="${2:-root}"
DB_PASS="${3}"

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "ETF Backtester Database Setup"
echo "=========================================="
echo ""

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    print_error "MySQL client is not installed!"
    echo "Please install MySQL client first:"
    echo "  - Ubuntu/Debian: sudo apt-get install mysql-client"
    echo "  - CentOS/RHEL: sudo yum install mysql"
    echo "  - macOS: brew install mysql-client"
    exit 1
fi

print_success "MySQL client found"

# Prepare MySQL connection parameters
MYSQL_CMD="mysql -h ${DB_HOST} -u ${DB_USER}"

# If password is provided, add it to the command
if [ -n "$DB_PASS" ]; then
    MYSQL_CMD="${MYSQL_CMD} -p${DB_PASS}"
else
    print_info "No password provided. You may be prompted for password."
    MYSQL_CMD="${MYSQL_CMD} -p"
fi

echo ""
print_info "Connection Details:"
echo "  Host: ${DB_HOST}"
echo "  User: ${DB_USER}"
echo ""

# Test MySQL connection
print_info "Testing MySQL connection..."
if echo "SELECT 1;" | $MYSQL_CMD &> /dev/null; then
    print_success "Connected to MySQL successfully"
else
    print_error "Failed to connect to MySQL"
    echo "Please check your connection settings and credentials."
    exit 1
fi

echo ""
print_info "Step 1: Creating database schema..."

# Run schema creation
if $MYSQL_CMD < "${SCRIPT_DIR}/schema/01_create_schema.sql"; then
    print_success "Database schema created successfully"
else
    print_error "Failed to create database schema"
    exit 1
fi

echo ""
print_info "Step 2: Loading ETF master data..."

# Run data loading
if $MYSQL_CMD < "${SCRIPT_DIR}/data/02_load_etf_master.sql"; then
    print_success "ETF master data loaded successfully"
else
    print_error "Failed to load ETF master data"
    exit 1
fi

echo ""
print_info "Step 3: Verifying data..."

# Verify data
VERIFICATION=$(echo "USE etf_backtester_db; SELECT COUNT(*) as count FROM ETF_Master;" | $MYSQL_CMD -N)

if [ "$VERIFICATION" = "50" ]; then
    print_success "Verification successful: 50 ETFs loaded"
else
    print_error "Verification failed: Expected 50 ETFs, found ${VERIFICATION}"
    exit 1
fi

# Show summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
print_success "Database: etf_backtester_db"
print_success "Tables: ETF_Master, Price_Data, Strategy_Log"
print_success "Views: vw_latest_prices, vw_portfolio_summary"
print_success "ETFs Loaded: 50"
echo ""
print_info "Next steps:"
echo "  1. Load historical price data"
echo "  2. Implement backtesting logic"
echo "  3. Run strategy backtests"
echo ""
print_info "To connect to the database:"
echo "  mysql -h ${DB_HOST} -u ${DB_USER} -p etf_backtester_db"
echo ""

# Display asset type breakdown
echo "ETF Breakdown by Asset Type:"
echo "USE etf_backtester_db; SELECT Asset_Type, COUNT(*) as Count FROM ETF_Master GROUP BY Asset_Type ORDER BY Asset_Type;" | $MYSQL_CMD -t

exit 0
