// hooks/auth.ts
import { useState} from 'react';
import service from '../services/service';

export function useAuth() {
    const [loggedIn, setLoggedIn] = useState<boolean>(() => {
        const isLoggedIn = localStorage.getItem('access_token');
        return isLoggedIn ? isLoggedIn!=undefined : false;
    });

    const login = async (username: string, password: string) => {
        try {
            const response = await service.login(username, password);
            localStorage.setItem('access_token', response.access_token);
            setLoggedIn(true);

            return { status: response.status };
        } catch (error) {
            return { success: false, error: 'An error occurred during login.' };
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token')
        setLoggedIn(false);
    };

    const isLoggedIn = () => {
        return loggedIn;
    };

    return { login, logout, isLoggedIn };
}
