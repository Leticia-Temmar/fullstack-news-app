// fetchers/fetchGetCategories.ts

import { Cat } from "../types";

const fetchGetCategories = async (): Promise<Cat[]> => {
    const response = await fetch("http://localhost:8000/categories");

    if (!response.ok) {
        throw new Error("Erreur lors de la récupération des catégories");
    }

    return await response.json();
};

export default fetchGetCategories;
