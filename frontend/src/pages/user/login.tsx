import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Copyright from '../../components/Copyright';
import { useAuth } from '../../hooks/auth';


export default function Login() {
    const [error, setError] = React.useState<string>('');
    const auth = useAuth()

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
    
        const username = data.get("username");
        const password = data.get("password");

    
        if(username !== null && password !== null){
            try {
                const response = await auth.login(username.toString(), password.toString())
                if (response.status==200) {
                    location.href='/models'
                } else {
                    setError('Invalid username or password.');
                }
            } catch (error) {
                setError('An error occurred while logging in. Please try again later.');
            }
        }
    };
    
    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
            sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
            >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign In
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                    {error && <Typography color="error">{error}</Typography>}
                    <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="username"
                    label="Username"
                    name="username"
                    autoComplete="username"
                    autoFocus
                    />
                    <TextField
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    />
                    <FormControlLabel
                    control={<Checkbox value="remember" color="primary" />}
                    label="Remember me"
                    />
                    <button className='signin-button'>Sign In</button>
                    <Grid container>
                    <Grid item xs>
                        <Link href="#" variant="body2">
                        Forgot password?
                        </Link>
                    </Grid>
                    <Grid item>
                        <Link href="/register" variant="body2">
                        {"Don't have an account? Sign Up"}
                        </Link>
                    </Grid>
                    </Grid>
                </Box>
            </Box>
            <Copyright/>
        </Container>
    );
}
