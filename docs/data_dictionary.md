# Data Dictionary — Thailand Trade Impact Analysis

## DADS 5001 Mini-Project | DADS, NIDA

**Data Source:** tradereport.moc.go.th (Ministry of Commerce, Thailand)
**API:** dataapi.moc.go.th (MOC Open Data API)

---

## Raw Data Columns

### trade_overview.csv (Dataset 1: Trade Overview)

| Column | Type | Description |
|--------|------|-------------|
| `country_eng` | String | Country name in English |
| `import_value_usd` | Float | Thailand's import value from this country (USD) |
| `import_value_baht` | Float | Thailand's import value from this country (THB) |
| `export_value_usd` | Float | Thailand's export value to this country (USD) |
| `export_value_baht` | Float | Thailand's export value to this country (THB) |
| `trade_value_usd` | Float | Total trade value = import + export (USD) |
| `trade_balance_usd` | Float | Trade balance = export - import (USD) |
| `year` | Integer | Calendar year (2019-2026) |
| `month` | Integer | Calendar month (1-12) |
| `data_type` | String | Always "overview" |

### Harmonize Data (Datasets 2-6)

Used by: energy_imports.csv, fertilizer_imports.csv, agrifood_exports.csv, industrial_exports.csv, petrochemical_imports.csv

| Column | Type | Description |
|--------|------|-------------|
| `country_eng` | String | Country name in English |
| `value_usd` | Float | Trade value in USD |
| `value_baht` | Float | Trade value in Thai Baht |
| `quantity` | Float | Trade quantity |
| `quantity_unit` | String | Unit of quantity (e.g., KGM = kilograms) |
| `year` | Integer | Calendar year (2019-2026) |
| `month` | Integer | Calendar month (1-12) |
| `hs_code` | String | Harmonized System tariff code (2-digit) |
| `hs_description` | String | Description of HS code |
| `data_type` | String | "import" or "export" |

---

## HS Code Reference

| HS Code | Description (EN) | Description (TH) | Dataset |
|---------|------------------|-------------------|---------|
| 27 | Mineral Fuels (Oil, Gas, Coal) | เชื้อเพลิงแร่ น้ำมันดิบ LNG LPG | energy_imports |
| 29 | Organic Chemicals (Naphtha) | เคมีอินทรีย์/แนฟทา | petrochemical_imports |
| 31 | Fertilizers | ปุ๋ยเคมี | fertilizer_imports |
| 10 | Cereals (Rice) | ข้าว | agrifood_exports |
| 16 | Prepared Meat/Fish (Canned Food) | อาหารแปรรูป/กระป๋อง | agrifood_exports |
| 17 | Sugars | น้ำตาล | agrifood_exports |
| 40 | Rubber & Articles | ยางพาราและผลิตภัณฑ์ | agrifood_exports |
| 85 | Electrical Machinery & Electronics | เครื่องจักรไฟฟ้าและอิเล็กทรอนิกส์ | industrial_exports |
| 87 | Vehicles & Parts | ยานยนต์และชิ้นส่วน | industrial_exports |
| 39 | Plastics & Articles | พลาสติกและผลิตภัณฑ์ | industrial_exports |

---

## Engineered Columns (Clean Data)

| Column | Type | Description |
|--------|------|-------------|
| `date` | Datetime | First day of year-month (YYYY-MM-01) |
| `year_month` | String | "YYYY-MM" format for labels |
| `region` | String | Geographic region classification |
| `shipping_route` | String | Maritime shipping route classification |
| `crisis_period` | String | Crisis period classification |
| `unit_price_usd` | Float | value_usd / quantity (for harmonize data) |
| `yoy_change_pct` | Float | Year-over-year % change in value_usd |
| `mom_change_pct` | Float | Month-over-month % change in value_usd |
| `is_outlier` | Boolean | True if value is an outlier (IQR method) |
| `dataset` | String | Source dataset name |

---

## Region Classification

| Region | Countries |
|--------|-----------|
| Middle East - Hormuz | Iran, Iraq, Kuwait, Qatar, UAE, Bahrain, Saudi Arabia, Oman |
| Middle East - Non-Hormuz | Israel, Jordan, Lebanon, Yemen, Syria, Turkey, Egypt |
| ASEAN | Malaysia, Singapore, Indonesia, Vietnam, Philippines, Myanmar, Cambodia, Laos, Brunei |
| East Asia | China, Japan, South Korea, Taiwan, Hong Kong |
| South Asia | India, Bangladesh, Pakistan, Sri Lanka |
| Europe | Germany, UK, France, Italy, Netherlands, Spain, Belgium, Switzerland, Sweden, Poland, Russia |
| Americas | USA, Canada, Brazil, Mexico, Argentina, Chile, Colombia, Peru |
| Africa | South Africa, Nigeria, Kenya, Ghana, Morocco, Algeria, Libya, Tanzania |
| Oceania | Australia, New Zealand |

---

## Shipping Route Classification

| Route | Description | Regions |
|-------|-------------|---------|
| Via Hormuz | Through Strait of Hormuz | Middle East - Hormuz |
| Via Suez/Red Sea | Through Suez Canal & Red Sea | Europe, Middle East - Non-Hormuz |
| Via Cape of Good Hope | Around southern Africa | Americas, Africa |
| Pacific/Direct | Direct Pacific routes | ASEAN, East Asia, South Asia, Oceania |

---

## Crisis Period Classification

| Period | Date Range | Description |
|--------|------------|-------------|
| Pre-COVID | Before 2020-03 | Normal period baseline |
| COVID-19 | 2020-03 to 2021-12 | COVID-19 pandemic disruption |
| Post-COVID | 2022-01 | Brief recovery period |
| Russia-Ukraine | 2022-02 to 2023-09 | Russia-Ukraine war, energy crisis |
| Post-RU War | 2023-10 to 2025-05 | Stabilization period |
| 12-Day War | 2025-06 | Brief Israel-Hezbollah conflict |
| Post-12-Day | 2025-07 to 2026-01 | Recovery period |
| Iran War | 2026-02 onward | US-Israel vs Iran conflict, Hormuz disruption |

---

## Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| HS | Harmonized System (international tariff classification) |
| GCC | Gulf Cooperation Council (Saudi Arabia, UAE, Kuwait, Qatar, Bahrain, Oman) |
| ASEAN | Association of Southeast Asian Nations |
| YoY | Year-over-Year |
| MoM | Month-over-Month |
| USD | United States Dollar |
| THB | Thai Baht |
| KGM | Kilograms |
| LNG | Liquefied Natural Gas |
| LPG | Liquefied Petroleum Gas |
| MOC | Ministry of Commerce (Thailand) |
| IQR | Interquartile Range |
