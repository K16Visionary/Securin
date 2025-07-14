from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import or_

app = Flask(__name__)

# MySQL connection
engine = create_engine("mysql+mysqlconnector://root:6411@localhost/nvd")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class CVE(Base):
    __tablename__ = "cves"
    id = Column("ID", String(30), primary_key=True)
    identifier = Column(String(100))
    published_date = Column(DateTime)
    last_modified_date = Column(DateTime)
    status = Column(String(50))

@app.route('/cves')
@app.route('/cves/list')
def cves_list_page():
    return render_template("cves_list.html")

@app.route('/cves/<cve_id>')
def cve_detail_page(cve_id):
    return render_template("cve_detail.html", cve_id=cve_id)

@app.route('/api/cves')
def get_cves():
    session = SessionLocal()
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit

        total = session.query(CVE).count()
        cves = session.query(CVE).order_by(CVE.published_date.desc()).offset(offset).limit(limit).all()

        data = [{
            "ID": cve.id,
            "IDENTIFIER": cve.identifier,
            "PUBLISHED DATE": cve.published_date.strftime("%Y-%m-%d") if cve.published_date else "",
            "LAST MODIFIED DATE": cve.last_modified_date.strftime("%Y-%m-%d") if cve.last_modified_date else "",
            "STATUS": cve.status
        } for cve in cves]

        return jsonify({"total": total, "data": data})
    finally:
        session.close()

@app.route('/api/cves/search')
def search_cves():
    session = SessionLocal()
    try:
        query = request.args.get("q", "").strip().lower()
        if not query:
            return jsonify({"total": 0, "data": []})

        like_query = f"%{query}%"

        results = session.query(CVE).filter(
            or_(
                CVE.id.ilike(like_query),
                CVE.identifier.ilike(like_query),
                CVE.status.ilike(like_query)
            )
        ).limit(100).all()

        data = [{
            "ID": cve.id,
            "IDENTIFIER": cve.identifier,
            "PUBLISHED DATE": cve.published_date.strftime("%Y-%m-%d") if cve.published_date else "",
            "LAST MODIFIED DATE": cve.last_modified_date.strftime("%Y-%m-%d") if cve.last_modified_date else "",
            "STATUS": cve.status
        } for cve in results]

        return jsonify({"total": len(data), "data": data})
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/api/cves')
def get_cves():
    session = SessionLocal()
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        sort = request.args.get("sort", "desc").lower()
        offset = (page - 1) * limit

        query = session.query(CVE)

        # Sort by date
        if sort == "asc":
            query = query.order_by(CVE.published_date.asc())
        else:
            query = query.order_by(CVE.published_date.desc())

        total = query.count()
        cves = query.offset(offset).limit(limit).all()

        data = [{
            "id": cve.id,
            "identifier": cve.identifier,
            "published": cve.published_date.strftime("%Y-%m-%d") if cve.published_date else "",
            "last_modified": cve.last_modified_date.strftime("%Y-%m-%d") if cve.last_modified_date else "",
            "status": cve.status
        } for cve in cves]

        return jsonify({"total": total, "data": data})
    finally:
        session.close()
