# 📁 วิธีดาวน์โหลดไฟล์ Weekly Dataset

**ไฟล์ทั้งหมดอยู่ใน Git repository แล้ว**
**Branch:** `claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN`

---

## 🎯 วิธีดาวน์โหลด (เลือกวิธีที่ถูกต้อง)

### วิธีที่ 1: ถ้าคุณมี Git clone อยู่แล้ว ⭐⭐⭐⭐⭐

**ขั้นตอน:**

1. เปิด Terminal/Command Prompt

2. ไปที่ folder desktop-tutorial:
   ```bash
   cd /path/to/desktop-tutorial
   ```

3. Pull ไฟล์ล่าสุด:
   ```bash
   git pull origin claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN
   ```

4. เช็คว่าได้ไฟล์แล้ว:
   ```bash
   ls -la
   ```

   **ไฟล์ที่ต้องเห็น:**
   - ✅ `IMPORT_WEEKLY_EASY.bat`
   - ✅ `IMPORT_WEEKLY_EASY.sh`
   - ✅ `import_weekly_price_history.py`
   - ✅ `convert_daily_to_weekly.py`
   - ✅ `WEEKLY_IMPORT_GUIDE.md`
   - ✅ `data/etf_price_history_weekly.csv`

5. **พร้อมใช้งาน!** ไปที่ Step 2

---

### วิธีที่ 2: ถ้ายังไม่มี Git clone

**ขั้นตอน:**

1. Clone repository:
   ```bash
   git clone <repository-url>
   cd desktop-tutorial
   ```

2. Switch ไปที่ branch ที่ถูกต้อง:
   ```bash
   git checkout claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN
   ```

3. เช็คว่าได้ไฟล์แล้ว:
   ```bash
   ls -la
   ```

4. **พร้อมใช้งาน!** ไปที่ Step 2

---

### วิธีที่ 3: ดาวน์โหลดจาก GitHub/GitLab Web

**ขั้นตอน:**

1. เปิดเว็บ repository ของคุณ

2. เปลี่ยน branch เป็น: `claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN`

3. คลิก "Code" → "Download ZIP"

4. แตกไฟล์ ZIP ที่ดาวน์โหลดมา

5. **พร้อมใช้งาน!** ไปที่ Step 2

---

## 📂 โครงสร้างไฟล์ที่ได้

```
desktop-tutorial/
├── IMPORT_WEEKLY_EASY.bat           ← Windows double-click
├── IMPORT_WEEKLY_EASY.sh            ← Mac/Linux double-click
├── import_weekly_price_history.py   ← Python import script
├── convert_daily_to_weekly.py       ← Convert script
├── WEEKLY_IMPORT_GUIDE.md          ← คู่มือละเอียด
│
├── data/
│   ├── etf_price_history_weekly.csv  ← Weekly data (4.6 MB, 41,800 rows)
│   ├── etf_list.csv
│   ├── benchmark_portfolios.csv
│   └── benchmark_holdings.csv
│
├── IMPORT_ALL_DATA.sql              ← Import 3 ตารางแรก
└── ... (ไฟล์อื่นๆ)
```

---

## ✅ Step 2: ตรวจสอบว่าได้ไฟล์ครบ

**เปิด File Explorer/Finder แล้วเช็ค:**

1. ไปที่ folder `desktop-tutorial`

2. ต้องเห็นไฟล์เหล่านี้:
   - [ ] `IMPORT_WEEKLY_EASY.bat` (Windows)
   - [ ] `IMPORT_WEEKLY_EASY.sh` (Mac/Linux)
   - [ ] `import_weekly_price_history.py`
   - [ ] `WEEKLY_IMPORT_GUIDE.md`

3. เปิด folder `data/` ต้องเห็น:
   - [ ] `etf_price_history_weekly.csv` (ขนาด 4.6 MB)

**ถ้าครบแล้ว → ไปต่อ Step 3!**

---

## 🚀 Step 3: Import ข้อมูล

### ก่อนอื่น: Import 3 ตารางแรก (ถ้ายังไม่ได้ทำ)

1. เปิด MySQL Workbench
2. เปิดไฟล์ `IMPORT_ALL_DATA.sql`
3. Copy ทั้งหมด (Ctrl+A, Ctrl+C)
4. Paste ใน MySQL Workbench
5. Execute (Ctrl+Shift+Enter)
6. ตรวจสอบ:
   ```sql
   SELECT COUNT(*) FROM etf_master;  -- ต้องได้ 50
   ```

### จากนั้น: Import Weekly Price History

**Windows:**
1. Double-click ไฟล์ `IMPORT_WEEKLY_EASY.bat`
2. รอ 30-60 วินาที
3. เสร็จ! ✅

**Mac/Linux:**
1. Double-click ไฟล์ `IMPORT_WEEKLY_EASY.sh`
2. รอ 30-60 วินาที
3. เสร็จ! ✅

**หรือใช้ Python:**
```bash
cd /path/to/desktop-tutorial
python import_weekly_price_history.py
```

---

## ✅ ตรวจสอบว่าสำเร็จ

รัน SQL นี้ใน MySQL Workbench:

```sql
SELECT COUNT(*) FROM price_history;
-- ต้องได้: 41,800
```

```sql
SELECT
    MIN(price_date) as first_date,
    MAX(price_date) as last_date,
    COUNT(DISTINCT etf_id) as etf_count
FROM price_history;
-- ต้องได้:
-- first_date: 2009-01-02
-- last_date: 2025-01-03
-- etf_count: 50
```

---

## ❌ ถ้ายังไม่เห็นไฟล์

### ตรวจสอบว่าอยู่ branch ที่ถูกต้องไหม:

```bash
cd /path/to/desktop-tutorial
git branch
```

**ต้องเห็น:**
```
* claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN
```

**ถ้าไม่ใช่:**
```bash
git checkout claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN
git pull
```

---

## 💡 คำถามที่พบบ่อย

### Q: ผมอยู่บน Windows แต่ไม่เห็นไฟล์

**A:** ลอง:
1. เปิด File Explorer
2. ไปที่: `C:\Users\YourName\desktop-tutorial`
3. กด F5 (Refresh)
4. ถ้ายังไม่เห็น: รัน `git pull` ใน Command Prompt

### Q: ผมดาวน์โหลด ZIP แล้ว แต่ไม่มีไฟล์ weekly

**A:** ZIP อาจเป็น branch ผิด
- ตรวจสอบว่าดาวน์โหลด branch: `claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN`
- ไม่ใช่ `main` หรือ `master`

### Q: ไฟล์ etf_price_history_weekly.csv ขนาด 0 KB

**A:** อาจ pull ไม่สมบูรณ์
```bash
git lfs pull  # ถ้าใช้ Git LFS
# หรือ
git pull --rebase
```

---

## 📞 ติดปัญหา?

**บอกผมได้เลยครับ พร้อมข้อมูลนี้:**
1. ระบบปฏิบัติการ (Windows/Mac/Linux)
2. ผลลัพธ์จาก:
   ```bash
   pwd
   ls -la
   git branch
   git status
   ```
3. Screenshot folder desktop-tutorial

**จะช่วยแก้ให้ทันที!** 🚀
