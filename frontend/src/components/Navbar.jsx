import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Library, Settings, Download } from 'lucide-react';
import ThemeToggle from './ThemeToggle';

const Navbar = ({ isDark, onToggleTheme }) => {
    return (
        <nav className="bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700 sticky top-0 z-50 shadow-sm backdrop-blur-md bg-opacity-90 dark:bg-opacity-90">
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <NavLink to="/" className="flex items-center gap-3 group">
                        <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-600/20 group-hover:scale-105 transition-transform">
                            <Download className="w-5 h-5 text-white" />
                        </div>
                        <h1 className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">
                            Arabic Toons <span className="text-blue-600">Downloader</span>
                        </h1>
                    </NavLink>

                    {/* Navigation Links */}
                    <div className="flex items-center gap-1 md:gap-2">
                        <NavLink
                            to="/"
                            className={({ isActive }) =>
                                `flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${isActive
                                    ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium'
                                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 hover:text-gray-900 dark:hover:text-white'
                                }`
                            }
                        >
                            <Home size={18} />
                            <span className="hidden md:inline">Home</span>
                        </NavLink>

                        <NavLink
                            to="/library"
                            className={({ isActive }) =>
                                `flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${isActive
                                    ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium'
                                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 hover:text-gray-900 dark:hover:text-white'
                                }`
                            }
                        >
                            <Library size={18} />
                            <span className="hidden md:inline">Library</span>
                        </NavLink>

                        <NavLink
                            to="/settings"
                            className={({ isActive }) =>
                                `flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${isActive
                                    ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium'
                                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 hover:text-gray-900 dark:hover:text-white'
                                }`
                            }
                        >
                            <Settings size={18} />
                            <span className="hidden md:inline">Settings</span>
                        </NavLink>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-3">
                        <ThemeToggle isDark={isDark} onToggle={onToggleTheme} />
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
