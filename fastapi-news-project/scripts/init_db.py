from app.database import Base, engine
from app.models import auth, news_model, Categorie

Base.metadata.create_all(bind=engine)
print("Toutes les tables ont été créées.")
