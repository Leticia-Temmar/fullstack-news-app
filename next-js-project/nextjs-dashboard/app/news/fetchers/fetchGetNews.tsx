import { News, Cat } from "../types";

interface FetchGetNewsParams {
  limit?: number;
  offset?: number;
  search?: string;
  categorie?: Cat | null;
}

interface FetchGetNewsResponse {
  news: News[];
  total: number;
}

const fetchGetNews = async ({
  limit = 5,
  offset = 0,
  search,
  categorie,
}: FetchGetNewsParams): Promise<FetchGetNewsResponse> => {
  let url: URL;
  console.log("Catégorie envoyée :", categorie);
  if (!categorie) {
    url = new URL("http://localhost:8000/news");
  } else {
    url = new URL(`http://localhost:8000/news/category/${categorie.id}`);
  }

  url.searchParams.append("limit", limit.toString());
  url.searchParams.append("offset", offset.toString());

  if (search?.trim()) {
    url.searchParams.append("search", search);
  }

  const response = await fetch(url.toString());

  if (!response.ok) {
    throw new Error("Erreur lors de la récupération des actualités.");
  }

  return await response.json();
};
export default fetchGetNews;