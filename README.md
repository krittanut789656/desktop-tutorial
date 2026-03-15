# การวิเคราะห์ผลกระทบจากการนำเข้าและส่งออกสินค้ากับภาวะสงครามที่เกิดขึ้นในปัจจุบัน

## Thailand Trade Impact Analysis: US-Israel vs Iran Conflict (2026)

### DADS 5001 Mini-Project | Data Analytics and Data Science Tools and Programming
### ภาคเรียนที่ 2/2568 | DADS, NIDA

---

## สมาชิกกลุ่ม

| ชื่อ | รหัสนักศึกษา | หน้าที่ |
|------|-------------|---------|
| ___ | ___ | Data Collection & Cleaning |
| ___ | ___ | EDA & Visualization |
| ___ | ___ | Analysis & Presentation |

---

## บทคัดย่อ (Abstract)

โปรเจกต์นี้วิเคราะห์ผลกระทบของสงคราม US-Israel vs Iran (เริ่ม 28 กุมภาพันธ์ 2026) ต่อการนำเข้า-ส่งออกของประเทศไทย โดยเฉพาะผลกระทบจากการปิดช่องแคบ Hormuz ซึ่งเป็นเส้นทางขนส่งน้ำมันหลักของโลก

การวิเคราะห์ครอบคลุม:
- **พลังงาน**: น้ำมันดิบ, LNG, LPG (HS 27)
- **ปุ๋ยเคมี**: ผลกระทบต่อต้นทุนเกษตรกรรม (HS 31)
- **สินค้าเกษตร/อาหาร**: ข้าว, อาหารกระป๋อง, ยางพารา, น้ำตาล (HS 10, 16, 40, 17)
- **อุตสาหกรรม**: อิเล็กทรอนิกส์, ยานยนต์, พลาสติก (HS 85, 87, 39)
- **ปิโตรเคมี**: เคมีอินทรีย์/แนฟทา (HS 29)

เปรียบเทียบผลกระทบกับวิกฤตที่ผ่านมา: COVID-19, สงคราม Russia-Ukraine, และ 12-Day War

---

## แหล่งข้อมูล

- **หลัก:** [tradereport.moc.go.th](https://tradereport.moc.go.th) — ระบบสถิติการค้าระหว่างประเทศ กระทรวงพาณิชย์
- **API:** [dataapi.moc.go.th](https://dataapi.moc.go.th) — MOC Open Data API
- **ช่วงเวลา:** รายเดือน ปี 2019-2026
- **ประเภท:** Open Data ภาครัฐ (ได้รับอนุญาตเผยแพร่)

---

## โครงสร้างโปรเจกต์

```
├── README.md                          # ไฟล์นี้
├── mini_project_eda.ipynb             # Jupyter Notebook หลัก
├── requirements.txt                   # Python dependencies
├── data/
│   ├── raw/                           # ข้อมูลดิบจาก API
│   │   ├── thailand_trade_raw_data.xlsx
│   │   ├── trade_overview.csv
│   │   ├── energy_imports.csv
│   │   ├── fertilizer_imports.csv
│   │   ├── agrifood_exports.csv
│   │   ├── industrial_exports.csv
│   │   ├── petrochemical_imports.csv
│   │   └── api_errors.log
│   └── clean/                         # ข้อมูลที่ clean แล้ว
│       ├── thailand_trade_clean.xlsx
│       ├── thailand_trade_clean.csv
│       └── data_quality_report.txt
├── src/
│   ├── 01_data_collection.py          # ดึงข้อมูลจาก API
│   ├── 02_data_cleaning.py            # ทำความสะอาดข้อมูล
│   ├── 03_eda_analysis.py             # วิเคราะห์ EDA 10 Insights
│   ├── generate_simulated_data.py     # สร้างข้อมูลจำลอง (สำหรับ demo)
│   └── utils.py                       # Shared functions
├── outputs/
│   ├── figures/                       # กราฟ PNG ทั้งหมด
│   └── tables/                        # ตาราง export
└── docs/
    └── data_dictionary.md             # อธิบายทุก column
```

---

## วิธีการรันโค้ด

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. ดึงข้อมูลจาก API (ต้องเชื่อมต่อ Internet)

```bash
python src/01_data_collection.py
```

> **หมายเหตุ:** หากไม่สามารถเข้าถึง API ได้ สามารถใช้ข้อมูลจำลองแทน:
> ```bash
> python src/generate_simulated_data.py
> ```

### 3. ทำความสะอาดข้อมูล

```bash
python src/02_data_cleaning.py
```

### 4. รัน EDA Analysis

```bash
python src/03_eda_analysis.py
```

### 5. เปิด Jupyter Notebook

```bash
jupyter notebook mini_project_eda.ipynb
```

---

## 10 Insights (สรุป)

| # | Insight | คำถามวิจัย |
|---|---------|-----------|
| 1 | แผนที่ความเสี่ยง | สัดส่วนนำเข้าผ่าน Strait of Hormuz คิดเป็นกี่ %? |
| 2 | ดุลการค้า 4 วิกฤต | ดุลการค้าเปลี่ยนแปลงอย่างไรในแต่ละวิกฤต? |
| 3 | วิกฤตพลังงาน | นำเข้าพลังงานแพงขึ้นเพราะราคาหรือปริมาณ? |
| 4 | Domino Effect | ปุ๋ยแพง → ต้นทุนเกษตรสูง → ส่งออกเกษตรลด? |
| 5 | ประเทศคู่ขัดแย้ง | การค้ากับ Iran/GCC เปลี่ยนแปลงอย่างไร? |
| 6 | ยานยนต์/อิเล็กทรอนิกส์ | HS 85, 87 ได้รับผลกระทบทางอ้อม? |
| 7 | อาหารคือทอง | ส่งออกอาหารเพิ่มขึ้นช่วงวิกฤต? |
| 8 | ยางธรรมชาติ vs สังเคราะห์ | น้ำมันแพง → ยางไทยได้ประโยชน์? |
| 9 | Dependency Scorecard | สินค้านำเข้าใดเสี่ยงสูงสุด? |
| 10 | Diversification Roadmap | ลดพึ่งพา Middle East ได้อย่างไร? |

---

## เทคโนโลยีที่ใช้

- **Python 3.11+**
- **Pandas** & **NumPy** — Data manipulation
- **Matplotlib** & **Seaborn** — Visualization (Storytelling with Data approach)
- **Requests** — API data collection
- **OpenPyXL** — Excel file handling
- **SciPy** — Statistical analysis

---

## บทบาทของ AI ในโปรเจกต์นี้

AI (Claude) ถูกใช้เป็นเครื่องมือช่วยในการ:
1. **โครงสร้างโค้ด**: ช่วยวางโครงสร้างไฟล์และ functions
2. **Data Pipeline**: ช่วยเขียน script สำหรับ data collection, cleaning, และ EDA
3. **Visualization**: ช่วยสร้างกราฟตามมาตรฐาน Storytelling with Data
4. **Documentation**: ช่วยเขียน README, data dictionary

ทุก insight, สมมติฐาน, และการตีความผลลัพธ์เป็นผลงานของสมาชิกกลุ่ม

---

## อ้างอิง (References)

1. **แหล่งข้อมูล:** กระทรวงพาณิชย์, tradereport.moc.go.th
2. **หลักการ Visualization:** Cole Nussbaumer Knaflic, *Storytelling with Data* (2015)
3. **HS Code Reference:** World Customs Organization, Harmonized System

---

*DADS 5001: Data Analytics and Data Science Tools and Programming*
*National Institute of Development Administration (NIDA)*
