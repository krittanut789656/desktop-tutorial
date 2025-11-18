@echo off
chcp 65001 >nul
REM ========================================
REM Import Price History - Windows Double-Click Version
REM ========================================

echo ======================================================================
echo        📥 Import Price History (208,700 rows)
echo ======================================================================
echo.

REM เปลี่ยนไปที่ directory ของไฟล์นี้
cd /d "%~dp0"

echo 📁 Working directory: %CD%
echo.

REM ========================================
REM เช็คว่ามี Python หรือไม่
REM ========================================
echo 🔍 ตรวจสอบ Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ไม่พบ Python!
    echo.
    echo 💡 กรุณาติดตั้ง Python ก่อน:
    echo    1. ดาวน์โหลดจาก: https://www.python.org/downloads/
    echo    2. ติดตั้ง Python (เลือก "Add Python to PATH"^)
    echo    3. รันไฟล์นี้อีกครั้ง
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM ========================================
REM ติดตั้ง libraries
REM ========================================
echo 📦 ติดตั้ง libraries (ถ้ายังไม่มี)...
echo.
python -m pip install --quiet mysql-connector-python pandas

REM ========================================
REM รัน import script
REM ========================================
echo.
echo ======================================================================
echo        🚀 เริ่ม Import!
echo ======================================================================
echo.

python import_price_history.py

REM ========================================
REM เสร็จแล้ว
REM ========================================
echo.
echo ======================================================================
pause
