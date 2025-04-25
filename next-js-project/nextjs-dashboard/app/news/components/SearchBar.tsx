// components/SearchBar.tsx
import { Input } from "@chakra-ui/react";
import { ChangeEvent } from "react";

interface SearchBarProps {
    value: string;
    onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

export default function SearchBar({ value, onChange }: SearchBarProps) {
    return (
        <Input
            placeholder="🔎 Rechercher une actualité"
            value={value}
            onChange={onChange}
            mb={4}
            maxW="400px"
        />
    );
}