# Import ข้อมูลเข้า MySQL - คู่มือง่ายๆ

## ✅ ไฟล์ที่มี (ทั้งหมด 6 ไฟล์):

```
excel_files/
├── 1_etf_master.xlsx                 (50 rows)
├── 2_benchmark_portfolios.xlsx       (35 rows)
├── 3_benchmark_holdings.xlsx         (116 rows)
├── 4_price_history_part01.xlsx       (100,000 rows)
├── 4_price_history_part02.xlsx       (100,000 rows)
└── 4_price_history_part03.xlsx       (8,700 rows)
```

---

## 🎯 วิธีที่ง่ายที่สุด: ใช้ Python Script (แนะนำ!)

### ทำไมต้องใช้ Python?
- ✅ **แปลง names เป็น IDs อัตโนมัติ** (benchmark_name → benchmark_id, ticker → etf_id)
- ✅ **รัน 1 คำสั่งเดียวจบ**
- ✅ **Import ถูกต้อง 100%**

### วิธีรัน:

**1. เปิด Terminal/CMD ไปที่โฟลเดอร์โปรเจค:**
```bash
cd /path/to/desktop-tutorial
```

**2. รัน script:**
```bash
python import_from_excel.py
```

**3. รอ 2-3 นาที**

**4. เสร็จ!** ✅

---

## 📋 วิธีที่ 2: Import ด้วย MySQL Workbench (ยุ่งยากกว่า)

### ⚠️ ข้อจำกัด:
- Import ได้แค่ 2 ตาราง:
  - ✅ etf_master
  - ✅ benchmark_portfolios
- ❌ **ไม่สามารถ import benchmark_holdings และ price_history ได้** เพราะต้องแปลง names เป็น IDs ก่อน

### ถ้าอยากลอง:

**ตารางที่ 1: etf_master**
1. เปิด MySQL Workbench
2. เชื่อมต่อกับ localhost
3. เลือก database `portfolio_backtesting`
4. คลิกขวาที่ table `etf_master` → **Table Data Import Wizard**
5. เลือก `1_etf_master.xlsx` (หรือแปลงเป็น CSV ก่อน)
6. ตั้งค่า Field Types:
   - ticker_symbol: VARCHAR(10)
   - etf_name: VARCHAR(255)
   - asset_class: VARCHAR(50)
   - region: VARCHAR(50)
   - sector: VARCHAR(100)
   - expense_ratio: DECIMAL(5,4)
   - inception_date: DATE
7. กด Next → Finish

**ตารางที่ 2: benchmark_portfolios**
- ทำซ้ำกับไฟล์ `2_benchmark_portfolios.xlsx`

**❌ ตารางที่ 3 และ 4 ไม่สามารถ import ด้วย Workbench ได้**

---

## 💡 Field Types สำหรับแต่ละ Column

ดูไฟล์ `FIELD_TYPES.md` สำหรับรายละเอียด

---

## ✅ ตรวจสอบว่า Import สำเร็จ

รัน SQL นี้:

```sql
SELECT COUNT(*) FROM etf_master;           -- ต้องได้ 50
SELECT COUNT(*) FROM benchmark_portfolios; -- ต้องได้ 35
SELECT COUNT(*) FROM benchmark_holdings;   -- ต้องได้ 116
SELECT COUNT(*) FROM price_history;        -- ต้องได้ 208,700
```

---

## 🎉 สรุป

**วิธีที่แนะนำ:**
```bash
python import_from_excel.py
```

เพียงแค่นี้! ใช้เวลา 2-3 นาที import เสร็จครบทุกตาราง 🚀
