import React, { useEffect, useState } from 'react';
import {
    Avatar, Alert, Button, CssBaseline, TextField,
    Link, Grid, Box, Typography, Container,
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from '../utils/enums';

export default function RegisterPage() {

    const navigate = useNavigate();
    const [error, setError] = useState(null)

    useEffect(() => {
        if (error) {
            const timeout = setTimeout(() => setError(null), 4000)
            return () => clearTimeout(timeout)
        }
    }, [error])

    const registerUser = async (full_name, email, username, password, password2) => {
        const response = await fetch(`${BASE_URL}/register/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ full_name, email, username, password, password2 })
        });

        if (response.ok) {
            navigate("/login")
        } else {
            setError(await response.json())
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        registerUser(
            data.get('full_name'),
            data.get('email'),
            data.get('username'),
            data.get('password'),
            data.get('password2'),
        )
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
                    Sign up
                </Typography>
                {error && Object.entries(error).map(([key, value]) => (
                    <Alert key={key} severity="error">{key}: {value}</Alert>
                ))}
                <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                                autoComplete="given-name"
                                name="full_name"
                                required
                                fullWidth
                                id="full_name"
                                label="Full Name"
                                autoFocus
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                autoComplete="username"
                                name="username"
                                required
                                fullWidth
                                id="username"
                                label="Username"
                                autoFocus
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                autoComplete="email"
                                name="email"
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="new-password"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                name="password2"
                                label="Confirm Password"
                                type="password"
                                id="password2"
                                autoComplete="new-password2"
                            />
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Sign Up
                    </Button>
                    <Grid container justifyContent="flex-end">
                        <Grid item>
                            <Link href="/login" variant="body2">
                                Already have an account?
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
    );
}

