import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { useAuth } from '../hooks/auth';
import { useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';

import {
    Storage as StorageIcon,
    Person as PersonIcon,
    Logout as LogoutIcon,
    AccountCircle as AccountCircleIcon,
    ShowChart as ShowChartIcon,
    Settings as SettingsIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

interface SidebarItem {
    name: string;
    icon: React.ElementType;
    link: string;
}

export default function NavLayout() {
    const auth = useAuth();
    const location = useLocation();
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);

    const isBaseUrl = location.pathname === '/';

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const primarySidebarItems: SidebarItem[] = [
        { name: 'My Models', icon: StorageIcon, link: '/models' },
        //{ name: 'Datasets', icon: Dataset, link: '/datasets' },
    ];

    const secondarySidebarItems: SidebarItem[] = [
        { name: 'Profile', icon: PersonIcon, link: '/profile' },
        { name: 'Sign out', icon: LogoutIcon, link: '/' },
    ];

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }} color={'primary'}>
                <Toolbar>
                    <ShowChartIcon sx={{ mr: 3.5 }} />
                    <Typography variant="h6" noWrap component="div" sx={{cursor: 'pointer'}} aria-label='Cracker Menu' onClick={()=>{window.location.href='/'}}>
                        Grand Line
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <div>
                        <IconButton
                            size="large"
                            aria-label="account of current user"
                            aria-controls="menu-appbar"
                            aria-haspopup="true"
                            onClick={handleMenu}
                            color="inherit"
                        >
                            <AccountCircleIcon />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorEl}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'left',
                            }}
                            open={open}
                            onClose={handleClose}
                        >
                            {auth.isLoggedIn() ? (
                                <>
                                    <MenuItem onClick={handleClose} component={Link} to="/profile">
                                        <ListItemIcon>
                                            <PersonIcon fontSize="small" />
                                        </ListItemIcon>
                                        Profile
                                    </MenuItem>
                                    <MenuItem onClick={handleClose} component={Link} to="/profile/settings">
                                        <ListItemIcon>
                                            <SettingsIcon fontSize="small" />
                                        </ListItemIcon>
                                        Settings
                                    </MenuItem>
                                    <Divider />
                                    <MenuItem onClick={() => { auth.logout(); handleClose(); window.location.href = '/' }}>
                                        <ListItemIcon>
                                            <LogoutIcon fontSize="small" />
                                        </ListItemIcon>
                                        Sign out
                                    </MenuItem>
                                </>
                            ) : (
                                <MenuItem onClick={handleClose} component={Link} to="/login">
                                    <ListItemIcon>
                                        <PersonIcon fontSize="small" />
                                    </ListItemIcon>
                                    Login
                                </MenuItem>
                            )}
                        </Menu>
                    </div>
                </Toolbar>
            </AppBar>
            {!isBaseUrl &&
                <Drawer
                    variant="permanent"
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
                    }}
                >
                    <Toolbar />
                    <Box sx={{ overflow: 'auto', ml: 1, mt: 2 }}>
                        <List>
                            {primarySidebarItems.map((item, index) => (
                                <ListItem key={index} disablePadding>
                                    <ListItemButton component={Link} to={item.link}>
                                        <ListItemIcon>
                                            <item.icon />
                                        </ListItemIcon>
                                        <ListItemText primary={item.name} />
                                    </ListItemButton>
                                </ListItem>
                            ))}
                        </List>
                        <Divider />
                        <List>
                            {secondarySidebarItems.map((item, index) => (
                                <ListItem key={index} disablePadding>
                                    <ListItemButton component={Link} to={item.link} onClick={() => { item.name == 'Sign out' ? auth.logout() : undefined }}>
                                        <ListItemIcon>
                                            <item.icon />
                                        </ListItemIcon>
                                        <ListItemText primary={item.name} />
                                    </ListItemButton>
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                </Drawer>
            }
        </Box>
    );
}
