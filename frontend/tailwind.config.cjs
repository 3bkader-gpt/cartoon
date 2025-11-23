/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                darker: '#0a0a0f',
                primary: {
                    light: '#60a5fa',
                    DEFAULT: '#3b82f6',
                    dark: '#2563eb',
                },
                accent: {
                    light: '#a78bfa',
                    DEFAULT: '#8b5cf6',
                    dark: '#7c3aed',
                }
            },
            animation: {
                'gradient': 'gradient 8s linear infinite',
            },
            keyframes: {
                gradient: {
                    '0%, 100%': {
                        'background-size': '200% 200%',
                        'background-position': 'left center'
                    },
                    '50%': {
                        'background-size': '200% 200%',
                        'background-position': 'right center'
                    },
                },
            },
        },
    },
    plugins: [],
}
