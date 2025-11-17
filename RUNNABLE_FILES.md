# 🚀 ไฟล์ที่สามารถ Run Code ได้

**คู่มือฉบับสมบูรณ์ - ไฟล์ไหนรันได้บ้าง?**

---

## 📋 สรุปรวด เร็ว:

### ⭐ แนะนำสำหรับมือใหม่:
1. **`Integrated_System_All_In_One.ipynb`** - ใช้งานประจำวัน (Jupyter)
2. **`Complete_Setup_and_Run.ipynb`** - Setup ครั้งแรก (Jupyter)

### ⭐ แนะนำสำหรับ Production:
1. **`main_integrated.py`** - ใช้งานประจำวัน (Terminal)

---

## 📊 ไฟล์ Jupyter Notebooks (.ipynb)

### 🌟 **Primary - ใช้งานหลัก:**

#### 1. **`Integrated_System_All_In_One.ipynb`** ⭐ แนะนำ!
```bash
jupyter notebook Integrated_System_All_In_One.ipynb
```

**ทำอะไร:**
- ✅ Run ทีเดียว ได้ทุกอย่าง
- ✅ Menu Loop แบบต่อเนื่อง
- ✅ ไม่ต้องมีไฟล์อื่น (Standalone)

**Features:**
- View Portfolios
- View ETFs  
- View Price Data
- Run Backtest (Buy & Hold)
- View Backtest History
- System Statistics

**ขั้นตอน:**
1. แก้ password ใน Cell 1
2. Run Cell 1 → Setup system
3. Run Cell 2 → Start menu loop
4. ใช้งานไปเรื่อยๆ จนกด 0 เพื่อ Exit

---

#### 2. **`Complete_Setup_and_Run.ipynb`** 🔧 Setup ครั้งแรก
```bash
jupyter notebook Complete_Setup_and_Run.ipynb
```

**ทำอะไร:**
- ✅ สร้าง Database + Tables
- ✅ Insert 40 ETFs
- ✅ Insert 7 Sample Portfolios
- ✅ Download ข้อมูลราคา (2009-2025) ⏱️ 15-20 นาที

**เมื่อไร:**
- ครั้งแรกที่ใช้งาน (Setup only)
- ต้องการ reset database

**ขั้นตอน:**
1. แก้ password ใน Cell 1
2. Run All (Cell → Run All)
3. รอให้เสร็จ (~20 นาที)

---

### 🎯 **Alternatives - ทางเลือกอื่น:**

#### 3. **`Integrated_System_Standalone.ipynb`** 
```bash
jupyter notebook Integrated_System_Standalone.ipynb
```

**ทำอะไร:**
- เหมือน `Integrated_System_All_In_One.ipynb`
- Standalone - ไม่ต้องมีไฟล์อื่น

**Note:** ใช้อันไหนก็ได้ ฟีเจอร์เหมือนกัน

---

#### 4. **`Main_Controller.ipynb`** 
```bash
jupyter notebook Main_Controller.ipynb
```

**ทำอะไร:**
- Interactive Widgets interface
- ต้องมี module files (crud_operations, backtesting, analytics)

**ข้อจำกัด:**
- ต้อง Run หลาย Cells
- ไม่ใช่ Loop system

---

#### 5. **`ETF_Full_Production.ipynb`**
```bash
jupyter notebook ETF_Full_Production.ipynb
```

**ทำอะไร:**
- View และ analyze data
- Create charts
- Custom analysis with Pandas

**Features:**
- Portfolio viewing
- ETF data exploration
- Price data analysis
- Charts และ visualizations
- Custom SQL queries

---

#### 6. **`Simple_Run_All.ipynb`**
```bash
jupyter notebook Simple_Run_All.ipynb
```

**ทำอะไร:**
- ดูข้อมูลพื้นฐาน
- Basic charts

**ข้อจำกัด:**
- ไม่มี Backtesting
- ไม่มี Analytics

---

#### 7. **`ETF_Backtesting_Notebook.ipynb`**
```bash
jupyter notebook ETF_Backtesting_Notebook.ipynb
```

**ทำอะไร:**
- Advanced features
- ต้องใช้ `jupyter_interface.py`

**ข้อจำกัด:**
- อาจมี import errors
- ไม่แนะนำ (ใช้ Integrated System แทน)

---

