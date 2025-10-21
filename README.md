Sure! Here’s a **README.md** for your **Assignment-2 ETL project** formatted like your CISA KEV example:

````markdown
---

# MITRE ATT&CK ETL Data Connector - Assignment 2

This project extracts data from the **MITRE ATT&CK** Enterprise, Mobile, and ICS endpoints, transforms it into a structured format, and loads it into **MongoDB**.  
It is designed for cybersecurity threat intelligence ingestion and analysis.

---

## 1. Clone the Repository

```bash
git clone https://github.com/Kyureeus-Edtech/custom-python-etl-data-connector-iniyadharshini.git
cd custom-python-etl-data-connector-iniyadharshini
````

---

## 2. Create and Activate Virtual Environment

**Windows (CMD or PowerShell)**:

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create and Configure `.env` File

The `.env` file stores **private configuration values** for the ETL script.
It should be placed in the **root folder** of the project (next to `etl_mitre_connector.py`).

**Example `.env` file:**

```env
# MongoDB Configuration
MONGO_URI=your_mongodb_connection_string_here
DB_NAME=your_database_name_here
COLLECTION_ENTERPRISE=enterprise_collection_name
COLLECTION_MOBILE=mobile_collection_name
COLLECTION_ICS=ics_collection_name

# MITRE ATT&CK Endpoints
ENTERPRISE_URL=https://cti-taxii.mitre.org/stix/enterprise
MOBILE_URL=https://cti-taxii.mitre.org/stix/mobile
ICS_URL=https://cti-taxii.mitre.org/stix/ics
```

---

## 5. Run the ETL Script

```bash
python etl_mitre_connector.py
```

The script will:

* Connect to MITRE ATT&CK Enterprise, Mobile, and ICS STIX endpoints
* Extract and parse the STIX data
* Transform it into MongoDB-compatible format
* Insert or update records in MongoDB collections

---

## 6. Verify Data in MongoDB

If MongoDB is running locally:

```bash
mongo
use your_database_name
db.enterprise_collection_name.find().pretty()
db.mobile_collection_name.find().pretty()
db.ics_collection_name.find().pretty()
```

---


```
