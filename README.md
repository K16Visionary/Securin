🔐 CVE Data Management & Visualization System
This project fetches CVE (Common Vulnerabilities and Exposures) information from the NVD API, cleans and deduplicates the data, stores it in a MySQL database, provides APIs for filtering, and displays the results in a clean, interactive web UI.

✅ Features Implemented
📥 CVE Data Ingestion
          Fetches all CVE data using startIndex and resultsPerPage from the NVD API.
          Stores the data in a MySQL database using SQLAlchemy ORM.
          Cleans and deduplicates records before inserting them into the DB.

🔍 API Endpoints
  Base route: /cves/list

📊 Web UI
  Displays data in an HTML table with:

CVE ID

  Identifier

  Published Date

  Last Modified Date

  Status

  Shows Total Records.

Includes pagination options: 10 (default), 50, 100 results per page.

Supports server-side date sorting
🔄 Technologies Used
Backend: Python, Flask, SQLAlchemy, MySQL

Frontend: HTML, CSS, JavaScript (Vanilla)

API: NVD CVE 2.0 API

Testing: (Planned) PyTest

🚀 How to Run the Project
1️⃣ Setup
bash
Copy
Edit
# Clone the repo
git clone https://github.com/yourusername/cve-data-visualizer.git
cd cve-data-visualizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2️⃣ MySQL Setup
Create a MySQL database (e.g., cvedb).

Update the connection string in sync_cves.py and app.py:

python
Copy
Edit
engine = create_engine("mysql+pymysql://username:password@localhost/cvedb")
3️⃣ Run the Data Sync
bash
Copy
Edit
python sync_cves.py
4️⃣ Start Flask Server
bash
Copy
Edit
python app.py
Visit http://localhost:5000/cves/list to view the CVE data UI.

<img width="1847" height="1089" alt="image" src="https://github.com/user-attachments/assets/3b51ca25-ef52-48a9-a646-81ca954223f0" />


