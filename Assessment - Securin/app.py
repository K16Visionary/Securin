import requests
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import insert
from datetime import datetime
from dateutil.parser import isoparse

# MySQL Connection
engine = create_engine("mysql+mysqlconnector://root:6411@localhost/nvd")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#CVE Model
class CVE(Base):
    __tablename__ = "cves"
    id = Column("ID", String(30), primary_key=True)
    identifier = Column(String(100))
    published_date = Column(DateTime)
    last_modified_date = Column(DateTime)
    status = Column(String(50))

   
    __table_args__ = {
        'mysql_row_format': 'DYNAMIC',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

# Create table
Base.metadata.create_all(engine)

#Fetch & Store CVEs LIMITED 1000
def sync_cves():
    session = SessionLocal()
    start_index = 0
    max_index = 1000
    results_per_page = 100

    while start_index < max_index:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?startIndex={start_index}&resultsPerPage={results_per_page}"
        try:
            res = requests.get(url)
            data = res.json()
        except Exception as e:
            print("❌ API request failed:", e)
            break

        items = data.get("vulnerabilities", [])
        if not items:
            break

        for item in items:
            cve = item.get("cve", {})
            cve_id = cve.get("id")
            if not cve_id:
                continue

            published = cve.get("published")
            last_modified = cve.get("lastModified")
            cve_data = {
                "id": cve_id,
                "identifier": cve.get("sourceIdentifier"),
                "published_date": isoparse(published) if published else None,
                "last_modified_date": isoparse(last_modified) if last_modified else None,
                "status": cve.get("vulnStatus")
            }
            
            insert_stmt = insert(CVE).values(**cve_data)
            upsert_stmt = insert_stmt.on_duplicate_key_update(**cve_data)

            try:
                session.execute(upsert_stmt)
            except Exception as e:
                print(f"❌ Error inserting {cve_id}:", e)

        session.commit()
        print(f"✅ Synced {min(start_index + results_per_page, max_index)}/1000")
        start_index += results_per_page

    session.close()
    print("🎉 Sync (first 1000 CVEs) complete")

if __name__ == "__main__":
    sync_cves()
