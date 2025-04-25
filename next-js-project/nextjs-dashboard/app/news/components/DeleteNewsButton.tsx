import { IconButton } from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";
import { useDialog } from "@chakra-ui/react";
import { DeleteNewsButtonProps } from "../types";
import { fetchDeleteNews } from "../fetchers/fetchDeleteNews";
import CustomDialog from "./CustomDialog";
import { getScopesFromToken } from "../getScopesFromToken"; // 👈 à ajouter

const DeleteNewsButton = ({ newsId, setNewsList }: DeleteNewsButtonProps) => {
  const dialog = useDialog();

  // Lecture du token et vérification des droits
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const scopes = getScopesFromToken(token);
  const canDelete = scopes.includes("delete_news");

  if (!canDelete) return null; // 🔒 Ne rien afficher si non autorisé

  const handleDelete = async () => {
    try {
      await fetchDeleteNews(newsId, setNewsList);
      dialog.setOpen(false);
    } catch (error) {
      console.error("Erreur lors de la suppression :", error);
    }
  };

  return (
    <>
      <IconButton
        aria-label="Supprimer"
        size="sm"
        variant="surface"
        colorPalette="red"
        onClick={() => dialog.setOpen(true)}
      >
        <DeleteIcon />
      </IconButton>

      <CustomDialog
        dialog={dialog}
        title="Supprimer l’actualité"
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        danger
        onConfirm={handleDelete}
        onCancel={() => dialog.setOpen(false)}
      >
        Êtes-vous sûr de vouloir supprimer cette actualité ?
      </CustomDialog>
    </>
  );
};

export default DeleteNewsButton;
