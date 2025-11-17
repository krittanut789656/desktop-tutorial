# 📋 วิธีดู Log Files และ Reports

## 📊 ไฟล์ที่ระบบสร้าง:

### 1. Analytics Reports (Text files)
- `insight1_risk_adjusted_report.txt` - Risk-adjusted performance analysis
- `insight2_rebalancing_analysis.txt` - Optimal rebalancing frequency
- `insight3_dca_vs_lumpsum.txt` - DCA vs Lump Sum comparison

### 2. Visualizations (PNG files)
- `insight1_risk_return_scatter.png` - Risk-return scatter plot
- `insight2_rebalancing_comparison.png` - Rebalancing strategy comparison
- `insight3_comparison_chart.png` - Portfolio value comparison
- `insight3_market_conditions.png` - Win rate by market condition

### 3. System Logs
- `analytics.log` - Analytics module execution log
- `backtesting.log` - Backtesting operations log (if enabled)

---

## 📂 ตำแหน่งไฟล์:

### Jupyter Notebook:
Files จะถูกสร้างใน **directory ที่คุณ run notebook**

```
ตัวอย่าง:
- Run จาก: /home/user/desktop-tutorial/
- Files อยู่ที่: /home/user/desktop-tutorial/insight*.txt
```

### Python Script:
Files จะถูกสร้างใน **current working directory**

```bash
cd /home/user/desktop-tutorial
python main_integrated.py
# → Files: /home/user/desktop-tutorial/insight*.txt

cd /home/user/desktop-tutorial/analytics
python example_analytics.py
# → Files: /home/user/desktop-tutorial/analytics/insight*.txt
```

---

## 🔍 วิธีดูไฟล์:

### วิธีที่ 1: ใช้ Jupyter Notebook

```python
# อ่าน report file
with open('insight1_risk_adjusted_report.txt', 'r') as f:
    print(f.read())
```

```python
# แสดงรูป
from IPython.display import Image, display
display(Image('insight1_risk_return_scatter.png'))
```

```python
# ดู log file
with open('analytics.log', 'r') as f:
    # แสดง 50 บรรทัดล่าสุด
    lines = f.readlines()
    print(''.join(lines[-50:]))
```

### วิธีที่ 2: ใช้ Terminal/Command Line

```bash
# ดู report
cat insight1_risk_adjusted_report.txt

# หรือใช้ less สำหรับไฟล์ยาว
less insight2_rebalancing_analysis.txt

# ดู log file (บรรทัดล่าสุด 50 บรรทัด)
tail -50 analytics.log

# ดู log แบบ real-time
tail -f analytics.log
```

### วิธีที่ 3: ใช้ File Explorer

**Windows:**
```
เปิด File Explorer → ไปที่ folder ที่ run notebook
```

**macOS:**
```
เปิด Finder → ไปที่ folder ที่ run notebook
```

**Linux:**
```bash
# เปิด file browser
nautilus /home/user/desktop-tutorial/

# หรือ list files
ls -lh /home/user/desktop-tutorial/*.txt
ls -lh /home/user/desktop-tutorial/*.png
```

---

## 📁 ตัวอย่างการจัดการไฟล์:

### ย้ายไฟล์ไปเก็บ:

```bash
# สร้าง folder สำหรับเก็บ reports
mkdir -p reports/$(date +%Y-%m-%d)

# ย้าย reports
mv insight*.txt reports/$(date +%Y-%m-%d)/
mv insight*.png reports/$(date +%Y-%m-%d)/
```

### Backup logs:

```bash
# สร้าง backup folder
mkdir -p logs_backup

# Copy logs
cp analytics.log logs_backup/analytics_$(date +%Y%m%d_%H%M%S).log
```

### ลบไฟล์เก่า:

```bash
# ลบ reports ทั้งหมด
rm -f insight*.txt
rm -f insight*.png

# ลบ logs
rm -f analytics.log
```

---

## 🔍 ค้นหาไฟล์:

### ค้นหา reports ทั้งหมด:

```bash
# Linux/macOS
find . -name "insight*.txt" -o -name "insight*.png"

# Windows PowerShell
Get-ChildItem -Recurse -Include insight*.txt,insight*.png
```

### ค้นหา reports ล่าสุด:

```bash
# Linux/macOS - แสดง 5 files ล่าสุด
ls -lt insight*.txt | head -5

# Windows PowerShell
Get-ChildItem insight*.txt | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

---

## 📊 ตัวอย่าง: ดู Reports ใน Jupyter

```python
import os
from glob import glob
from IPython.display import Image, display
import pandas as pd

# ===================================================================
# หา report files ทั้งหมด
# ===================================================================

