// components/AddNews.tsx
import {
  Box,
  Input,
  Stack,
  Textarea,
  IconButton,
  Text,
} from "@chakra-ui/react";
import { AddIcon } from "@chakra-ui/icons";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { AddNewsProps, Cat } from "../types";
import fetchAddNews from "../fetchers/fetchAddNews";
import SelectCategory from "./SelectCategory";
import { getScopesFromToken } from "../getScopesFromToken";

const schema = z.object({
  title: z.string().min(1, "Titre requis"),
  content: z.string().min(1, "Contenu requis"),
  categorie_id: z.string().min(1, "Catégorie requise"),
});

type FormValues = z.infer<typeof schema>;

interface Props extends AddNewsProps {
  categories: Cat[];
  selectedCategorie?: string; // ← nouvelle prop
}

const AddNews = ({ onNewsAdded, categories, selectedCategorie }: Props) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const scopes = getScopesFromToken(token);
  const canAdd = scopes.includes("create_news");

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      title: "",
      content: "",
      categorie_id: "",
    },
  });

  const onSubmit = async (data: FormValues) => {
    try {
      const newNews = await fetchAddNews({
        title: data.title,
        content: data.content,
        categorie_id: Number(data.categorie_id),
      });

      // Ajouter seulement si la catégorie affichée correspond à celle de la news, ou si filtre sur "Tous"
      if (!selectedCategorie || selectedCategorie === "Tous" || selectedCategorie === newNews.categorie.name) {
        onNewsAdded((prevList) => [newNews, ...prevList]);
      }

      reset();
    } catch (err) {
      console.error("Erreur lors de l'ajout :", err);
    }
  };

  if (!canAdd) return null;

  return (
    <Box mt={6}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack>
          <Controller
            control={control}
            name="title"
            render={({ field }) => (
              <Input placeholder="Titre de l’actualité" {...field} />
            )}
          />
          {errors.title && <Text color="red.500">{errors.title.message}</Text>}

          <Controller
            control={control}
            name="content"
            render={({ field }) => (
              <Textarea placeholder="Contenu de l’actualité" {...field} />
            )}
          />
          {errors.content && (
            <Text color="red.500">{errors.content.message}</Text>
          )}

          <Controller
            control={control}
            name="categorie_id"
            render={({ field }) => (
              <SelectCategory
                listCategory={categories}
                value={field.value}
                onChange={field.onChange}
              />
            )}
          />
          {errors.categorie_id && (
            <Text color="red.500">{errors.categorie_id.message}</Text>
          )}

          <IconButton
            aria-label="Ajouter"
            type="submit"
            alignSelf="start"
            colorPalette="blue"
            variant="surface"
          >
            <AddIcon />
          </IconButton>
        </Stack>
      </form>
    </Box>
  );
};

export default AddNews;
