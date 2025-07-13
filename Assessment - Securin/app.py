import requests
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import insert
from datetime import datetime
from dateutil.parser import isoparse

# MySQL Connection
engine = create_engine("mysql+mysqlconnector://root:Yourpassword@localhost/nvd")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#CVE Model
class CVE(Base):
    __tablename__ = "cves"
    id = Column(String(30), primary_key=True)
    published = Column(DateTime)
    last_modified = Column(DateTime)
    description = Column(String(5000))
    score = Column(Float)
    year = Column(Integer)

# Create table if it doesn't exist
Base.metadata.create_all(engine)

#Fetch & Store CVEs (LIMITED TO FIRST 1000)
def sync_cves():
    session = SessionLocal()
    start_index = 0
    max_index = 1000  # stop after 1000 records
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
            description = next((d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"), "")
            score = cve.get("metrics", {}).get("cvssMetricV3", [{}])[0].get("cvssData", {}).get("baseScore", 0.0)
            year = int(cve_id.split("-")[1]) if cve_id and "-" in cve_id else None

            insert_stmt = insert(CVE).values(
                id=cve_id,
                published=isoparse(published) if published else None,
                last_modified=isoparse(last_modified) if last_modified else None,
                description=description,
                score=score,
                year=year
            )

            upsert_stmt = insert_stmt.on_duplicate_key_update(
                published=insert_stmt.inserted.published,
                last_modified=insert_stmt.inserted.last_modified,
                description=insert_stmt.inserted.description,
                score=insert_stmt.inserted.score,
                year=insert_stmt.inserted.year
            )

            try:
                session.execute(upsert_stmt)
            except Exception as e:
                print(f"❌ Error inserting {cve_id}:", e)

        session.commit()
        print(f"✅ Synced {min(start_index + results_per_page, max_index)}/1000")
        start_index += results_per_page

    session.close()
    print("🎉 Sync (first 1000 CVEs) complete")

# Run the sync
if __name__ == "__main__":
    sync_cves()
