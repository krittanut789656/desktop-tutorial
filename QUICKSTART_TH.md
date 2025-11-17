# Quick Start Guide - เริ่มใช้งานเร็ว 🚀

**เริ่มใช้งานภายใน 5 นาที!**

---

## ⚡ 3 ขั้นตอนเท่านั้น!

### ขั้นที่ 1: Setup (ครั้งเดียว)

```bash
python3 setup_production.py
```

**ตอบคำถาม:**
- MySQL Host: [กด Enter]
- MySQL Port: [กด Enter]
- MySQL User: [กด Enter]
- MySQL Password: **พิมพ์ password ของคุณ**

รอ 15-20 นาที (ส่วนใหญ่คือดึงข้อมูลราคา ETF)

### ขั้นที่ 2: ตรวจสอบ

```bash
python3 check_system.py
```

**ต้องเห็น:**
```
✓ Dependencies    PASS
✓ Configuration   PASS
✓ Modules         PASS
✓ Database        PASS

✓ System is ready for production use!
```

### ขั้นที่ 3: เริ่มใช้งาน!

```bash
python3 main.py
```

---

## 🎯 ทำอะไรได้บ้าง?

### 1. ดู Portfolio ตัวอย่าง (2 นาที)
```
เปิดแอป → เลือก 1.2 → ดู portfolio ที่ชอบ
```

### 2. วิเคราะห์ความเสี่ยง (5 นาที)
```bash
cd analytics
python3 example_analytics.py
เลือก: 1
```

### 3. หาความถี่ Rebalancing ที่ดีที่สุด (3 นาที)
```bash
cd analytics
python3 example_analytics.py
เลือก: 2
```

### 4. สร้าง Portfolio ของตัวเอง (3 นาที)
```
เปิดแอป → เลือก 1.1 → ตามขั้นตอน
```

---

## 📋 เมนูสำคัญ

```
1.1 = สร้าง Portfolio
1.2 = ดู Portfolios
2.1 = ดู ETFs ที่มี
3.3 = ดูประวัติ Backtests
4.x = Analytics (3 insights)
```

---

## ❓ มีปัญหา?

### ติด "Can't connect to MySQL"
```bash
sudo systemctl start mysql
```

### ติด "No module named xxx"
```bash
pip install -r requirements.txt
```

### อยากเริ่มใหม่
```bash
python3 setup_production.py
```

---

## 📚 อยากรู้มากกว่านี้?

**คู่มือฉบับสมบูรณ์:**
```bash
cat USER_GUIDE_TH.md
```

**Documentation:**
- `README.md` - Overview
- `PRODUCTION_SETUP.md` - Setup guide
- `USER_GUIDE_TH.md` - คู่มือละเอียด

---

## 🎓 ตัวอย่างการใช้งาน 10 นาที

```bash
# 1. เปิดแอป
python3 main.py

# 2. ดู portfolio Conservative 60/40
เลือก: 1.2 → พิมพ์: 1

# 3. วิเคราะห์
cd analytics
python3 example_analytics.py
เลือก: 1

# 4. ดูผลลัพธ์
cat insight1_risk_adjusted_report.txt
```

**เรียนรู้:**
- Portfolio นี้มีความเสี่ยงเท่าไร
- เทียบกับตลาดแล้วเป็นอย่างไร
- เหมาะกับเราไหม

---

## 💡 Tips เร็ว

**เร่งความเร็ว:**
```bash
./quick_start.sh  # เมนูรวม
```

**เช็คสถานะเร็ว:**
```bash
python3 check_system.py
```

**Analytics แบบครบ:**
```bash
cd analytics
python3 example_analytics.py
เลือก: 4  # Run ทั้ง 3 insights
```

---

## 🎯 เป้าหมาย

**ได้อะไร:**
- ✅ เข้าใจความเสี่ยงของ portfolio
- ✅ เปรียบเทียบกับตลาด (SPY)
- ✅ หาความถี่ rebalancing ที่ดี
- ✅ ตัดสินใจ DCA vs Lump Sum
- ✅ ลงทุนอย่างมีข้อมูล!

---

## 🚀 เริ่มเลย!

```bash
# ถ้ายังไม่ได้ setup
python3 setup_production.py

# ถ้า setup แล้ว
python3 main.py
```

**Good luck! 📊🎉**

---

## 📞 ต้องการความช่วยเหลือ?

1. ดู `USER_GUIDE_TH.md` (คู่มือละเอียด)
2. เช็ค logs: `tail -f main_app.log`
3. ดู FAQ ใน USER_GUIDE_TH.md section 8

**พร้อมช่วยเสมอ!** 💪
