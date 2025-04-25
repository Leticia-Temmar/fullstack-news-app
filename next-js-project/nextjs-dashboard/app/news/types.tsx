
import { Dispatch, SetStateAction, ReactNode } from "react";
import { UseDialogReturn } from "@chakra-ui/react";
export interface News {
  id?: number;
  title: string;
  content: string;
  created_at?: string;
  categorie_id: number;
  categorie: {
    id: number;
    name: string;
  };
}

export interface AddNewsProps {
  onNewsAdded: Dispatch<SetStateAction<News[]>>;
  categories: Cat[];
}

export interface NewsListProps {
  newsList: News[];
  setNewsList: Dispatch<SetStateAction<News[]>>
  categories: Cat[];
  selectedCategorie?: string;
}

export interface NewsCardProps {
  setNewsList: Dispatch<SetStateAction<News[]>>
  news: News;
  categories: Cat[];
  selectedCategorie?: string;
}

export interface EditNewsButtonProps {
  setNewsList: Dispatch<SetStateAction<News[]>>
  news: News;
  categories: Cat[];
  selectedCategorie?: string;
}

export interface DeleteNewsButtonProps {
  newsId: number;
  setNewsList: Dispatch<SetStateAction<News[]>>
}



export interface CustomDialogProps {
  dialog: UseDialogReturn;
  onConfirm: () => void;
  onCancel?: () => void;
  title: string;
  children: ReactNode;
  confirmLabel?: string;
  cancelLabel?: string;
  danger?: boolean;
}

export interface Cat {
  id: number;
  name: string;
}
