"use client";

import { useEffect, useState } from "react";
import { Box, Heading, Stack, Text } from "@chakra-ui/react";
import { useRouter } from "next/navigation";
import { News, Cat } from "../types";
import fetchGetNews from "../fetchers/fetchGetNews";
import fetchGetCategories from "../fetchers/fetchGetCategories";
import NavigationBoutons from "@/components/navigationBoutons";
import AddNews from "./AddNews";
import NewsList from "./NewsList";
import Pagination from "./Pagination";
import SearchBar from "./SearchBar";
import CategoryFilter from "./CategoryFilter";

const Container = () => {
  const router = useRouter();
  const [newsList, setNewsList] = useState<News[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const limit = 5;
  const totalPages = Math.ceil(total / limit);
  const hasMore = currentPage < totalPages;
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [categories, setCategories] = useState<Cat[]>([]);
  const [categorie, setCategorie] = useState<Cat | null>(null);

  // Récupère les catégories une seule fois
  useEffect(() => {
    fetchGetCategories()
      .then(setCategories)
      .catch((err) => {
        console.error("Erreur chargement catégories :", err);
        setCategories([]);
      });
  }, []);

  // Récupère les news en fonction de la catégorie, recherche, page
  useEffect(() => {
    (async () => {
      try {
        const offset = (currentPage - 1) * limit;
        const { news, total } = await fetchGetNews({
          limit,
          offset,
          search: debouncedSearch,
          categorie, //  objet Cat ou null
        });
        setNewsList(news);
        setTotal(total);
      } catch (error) {
        console.error("Erreur lors du rechargement des actualités :", error);
      }
    })();

    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentPage, debouncedSearch, categorie]);

  // Recherche avec délai
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
      setCurrentPage(1);
    }, 500);

    return () => clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    setCurrentPage(1);
  }, [categorie]);
  
  useEffect(() => {
    const maxPage = Math.max(1, Math.ceil(total / limit));
    if (currentPage > maxPage) {
      setCurrentPage(maxPage);
    }
  }, [total]);

  return (
    <Box p={8}>
      <Stack direction="column">
        <Heading>Actualités</Heading>

        <NavigationBoutons onAccueilClick={() => router.push("/home")} />
        <SearchBar value={search} onChange={(e) => setSearch(e.target.value)} />
        <AddNews onNewsAdded={setNewsList} categories={categories} selectedCategorie={categorie?.name} />

        <CategoryFilter
          selected={categorie}
          onSelect={setCategorie}
          categories={categories}
        />

        <Text fontSize="md" fontWeight="semibold" mt={2}>
          Catégorie : {categorie ? categorie.name : "Toutes les catégories"}
        </Text>

        <Text fontSize="lg" fontWeight="bold" mt={8}>
          Liste des actualités
        </Text>

        <NewsList newsList={newsList} setNewsList={setNewsList} categories={categories} selectedCategorie={categorie?.name} />
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
          hasMore={hasMore}
        />
      </Stack>
    </Box>
  );
};

export default Container;