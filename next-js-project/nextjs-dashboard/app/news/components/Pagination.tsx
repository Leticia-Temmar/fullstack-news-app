import { ArrowBackIcon, ArrowForwardIcon } from "@chakra-ui/icons";
import { HStack, Button, Text, IconButton } from "@chakra-ui/react";

interface PaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    hasMore: boolean;
}


const Pagination = ({ currentPage, totalPages, onPageChange, hasMore }: PaginationProps) => {
    return (
        <HStack spacing={4} justify="center" mt={6}>
            <IconButton
                colorPalette="teal"
                variant="outline"
                onClick={() => onPageChange(currentPage - 1)}
                disabled={currentPage === 1}
            >
                <ArrowBackIcon />
            </IconButton>

            <Text fontWeight="medium">
                    {currentPage} / {totalPages}
            </Text>

            <IconButton
                colorPalette="teal"
                variant="outline"
                onClick={() => onPageChange(currentPage + 1)}
                disabled={!hasMore}
            >
                <ArrowForwardIcon />
            </IconButton>
        </HStack>
    );
};

export default Pagination;