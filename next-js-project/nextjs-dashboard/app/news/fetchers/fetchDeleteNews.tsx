// fetchers/fetchDeleteNews.ts

import { Dispatch, SetStateAction } from "react";
import { News } from "../types";

export const fetchDeleteNews = async (
  newsId: number,
  setNewsList: Dispatch<SetStateAction<News[]>>
) => {
  const token = localStorage.getItem("token");

  const response = await fetch(`http://localhost:8000/news/${newsId}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  if (response.ok) {
    setNewsList((prev) => prev.filter((item) => item.id !== newsId));
  } else {
    throw new Error("Erreur lors de la suppression de l’actualité.");
  }
};
