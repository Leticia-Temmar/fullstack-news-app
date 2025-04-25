from pydantic import BaseModel
from typing import List

# Base pour les entrées (POST)
class CategorieBase(BaseModel):
    name: str

# Pour la création
class CategorieCreate(CategorieBase):
    pass

# Pour la sortie (GET, etc.)
class CategorieOut(CategorieBase):
    id: int

    model_config = {
        "from_attributes": True
    }
