
import { VStack, Text } from "@chakra-ui/react";
import { NewsListProps } from "../types";
import NewsCard from "./NewsCard";


const NewsList = ({ newsList, setNewsList, categories , selectedCategorie }: NewsListProps) => {
  if (newsList.length === 0) {
    return <Text mt={4} textAlign="center" width="100%">Oups 😵‍💫 ! Aucune actualité trouvée. </Text>;
  }
  return (
    <VStack align="stretch" mt={4}>
      {newsList.map((news) => (
        <NewsCard key={news.id} news={news} setNewsList={setNewsList} categories={categories} selectedCategorie={selectedCategorie} />
      ))}
    </VStack>
  );
};

export default NewsList;