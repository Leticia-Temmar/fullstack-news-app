import { News } from "../types";

interface EditNewsInput {
  title: string;
  content: string;
  categorie_id: number;
}

const fetchEditNews = async (
  newsId: number,
  { title, content, categorie_id }: EditNewsInput
): Promise<void> => {
  const token = localStorage.getItem("token");

  const response = await fetch(`http://localhost:8000/news/${newsId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ title, content, categorie_id }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Erreur lors de la modification.");
  }
};

export default fetchEditNews;
