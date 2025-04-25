'use client';

import { useState } from 'react';
import { LoginFormProps } from '../types'; // adapte ce chemin selon ta structure
import {
    Box,
    Button,
    Input,
    VStack,
    Alert,
    Field,
} from '@chakra-ui/react';

const LoginForm: React.FC<LoginFormProps> = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const response = await fetch('http://localhost:8000/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString(),
            });

            const data = await response.json();

            if (response.ok) {
                setError('');
                onLogin(data.access_token);
            } else {
                setError(data.detail || 'Erreur d’identification');
            }
        } catch {
            setError('Erreur de connexion au serveur');
        }
    };

    return (
        <Box w="100%" maxW="400px" mt={6}>
            <form onSubmit={handleSubmit}>
                <VStack align="stretch">
                    <Field.Root id="email" required>
                        <Field.Label>Email</Field.Label>
                        <Input
                            type="email"
                            placeholder="test@user.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </Field.Root>

                    <Field.Root id="password" required>
                        <Field.Label>Mot de passe</Field.Label>
                        <Input
                            type="password"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </Field.Root>

                    {error && (
                        <Alert.Root status="error" variant="subtle">
                            <Alert.Indicator />
                            <Alert.Content>
                                <Alert.Title>Erreur</Alert.Title>
                                <Alert.Description>{error}</Alert.Description>
                            </Alert.Content>
                        </Alert.Root>
                    )}

                    <Button colorScheme="blue" type="submit">
                        Se connecter
                    </Button>
                </VStack>
            </form>
        </Box>
    );
};

export default LoginForm;