print("📄 Text Reports:")
print("="*60)
for file in sorted(glob("insight*.txt")):
    size = os.path.getsize(file)
    mtime = pd.Timestamp(os.path.getmtime(file), unit='s')
    print(f"  {file:40s} {size:>8,} bytes  {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

print("\n📈 Visualizations:")
print("="*60)
for file in sorted(glob("insight*.png")):
    size = os.path.getsize(file)
    mtime = pd.Timestamp(os.path.getmtime(file), unit='s')
    print(f"  {file:40s} {size:>8,} bytes  {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

# ===================================================================
# อ่าน report
# ===================================================================

print("\n" + "="*60)
print("📄 INSIGHT 1: Risk-Adjusted Performance")
print("="*60)
try:
    with open('insight1_risk_adjusted_report.txt', 'r') as f:
        print(f.read())
except FileNotFoundError:
    print("⚠️  File not found - Run analytics first!")

# ===================================================================
# แสดงรูป
# ===================================================================

print("\n" + "="*60)
print("📈 VISUALIZATIONS")
print("="*60)
for file in sorted(glob("insight*.png")):
    print(f"\n{file}:")
    try:
        display(Image(file))
    except:
        print(f"⚠️  Cannot display {file}")
```

---

## 📋 ตัวอย่าง: Monitor Logs

```python
import time
from IPython.display import clear_output

def tail_log(filename='analytics.log', lines=20, refresh_seconds=5):
    """Monitor log file - แสดง real-time updates"""

    try:
        while True:
            clear_output(wait=True)

            print(f"📋 Monitoring: {filename}")
            print(f"   Refresh every {refresh_seconds} seconds")
            print(f"   Press Ctrl+C to stop")
            print("="*70)

            try:
                with open(filename, 'r') as f:
                    all_lines = f.readlines()
                    recent_lines = all_lines[-lines:]
                    print(''.join(recent_lines))
            except FileNotFoundError:
                print(f"⚠️  {filename} not found")

            print("="*70)
            print(f"Last update: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

            time.sleep(refresh_seconds)

    except KeyboardInterrupt:
        print("\n\n✓ Monitoring stopped")

# ใช้งาน:
# tail_log('analytics.log', lines=30, refresh_seconds=3)
```

---

## 💡 Tips:

### 1. Organize Reports:
```bash
# สร้าง folder structure
mkdir -p reports/{2024-01,2024-02,2024-03}
```

### 2. Auto-timestamped Files:

```python
# ใน Python code
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'insight1_risk_adjusted_{timestamp}.txt'
```

### 3. Rotate Logs:

```bash
# สร้าง cron job เพื่อ rotate logs ทุกวัน
0 0 * * * cd /home/user/desktop-tutorial && mv analytics.log analytics_$(date +\%Y\%m\%d).log
```

### 4. Quick View Script:

```bash
#!/bin/bash
# view_reports.sh

echo "📊 ETF Backtesting Reports"
echo "=========================="
echo ""
echo "📄 Text Reports:"
ls -lh insight*.txt 2>/dev/null || echo "  No reports found"
echo ""
echo "📈 Visualizations:"
ls -lh insight*.png 2>/dev/null || echo "  No visualizations found"
echo ""
echo "📋 Logs:"
ls -lh *.log 2>/dev/null || echo "  No logs found"
```

---

## ❓ FAQ

**Q: Files ไม่มี/หาไม่เจอ?**
A:
- ตรวจสอบว่า run analytics แล้วหรือยัง
- ตรวจสอบ current directory: `pwd` (Linux/Mac) หรือ `cd` (Windows)
- Files อาจอยู่ใน folder ที่คุณ run notebook

**Q: Log file ใหญ่เกินไป?**
A:
```bash
# ลบ log เก่า
rm analytics.log

# หรือ rotate
mv analytics.log analytics_backup.log
```

**Q: ต้องการ export reports ออกมา?**
A:
```bash
# Zip ทุกอย่าง
zip -r reports_$(date +%Y%m%d).zip insight*.txt insight*.png
```

**Q: Charts ไม่แสดง?**
A:
- ติดตั้ง matplotlib: `pip install matplotlib`
- ตรวจสอบว่าไฟล์ .png มีอยู่จริง
- ใช้ `display(Image('file.png'))` ใน Jupyter

---

## 🚀 Quick Commands:

```bash
# ดู reports ทั้งหมด
ls -lh insight*.{txt,png}

# อ่าน report ล่าสุด
ls -t insight1*.txt | head -1 | xargs cat

# แสดง charts ทั้งหมด (Jupyter)
from IPython.display import Image, display
import glob
for f in glob.glob('insight*.png'): display(Image(f))

# Tail log
tail -f analytics.log
```

---

**Happy Analyzing! 📊**
