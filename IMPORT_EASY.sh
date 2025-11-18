#!/bin/bash
# ========================================
# Import Price History - Mac/Linux Double-Click Version
# ========================================

echo "======================================================================"
echo "       📥 Import Price History (208,700 rows)"
echo "======================================================================"
echo

# เปลี่ยนไปที่ directory ของไฟล์นี้
cd "$(dirname "$0")"

echo "📁 Working directory: $(pwd)"
echo

# ========================================
# เช็คว่ามี Python หรือไม่
# ========================================
echo "🔍 ตรวจสอบ Python..."

if ! command -v python3 &> /dev/null
then
    echo
    echo "❌ ไม่พบ Python!"
    echo
    echo "💡 กรุณาติดตั้ง Python ก่อน:"
    echo "   Mac: brew install python3"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo
    read -p "กด Enter เพื่อปิด..."
    exit 1
fi

python3 --version
echo

# ========================================
# ติดตั้ง libraries
# ========================================
echo "📦 ติดตั้ง libraries (ถ้ายังไม่มี)..."
echo
python3 -m pip install --quiet mysql-connector-python pandas

# ========================================
# รัน import script
# ========================================
echo
echo "======================================================================"
echo "       🚀 เริ่ม Import!"
echo "======================================================================"
echo

python3 import_price_history.py

# ========================================
# เสร็จแล้ว
# ========================================
echo
echo "======================================================================"
read -p "กด Enter เพื่อปิด..."