## 🐍 ไฟล์ Python Scripts (.py)

### 🌟 **Primary - ใช้งานหลัก:**

#### 1. **`main_integrated.py`** ⭐ Production Ready!
```bash
cd desktop-tutorial
python main_integrated.py
```

**ทำอะไร:**
- ✅ Integrated System แบบ Terminal
- ✅ Menu Loop ต่อเนื่อง
- ✅ เหมาะสำหรับ Production

**Features:**
- Portfolio Management
- ETF Management
- Run Backtests
- Run Analytics
- System Statistics

**ขั้นตอน:**
1. Run command
2. ใส่ MySQL password
3. ใช้ Menu system
4. กด 0 เพื่อ Exit

---

#### 2. **`main.py`** 📋 Original Version
```bash
cd desktop-tutorial
python main.py
```

**ทำอะไร:**
- Original console application
- Menu-driven interface

**Note:** เป็น version เก่า แนะนำใช้ `main_integrated.py` แทน

---

### 🔧 **Module Scripts - รันแยกได้:**

#### 3. **CRUD Operations:**
```bash
cd desktop-tutorial/crud_operations
python test_crud.py
```

**ทำอะไร:**
- ทดสอบ CRUD operations
- Portfolio management
- ETF management

---

#### 4. **Backtesting:**
```bash
cd desktop-tutorial/backtesting
python example_backtest.py
```

**ทำอะไร:**
- Run example backtests
- ทดสอบ strategies ต่างๆ
- Generate backtest reports

**Strategies:**
- Buy & Hold
- Rebalancing (monthly/quarterly/semi-annual/annual)
- Dollar Cost Averaging (DCA)

---

#### 5. **Analytics:**
```bash
cd desktop-tutorial/analytics
python example_analytics.py
```

**ทำอะไร:**
- Run 3 Analytics Insights
- Generate reports และ charts

**Insights:**
- Insight 1: Risk-Adjusted Performance
- Insight 2: Optimal Rebalancing
- Insight 3: DCA vs Lump Sum

---

#### 6. **Data Collection:**
```bash
cd desktop-tutorial/data_collection
python data_collection.py
```

**ทำอะไร:**
- Download ETF price data
- Update ข้อมูลราคา
- Insert เข้า database

**Note:** ใช้เวลา 10-15 นาที (40 ETFs)

---

### ⚙️ **Utility Scripts:**

#### 7. **`setup_production.py`**
```bash
python setup_production.py
```

**ทำอะไร:**
- Setup production environment
- Create database
- Insert sample data

---

#### 8. **`check_system.py`**
```bash
python check_system.py
```

**ทำอะไร:**
- ตรวจสอบระบบ
- Check database connection
- Verify modules

---

#### 9. **`test_connection.py`**
```bash
python test_connection.py
```

**ทำอะไร:**
- ทดสอบ MySQL connection
- Verify credentials

---

## 📊 ตารางสรุป - เลือกใช้ไฟล์ไหนดี?

### สำหรับมือใหม่ (Jupyter):

| Use Case | File | Run Time | Features |
|----------|------|----------|----------|
| **Setup ครั้งแรก** | `Complete_Setup_and_Run.ipynb` | 20 min | Setup DB + Data |
| **ใช้งานทุกวัน** | `Integrated_System_All_In_One.ipynb` | Instant | Full Features |
| **ดูข้อมูลเบื้องต้น** | `Simple_Run_All.ipynb` | Instant | View Only |
| **Analyze ข้อมูล** | `ETF_Full_Production.ipynb` | Instant | Charts + Analysis |

### สำหรับ Production (Terminal):

| Use Case | File | Run Time | Features |
|----------|------|----------|----------|
| **ใช้งานทุกวัน** | `main_integrated.py` | Instant | Full Features |
| **Setup** | `setup_production.py` | 20 min | Setup DB + Data |
| **Run Analytics** | `analytics/example_analytics.py` | 5-10 min | Generate Reports |
| **Run Backtest** | `backtesting/example_backtest.py` | 1-2 min | Test Strategies |

---

## 🎯 Recommended Workflow:

### ครั้งแรก (First Time):

```bash
# Option A: Jupyter
jupyter notebook Complete_Setup_and_Run.ipynb
# → Run All → Wait 20 minutes

# Option B: Terminal
python setup_production.py
# → Wait 20 minutes
```

