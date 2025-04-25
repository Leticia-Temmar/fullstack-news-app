'use client';

import { useEffect, useState } from 'react';
import { Box, Heading, VStack } from '@chakra-ui/react';
import LoginForm from './components/LoginForm';

const Home = () => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // On force la déconnexion à chaque arrivée sur /
    localStorage.removeItem('token');
    setToken(null);
    setIsLoading(false);
  }, []);

  const handleLoginSuccess = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    window.location.href = '/news'; // Redirection après login
  };

  return (
    <Box p={8}>
      <VStack>
        <Heading>Le Monde</Heading>

        {!isLoading && <LoginForm onLogin={handleLoginSuccess} />}
      </VStack>
    </Box>
  );
};

export default Home;
