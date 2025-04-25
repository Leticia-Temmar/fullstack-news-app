// components/NewsCard.tsx

import { Box, Flex, Heading, Text, Badge, } from "@chakra-ui/react";
import { NewsCardProps } from "../types";
import EditNewsButton from "./EditNewsButton";
import DeleteNewsButton from "./DeleteNewsButton";

// Mapping des couleurs selon le nom de la catégorie
const getCategoryColor = (name: string) => {
  const key = name.trim().toLowerCase();
  const map: Record<string, string> = {
    politique: "red",
    economie: "green",
    science: "blue",
    sport: "orange",
  };
  return map[key] || "teal";
};


const formatDate = (rawDate: string) => {
  const date = new Date(rawDate);
  const jour = String(date.getDate()).padStart(2, "0");
  const mois = String(date.getMonth() + 1).padStart(2, "0");
  const annee = date.getFullYear();
  const heures = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${jour}/${mois}/${annee} à ${heures}:${minutes}`;
};

const NewsCard = ({ news, setNewsList, categories, selectedCategorie}: NewsCardProps) => {
  const color = getCategoryColor(news.categorie?.name || "");

  return (
    <Box
      borderWidth="1px"
      borderRadius="xl"
      p={4}
      boxShadow="md"
      position="relative"
    >
      {/* Boutons en haut à droite */}
      <Flex position="absolute" top={2} right={2} gap={2}>
        <EditNewsButton news={news} setNewsList={setNewsList} categories={categories} selectedCategorie={selectedCategorie}/>
        <DeleteNewsButton newsId={news.id!} setNewsList={setNewsList} />
      </Flex>

      {/* Badge de catégorie */}
      {news.categorie?.name && (
        <Badge
          bg={`${color}.100`}
          color={`${color}.800`}
          borderRadius="full"
          px={3}
          py={1}
          mb={2}
          fontWeight="bold"
          width="fit-content"
        >
          {news.categorie.name}
        </Badge>
      )}

      {/* Contenu de la news */}
      <Heading size="md">{news.title}</Heading>
      <Text mt={2}>{news.content}</Text>
      {news.created_at && (
        <Text fontSize="sm" color="gray.500" textAlign="right" mt={2}>
          🕒 Ajoutée le {formatDate(news.created_at)}
        </Text>
      )}
    </Box>
  );
};

export default NewsCard;