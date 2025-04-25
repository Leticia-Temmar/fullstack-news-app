import { Dispatch, SetStateAction } from 'react';

export interface LoginFormProps {
    onLogin: (token: string) => void;
}