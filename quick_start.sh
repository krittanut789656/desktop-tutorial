#!/bin/bash
# Quick Start Script for ETF Portfolio Backtesting System
# This script provides a fast way to setup and run the system

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║              ETF Portfolio Backtesting System - Quick Start               ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if setup has been run
if [ ! -f "config.ini" ]; then
    echo "⚠ config.ini not found. Running initial setup..."
    echo ""
    python3 setup_production.py
else
    echo "✓ Configuration found"
    echo ""
    echo "Options:"
    echo "  1. Run main application"
    echo "  2. Run analytics examples"
    echo "  3. Run backtesting examples"
    echo "  4. Re-run setup"
    echo "  5. Check system status"
    echo "  0. Exit"
    echo ""
    read -p "Select option (0-5): " choice

    case $choice in
        1)
            echo ""
            echo "🚀 Launching main application..."
            python3 main.py
            ;;
        2)
            echo ""
            echo "📊 Launching analytics examples..."
            cd analytics
            python3 example_analytics.py
            ;;
        3)
            echo ""
            echo "📈 Launching backtesting examples..."
            cd backtesting
            python3 example_backtest.py
            ;;
        4)
            echo ""
            echo "🔧 Re-running setup..."
            python3 setup_production.py
            ;;
        5)
            echo ""
            echo "🔍 Checking system status..."
            python3 check_system.py
            ;;
        0)
            echo ""
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo ""
            echo "❌ Invalid option"
            exit 1
            ;;
    esac
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "Thank you for using ETF Portfolio Backtesting System!"
echo "════════════════════════════════════════════════════════════════════════════"
