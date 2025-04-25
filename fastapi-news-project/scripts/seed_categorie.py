from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.Categorie import Categorie
from app.models.news_model import News

db: Session = SessionLocal()

default_categories = ["Politique", "Economie", "Science", "Sport"]

for name in default_categories:
    if not db.query(Categorie).filter_by(name=name).first():
        db.add(Categorie(name=name))

db.commit()
db.close()
print("Catégories insérées.")
