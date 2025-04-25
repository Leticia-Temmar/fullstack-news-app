import { Button, HStack } from '@chakra-ui/react';
import { useRouter } from 'next/navigation';

const NavigationBoutons = ({ onAccueilClick }: { onAccueilClick?: () => void }) => {
  const router = useRouter();

  return (
    <HStack >
      <Button colorPalette="blue" variant="surface" onClick={onAccueilClick}>
        Accueil
      </Button>
      <Button colorPalette="green" variant="surface" onClick={() => router.push('/news')}>
        Actualités
      </Button>
    </HStack>
  );
};

export default NavigationBoutons;
