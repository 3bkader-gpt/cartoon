import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Type, Moon, Globe, Info } from 'lucide-react';
import axios from 'axios';

const Settings = () => {
    const [plexNaming, setPlexNaming] = useState(false);
    const [backendStatus, setBackendStatus] = useState('Checking...');

    useEffect(() => {
        // Load settings
        const savedPlex = localStorage.getItem('plex_naming') === 'true';
        setPlexNaming(savedPlex);

        // Check backend
        checkBackend();
    }, []);

    const checkBackend = async () => {
        try {
            await axios.get('http://127.0.0.1:8000/api/health');
            setBackendStatus('Online 🟢');
        } catch {
            // Try root if health not available
            try {
                await axios.get('http://127.0.0.1:8000/');
                setBackendStatus('Online 🟢');
            } catch {
                setBackendStatus('Offline 🔴');
            }
        }
    };

    const handleTogglePlex = () => {
        const newValue = !plexNaming;
        setPlexNaming(newValue);
        localStorage.setItem('plex_naming', newValue);
    };

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <SettingsIcon className="text-gray-500" />
                Settings
            </h2>

            {/* Application Settings */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
                <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
                    <h3 className="font-bold text-gray-900 dark:text-white">Application</h3>
                </div>

                <div className="divide-y divide-gray-100 dark:divide-gray-700">
                    {/* Plex Naming Toggle */}
                    <div className="p-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 dark:text-purple-400">
                                <Type size={20} />
                            </div>
                            <div>
                                <h4 className="font-medium text-gray-900 dark:text-white">Plex/Kodi Friendly Naming</h4>
                                <p className="text-sm text-gray-500 dark:text-gray-400">
                                    Rename files to "Series - S01E01 - Title.mp4"
                                </p>
                            </div>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                            <input
                                type="checkbox"
                                className="sr-only peer"
                                checked={plexNaming}
                                onChange={handleTogglePlex}
                            />
                            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                        </label>
                    </div>
                </div>
            </div>

            {/* System Status */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
                <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
                    <h3 className="font-bold text-gray-900 dark:text-white">System Status</h3>
                </div>

                <div className="p-4 space-y-4">
                    <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-100 dark:border-gray-700">
                        <span className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                            <Globe size={18} />
                            Backend API
                        </span>
                        <span className="font-mono font-bold">{backendStatus}</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-100 dark:border-gray-700">
                        <span className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                            <Info size={18} />
                            Version
                        </span>
                        <span className="font-mono font-bold text-gray-900 dark:text-white">v3.1.0</span>
                    </div>
                </div>
            </div>

            <div className="text-center text-sm text-gray-400 dark:text-gray-500">
                Configuration is saved automatically to your browser.
            </div>
        </div>
    );
};

export default Settings;
