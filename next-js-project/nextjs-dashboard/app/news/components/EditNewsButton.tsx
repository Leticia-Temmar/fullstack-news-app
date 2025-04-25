import {
  IconButton,
  Input,
  Stack,
  Textarea,
  AlertRoot,
  AlertContent,
  AlertTitle,
  AlertDescription,
} from "@chakra-ui/react";
import { WarningIcon, EditIcon } from "@chakra-ui/icons";
import { useState } from "react";
import { EditNewsButtonProps } from "../types";
import CustomDialog from "./CustomDialog";
import { useDialog } from "@chakra-ui/react";
import fetchEditNews from "../fetchers/fetchEditNews";
import { getScopesFromToken } from "../getScopesFromToken";
import SelectCategory from "./SelectCategory";

const EditNewsButton = ({ news, setNewsList, categories, selectedCategorie }: EditNewsButtonProps) => {
  const dialog = useDialog();

  const [newTitle, setNewTitle] = useState(news.title);
  const [newContent, setNewContent] = useState(news.content);
  const [newCategorieId, setNewCategorieId] = useState(news.categorie_id.toString());
  const [error, setError] = useState("");

  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const scopes = getScopesFromToken(token);
  const canEdit = scopes.includes("update_news");
  const handleEditConfirm = async () => {
    try {
      await fetchEditNews(news.id!, {
        title: newTitle,
        content: newContent,
        categorie_id: Number(newCategorieId),
      });
  
      // Mise à jour locale sans dépendre d'un retour backend
      const updatedCategoryName = categories.find(cat => cat.id === Number(newCategorieId))?.name;
  
      setNewsList((prev) =>
        selectedCategorie === "Tous" || !selectedCategorie || selectedCategorie === updatedCategoryName
          ? prev.map((n) =>
              n.id === news.id
                ? {
                    ...n,  
                    title: newTitle,
                    content: newContent,
                    categorie_id: Number(newCategorieId),
                    categorie: {
                      ...n.categorie,
                      name: updatedCategoryName || "",
                    },
                  }
                : n
            )
          : prev.filter((n) => n.id !== news.id)
      );
  
      dialog.setOpen(false);
      setError("");
    } catch (err: any) {
      setError(err.message || "Erreur inconnue");
    }
  };
  

  if (!canEdit) return null;

  return (
    <>
      <IconButton
        aria-label="Modifier"
        size="sm"
        variant="surface"
        colorPalette="teal"
        onClick={() => dialog.setOpen(true)}
      >
        <EditIcon />
      </IconButton>

      <CustomDialog
        dialog={dialog}
        title="Modifier l’actualité"
        confirmLabel="Enregistrer"
        cancelLabel="Annuler"
        onConfirm={handleEditConfirm}
        onCancel={() => {
          dialog.setOpen(false);
          setNewTitle(news.title);
          setNewContent(news.content);
          setNewCategorieId(news.categorie_id.toString());
          setError("");
        }}
      >
        <Stack mt={4}>
          {error && (
            <AlertRoot status="error" variant="subtle">
              <WarningIcon style={{ marginRight: "8px" }} />
              <AlertContent>
                <AlertTitle>Erreur</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </AlertContent>
            </AlertRoot>
          )}

          <Input
            placeholder="Titre"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
          />

          <Textarea
            placeholder="Contenu"
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
          />

          <SelectCategory
            listCategory={categories}
            value={newCategorieId}
            onChange={setNewCategorieId}
          />
        </Stack>
      </CustomDialog>
    </>
  );
};

export default EditNewsButton;