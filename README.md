# 🔐 CVE Data Management & Visualization System

This project fetches CVE (Common Vulnerabilities and Exposures) data from the **NVD API**, deduplicates and stores it in a **MySQL** database, and presents it through a clean, interactive **Flask-based web interface**.

---

## ✅ Features

### 📥 CVE Data Ingestion
- Fetches all CVE data using `startIndex` and `resultsPerPage` from the [NVD CVE 2.0 API](https://nvd.nist.gov/developers/vulnerabilities).
- Cleans and deduplicates data before inserting into the DB.
- Uses **SQLAlchemy ORM** to manage the MySQL database.

### 🔍 API Endpoints
- `GET /cves/list`  
  Returns paginated, filterable, and sortable CVE data.

### 📊 Web UI
- Displays CVE entries in an interactive HTML table.
- Columns include:
  - **CVE ID**
  - **Identifier**
  - **Published Date**
  - **Last Modified Date**
  - **Status**
- Supports:
  - Server-side pagination: `10` (default), `50`, `100` results per page.
  - Server-side sorting by date fields.
  - Record count display.

---

## 🧠 Project Workflow

1. **Fetch CVE Data from NVD API**
   - Using `startIndex` and `resultsPerPage` for pagination.
   - Raw JSON is parsed and cleaned.

2. **Store Structured Data in MySQL**
   - Each CVE record is inserted after deduplication.
   - Tables are created using **SQLAlchemy ORM**.

3. **Display Data on UI**
   - Data is retrieved from the MySQL DB using Flask API.
   - Rendered in a paginated HTML table using vanilla JS.

4. **View Details by Clicking a Record**
   - When a user clicks a CVE ID (or any specific field),
   - It triggers a frontend action that **calls the live NVD API** to fetch **full CVE details** and display them dynamically.

---

## 🔄 Tech Stack

| Layer      | Technology                      |
|------------|----------------------------------|
| Backend    | Python, Flask, SQLAlchemy        |
| Database   | MySQL                            |
| Frontend   | HTML, CSS, JavaScript (Vanilla)  |
| API Source | NVD CVE 2.0 API                  |
| Testing    | (Planned) PyTest                |

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/cve-data-visualizer.git
cd cve-data-visualizer
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ MySQL Setup
- Create a MySQL database (e.g., `cvedb`)
- Update the DB connection string in `sync_cves.py` and `app.py`:

```python
engine = create_engine("mysql+pymysql://username:password@localhost/cvedb")
```

### 5️⃣ Sync CVE Data
```bash
python sync_cves.py
```

### 6️⃣ Run the Flask App
```bash
python app.py
```

- Visit [http://localhost:5000/cves/list](http://localhost:5000/cves/list) to access the CVE UI.

---

## 📸 Screenshots

<img src="https://github.com/user-attachments/assets/3b51ca25-ef52-48a9-a646-81ca954223f0" alt="Screenshot 1" width="100%" />

<img src="https://github.com/user-attachments/assets/c7b6d0e5-379f-42d5-9005-d9a9da76f696" alt="Screenshot 2" width="100%" />

<img src="https://github.com/user-attachments/assets/1a4f01c8-b92c-4168-9532-ed6d5a36a475" alt="Screenshot 3" width="100%" />

![466123828-eca2c7ae-2151-4636-986d-c8b050812ce9](https://github.com/user-attachments/assets/8f27f8f7-356f-4951-a60a-cf36e3069071)


---

## 🛠️ Points Implemented
    1. Render CPEs in a table with specific columns and formatting
    2. Field-level filtering using the /search API
    3. Pagination with customizable results per page (15 to 50)
    4. Fallback screen when no results are found
    5. Fallback screen when no data is available

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---
