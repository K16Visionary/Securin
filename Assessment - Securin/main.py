from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

# MySQL connection
engine = create_engine("mysql+mysqlconnector://root:6411@localhost/nvd")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class CVE(Base):
    __tablename__ = "cves"
    id = Column(String(30), primary_key=True)
    published = Column(DateTime)
    last_modified = Column(DateTime)
    description = Column(String(5000))
    score = Column(Float)
    year = Column(Integer)

#Web routes for the UI
@app.route('/cves')
@app.route('/cves/list')
def cves_list_page():
    return render_template("cves_list.html")

@app.route('/cves/<cve_id>')
def cve_detail_page(cve_id):
    return render_template("cve_detail.html")

#API route for frontend JS
@app.route('/api/cves')
def get_cves():
    session = SessionLocal()
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit

        total = session.query(CVE).count()
        cves = session.query(CVE).order_by(CVE.published.desc()).offset(offset).limit(limit).all()

        data = [{
            "id": c.id,
            "published": c.published.strftime("%Y-%m-%d") if c.published else "",
            "description": c.description,
            "score": c.score,
            "year": c.year
        } for c in cves]

        return jsonify({"total": total, "data": data})
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
