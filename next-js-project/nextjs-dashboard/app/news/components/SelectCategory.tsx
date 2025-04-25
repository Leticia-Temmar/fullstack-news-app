import { createListCollection, Select, Stack, } from "@chakra-ui/react";
import { Cat } from "../types";

interface Props {
    listCategory: Cat[];
    value: string;
    onChange: (value: string) => void;
}

const SelectCategory = ({ listCategory, value, onChange }: Props) => {
   

    const list = createListCollection({
        items: listCategory.map((cat) => ({
            label: cat.name,
            value: cat.id.toString(),
        })),
    });

    return (
        <Stack gap="5" width="100%">
            <Select.Root
                collection={list}
                value={[value]} // toujours un tableau
                onValueChange={(e) => onChange(e.value[0])} // première valeur sélectionnée
            >
                <Select.HiddenSelect />
                <Select.Control>
                    <Select.Trigger>
                        <Select.ValueText placeholder="Sélectionner une catégorie" />
                    </Select.Trigger>
                    <Select.IndicatorGroup>
                        <Select.Indicator />
                    </Select.IndicatorGroup>
                </Select.Control>

                <Select.Positioner>
                    <Select.Content>
                        {list.items.map((element) => (
                            <Select.Item item={element} key={element.value}>
                                {element.label}
                                <Select.ItemIndicator />
                            </Select.Item>
                        ))}
                    </Select.Content>
                </Select.Positioner>

            </Select.Root>
        </Stack>
    );
};
export default SelectCategory;
