from app.database import SessionLocal
from app.models.news_model import News
from app.models.Categorie import Categorie
from datetime import datetime, timezone
import sys
import os

# Corriger les chemins si besoin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

db = SessionLocal()

# Récupérer les catégories
categories = db.query(Categorie).all()
if not categories:
    print("Aucune catégorie trouvée. Exécutez d'abord seed_categories.py.")
    sys.exit(1)

# Insérer les news en les liant aux catégories cycliquement
for i in range(1, 16):
    categorie = categories[(i - 1) % len(categories)]  # Répartition cyclique
    news = News(
        title=f"Actualité test n°{i}",
        content=f"Ceci est le contenu de l'actualité numéro {i}.",
        created_at=datetime.now(timezone.utc),
        categorie_id=categorie.id
    )
    db.add(news)

db.commit()
db.close()

print("15 actualités ont été insérées avec succès.")
