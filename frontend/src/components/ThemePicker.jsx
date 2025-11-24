import React, { useState } from 'react';
import { useColorTheme, themes } from '../contexts/ColorThemeContext';

const ThemePicker = () => {
    const { currentTheme, changeTheme } = useColorTheme();
    const [isOpen, setIsOpen] = useState(false);

    const themeColors = {
        blue: '#3b82f6',
        purple: '#a855f7',
        green: '#10b981',
        pink: '#ec4899',
        orange: '#f97316',
        indigo: '#6366f1',
        teal: '#14b8a6',
        red: '#ef4444',
    };

    return (
        <div className="relative">
            {/* Theme Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="p-2.5 rounded-xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 transition-all shadow-lg hover:shadow-xl"
                title="Change Theme"
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
            </button>

            {/* Theme Picker Popup */}
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <div
                        className="fixed inset-0 z-40"
                        onClick={() => setIsOpen(false)}
                    ></div>

                    {/* Popup */}
                    <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border-2 border-gray-200 dark:border-gray-700 z-50 overflow-hidden animate-scale-in">
                        {/* Header */}
                        <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                                </svg>
                                Choose Theme
                            </h3>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                Customize your experience
                            </p>
                        </div>

                        {/* Theme Grid */}
                        <div className="p-4 grid grid-cols-2 gap-3 max-h-96 overflow-y-auto custom-scrollbar">
                            {Object.entries(themes).map(([key, theme]) => (
                                <button
                                    key={key}
                                    onClick={() => {
                                        changeTheme(key);
                                        setIsOpen(false);
                                    }}
                                    className={`group relative p-4 rounded-xl border-2 transition-all ${currentTheme === key
                                            ? 'border-gray-900 dark:border-white bg-gray-50 dark:bg-gray-700 shadow-lg'
                                            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-md'
                                        }`}
                                >
                                    {/* Color Circle */}
                                    <div className="flex items-center gap-3 mb-2">
                                        <div
                                            className="w-10 h-10 rounded-full shadow-lg ring-2 ring-white dark:ring-gray-800 group-hover:scale-110 transition-transform"
                                            style={{ backgroundColor: themeColors[key] }}
                                        ></div>

                                        {/* Checkmark */}
                                        {currentTheme === key && (
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-600 dark:text-green-400" viewBox="0 0 20 20" fill="currentColor">
                                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                            </svg>
                                        )}
                                    </div>

                                    {/* Theme Name */}
                                    <div className="text-left">
                                        <p className="font-semibold text-sm text-gray-900 dark:text-white">
                                            {theme.name}
                                        </p>
                                        <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                                            {key}
                                        </p>
                                    </div>

                                    {/* Preview Gradient */}
                                    <div
                                        className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${theme.gradient} opacity-0 group-hover:opacity-100 transition-opacity`}
                                    ></div>
                                </button>
                            ))}
                        </div>

                        {/* Footer */}
                        <div className="p-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                            <p className="text-xs text-center text-gray-500 dark:text-gray-400">
                                Theme saved automatically
                            </p>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default ThemePicker;
