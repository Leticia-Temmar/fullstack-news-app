// components/CategoryFilter.tsx
import { HStack, Button } from "@chakra-ui/react";
import { Dispatch, SetStateAction } from "react";
import { Cat } from "../types";

type Props = {
  selected: Cat | null;
  onSelect: Dispatch<SetStateAction<Cat | null>>;
  categories: Cat[];
};

export default function CategoryFilter({ selected, onSelect, categories }: Props) {
  return (
    <HStack mb={4} flexWrap="wrap" gap={2}>
      <Button
        minW="120px"
        colorPalette={selected === null ? "teal" : "gray"}
        onClick={() => onSelect(null)}
      >
        Tous
      </Button>
      {categories.map((cat) => (
        <Button
          key={cat.id}
          minW="120px"
          colorPalette={selected?.id === cat.id ? "teal" : "gray"}
          onClick={() => onSelect(cat)}
        >
          {cat.name}
        </Button>
      ))}
    </HStack>
  );
}