### ใช้งานประจำวัน (Daily Use):

```bash
# Option A: Jupyter (แนะนำสำหรับมือใหม่)
jupyter notebook Integrated_System_All_In_One.ipynb
# → Run Cell 1 → Run Cell 2 → Use menu

# Option B: Terminal (แนะนำสำหรับ Production)
python main_integrated.py
# → Enter password → Use menu
```

### วิเคราะห์ข้อมูล (Analysis):

```bash
# Option A: Jupyter
jupyter notebook ETF_Full_Production.ipynb
# → Custom analysis with Pandas

# Option B: Terminal
cd analytics
python example_analytics.py
# → Generate reports
```

---

## 💡 Tips:

### 1. ไฟล์ที่ใช้บ่อยที่สุด:
```
✅ Integrated_System_All_In_One.ipynb (Jupyter)
✅ main_integrated.py (Terminal)
```

### 2. ไฟล์ที่ Run ครั้งเดียว:
```
✅ Complete_Setup_and_Run.ipynb (Setup)
✅ setup_production.py (Setup)
```

### 3. ไฟล์สำหรับ Advanced Users:
```
✅ analytics/example_analytics.py
✅ backtesting/example_backtest.py
✅ data_collection/data_collection.py
```

---

## ❓ FAQ

**Q: ควรเริ่มจากไฟล์ไหน?**
A: 
1. ครั้งแรก → `Complete_Setup_and_Run.ipynb`
2. หลังจากนั้น → `Integrated_System_All_In_One.ipynb`

**Q: ไฟล์ไหนดีที่สุด?**
A: 
- Jupyter → `Integrated_System_All_In_One.ipynb`
- Terminal → `main_integrated.py`

**Q: ต้องการ Run Analytics?**
A:
- ใน Integrated System → เลือก Menu option 7
- แยก → `analytics/example_analytics.py`

**Q: ต้องการ Run Backtest?**
A:
- ใน Integrated System → เลือก Menu option 5
- แยก → `backtesting/example_backtest.py`

**Q: Update ราคา ETF?**
A:
```bash
cd data_collection
python data_collection.py
```

**Q: ไฟล์ไหนที่ไม่ควร Run?**
A:
- `jupyter_interface.py` - เป็น library ไม่ใช่ standalone script
- `config.py` - Configuration only
- `etf_system.py` - Legacy file

---

## 🚀 Quick Commands:

### Setup (ครั้งเดียว):
```bash
# Jupyter
jupyter notebook Complete_Setup_and_Run.ipynb

# Terminal
python setup_production.py
```

### Daily Use (แนะนำ):
```bash
# Jupyter
jupyter notebook Integrated_System_All_In_One.ipynb

# Terminal
python main_integrated.py
```

### Analytics:
```bash
cd analytics
python example_analytics.py
```

### Backtest:
```bash
cd backtesting
python example_backtest.py
```

### Update Data:
```bash
cd data_collection
python data_collection.py
```

---

## 📁 File Organization:

```
desktop-tutorial/
│
├── 🌟 PRIMARY RUNNABLE FILES 🌟
│   ├── Integrated_System_All_In_One.ipynb  ⭐ Daily (Jupyter)
│   ├── Complete_Setup_and_Run.ipynb        🔧 Setup (Jupyter)
│   ├── main_integrated.py                  ⭐ Daily (Terminal)
│   └── setup_production.py                 🔧 Setup (Terminal)
│
├── 📊 ALTERNATIVE NOTEBOOKS
│   ├── Integrated_System_Standalone.ipynb
│   ├── Main_Controller.ipynb
│   ├── ETF_Full_Production.ipynb
│   ├── Simple_Run_All.ipynb
│   └── ETF_Backtesting_Notebook.ipynb
│
├── 🐍 MODULE SCRIPTS
│   ├── crud_operations/
│   │   └── test_crud.py
│   ├── backtesting/
│   │   └── example_backtest.py
│   ├── analytics/
│   │   └── example_analytics.py
│   └── data_collection/
│       └── data_collection.py
│
└── ⚙️ UTILITY SCRIPTS
    ├── main.py                             (Legacy)
    ├── check_system.py
    └── test_connection.py
```

---

**Happy Coding! 🚀**

**เลือกไฟล์ที่เหมาะกับคุณและเริ่มใช้งานได้เลย!** ✅
