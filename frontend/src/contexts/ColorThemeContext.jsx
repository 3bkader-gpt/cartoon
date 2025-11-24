import React, { createContext, useContext, useState, useEffect } from 'react';

const ColorThemeContext = createContext();

export const useColorTheme = () => {
    const context = useContext(ColorThemeContext);
    if (!context) {
        throw new Error('useColorTheme must be used within ColorThemeProvider');
    }
    return context;
};

// Theme definitions
export const themes = {
    blue: {
        name: 'Blue Ocean',
        primary: '#3b82f6',
        primaryHover: '#2563eb',
        primaryLight: '#dbeafe',
        primaryDark: '#1e40af',
        gradient: 'from-blue-500 via-blue-600 to-blue-700',
        shadow: 'shadow-blue-600/30',
        ring: 'ring-blue-500',
    },
    purple: {
        name: 'Purple Dream',
        primary: '#a855f7',
        primaryHover: '#9333ea',
        primaryLight: '#f3e8ff',
        primaryDark: '#7e22ce',
        gradient: 'from-purple-500 via-purple-600 to-purple-700',
        shadow: 'shadow-purple-600/30',
        ring: 'ring-purple-500',
    },
    green: {
        name: 'Emerald Forest',
        primary: '#10b981',
        primaryHover: '#059669',
        primaryLight: '#d1fae5',
        primaryDark: '#047857',
        gradient: 'from-green-500 via-green-600 to-green-700',
        shadow: 'shadow-green-600/30',
        ring: 'ring-green-500',
    },
    pink: {
        name: 'Rose Garden',
        primary: '#ec4899',
        primaryHover: '#db2777',
        primaryLight: '#fce7f3',
        primaryDark: '#be185d',
        gradient: 'from-pink-500 via-pink-600 to-pink-700',
        shadow: 'shadow-pink-600/30',
        ring: 'ring-pink-500',
    },
    orange: {
        name: 'Sunset Glow',
        primary: '#f97316',
        primaryHover: '#ea580c',
        primaryLight: '#ffedd5',
        primaryDark: '#c2410c',
        gradient: 'from-orange-500 via-orange-600 to-orange-700',
        shadow: 'shadow-orange-600/30',
        ring: 'ring-orange-500',
    },
    indigo: {
        name: 'Midnight Sky',
        primary: '#6366f1',
        primaryHover: '#4f46e5',
        primaryLight: '#e0e7ff',
        primaryDark: '#4338ca',
        gradient: 'from-indigo-500 via-indigo-600 to-indigo-700',
        shadow: 'shadow-indigo-600/30',
        ring: 'ring-indigo-500',
    },
    teal: {
        name: 'Ocean Breeze',
        primary: '#14b8a6',
        primaryHover: '#0d9488',
        primaryLight: '#ccfbf1',
        primaryDark: '#0f766e',
        gradient: 'from-teal-500 via-teal-600 to-teal-700',
        shadow: 'shadow-teal-600/30',
        ring: 'ring-teal-500',
    },
    red: {
        name: 'Crimson Fire',
        primary: '#ef4444',
        primaryHover: '#dc2626',
        primaryLight: '#fee2e2',
        primaryDark: '#b91c1c',
        gradient: 'from-red-500 via-red-600 to-red-700',
        shadow: 'shadow-red-600/30',
        ring: 'ring-red-500',
    },
};

export const ColorThemeProvider = ({ children }) => {
    const [currentTheme, setCurrentTheme] = useState('blue');
    const [isChanging, setIsChanging] = useState(false);

    // Load theme from localStorage on mount
    useEffect(() => {
        const savedTheme = localStorage.getItem('colorTheme');
        if (savedTheme && themes[savedTheme]) {
            setCurrentTheme(savedTheme);
        }
    }, []);

    // Apply theme to CSS variables
    useEffect(() => {
        const theme = themes[currentTheme];
        if (theme) {
            const root = document.documentElement;
            root.style.setProperty('--theme-primary', theme.primary);
            root.style.setProperty('--theme-primary-hover', theme.primaryHover);
            root.style.setProperty('--theme-primary-light', theme.primaryLight);
            root.style.setProperty('--theme-primary-dark', theme.primaryDark);
        }
    }, [currentTheme]);

    const changeTheme = (themeName) => {
        if (themes[themeName]) {
            setIsChanging(true);

            // Smooth transition
            setTimeout(() => {
                setCurrentTheme(themeName);
                localStorage.setItem('colorTheme', themeName);

                setTimeout(() => {
                    setIsChanging(false);
                }, 300);
            }, 150);
        }
    };

    const value = {
        currentTheme,
        theme: themes[currentTheme],
        themes,
        changeTheme,
        isChanging,
    };

    return (
        <ColorThemeContext.Provider value={value}>
            {children}
        </ColorThemeContext.Provider>
    );
};
