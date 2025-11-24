import React, { useState, useEffect } from 'react';
import { historyStorage } from '../utils/historyStorage';

const DownloadHistory = ({ onSelectHistory }) => {
    const [history, setHistory] = useState([]);
    const [stats, setStats] = useState(null);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = () => {
        const items = historyStorage.getHistory();
        const statistics = historyStorage.getStats();
        setHistory(items);
        setStats(statistics);
    };

    const handleRemove = (id) => {
        historyStorage.removeHistory(id);
        loadHistory();
    };

    const handleClear = () => {
        if (window.confirm('Are you sure you want to clear all history?')) {
            historyStorage.clearHistory();
            loadHistory();
        }
    };

    const handleSelect = (item) => {
        if (onSelectHistory) {
            onSelectHistory(item.url);
        }
        setIsOpen(false);
    };

    const formatSize = (bytes) => {
        if (bytes >= 1024 * 1024 * 1024) {
            return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
        } else if (bytes >= 1024 * 1024) {
            return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
        } else {
            return `${(bytes / 1024).toFixed(2)} KB`;
        }
    };

    if (history.length === 0) {
        return null;
    }

    return (
        <div className="relative">
            {/* History Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="relative p-2.5 rounded-xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 transition-all shadow-lg hover:shadow-xl"
                title="Download History"
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {history.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                        {history.length}
                    </span>
                )}
            </button>

            {/* History Popup */}
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <div
                        className="fixed inset-0 z-40"
                        onClick={() => setIsOpen(false)}
                    ></div>

                    {/* Popup */}
                    <div className="absolute right-0 mt-2 w-96 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border-2 border-gray-200 dark:border-gray-700 z-50 overflow-hidden animate-scale-in max-h-[600px] flex flex-col">
                        {/* Header */}
                        <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                            <div className="flex justify-between items-center mb-2">
                                <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    Download History
                                </h3>
                                <button
                                    onClick={handleClear}
                                    className="text-xs text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 font-medium"
                                >
                                    Clear All
                                </button>
                            </div>

                            {/* Stats */}
                            {stats && (
                                <div className="grid grid-cols-3 gap-2 mt-3">
                                    <div className="bg-white dark:bg-gray-800 rounded-lg p-2 text-center">
                                        <div className="text-xs text-gray-500 dark:text-gray-400">Series</div>
                                        <div className="text-lg font-bold text-blue-600 dark:text-blue-400">{stats.totalDownloads}</div>
                                    </div>
                                    <div className="bg-white dark:bg-gray-800 rounded-lg p-2 text-center">
                                        <div className="text-xs text-gray-500 dark:text-gray-400">Episodes</div>
                                        <div className="text-lg font-bold text-green-600 dark:text-green-400">{stats.totalEpisodes}</div>
                                    </div>
                                    <div className="bg-white dark:bg-gray-800 rounded-lg p-2 text-center">
                                        <div className="text-xs text-gray-500 dark:text-gray-400">Size</div>
                                        <div className="text-lg font-bold text-purple-600 dark:text-purple-400">{formatSize(stats.totalSize)}</div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* History List */}
                        <div className="overflow-y-auto flex-1 custom-scrollbar">
                            {history.map((item) => (
                                <div
                                    key={item.id}
                                    className="p-4 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer group"
                                    onClick={() => handleSelect(item)}
                                >
                                    <div className="flex gap-3">
                                        {/* Poster */}
                                        <div className="shrink-0">
                                            {item.poster ? (
                                                <img
                                                    src={item.poster}
                                                    alt={item.seriesName}
                                                    className="w-16 h-24 rounded-lg object-cover border border-gray-200 dark:border-gray-600"
                                                />
                                            ) : (
                                                <div className="w-16 h-24 rounded-lg bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center border border-gray-200 dark:border-gray-600">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                                                    </svg>
                                                </div>
                                            )}
                                        </div>

                                        {/* Info */}
                                        <div className="flex-1 min-w-0">
                                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                                                {item.seriesName}
                                            </h4>

                                            <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-gray-400">
                                                <span className="flex items-center gap-1">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                                                    </svg>
                                                    {item.selectedCount} episodes
                                                </span>
                                                <span>•</span>
                                                <span className="flex items-center gap-1">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                                                    </svg>
                                                    {item.totalSize}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-2 mt-2">
                                                <span className="text-xs text-gray-400 dark:text-gray-500">
                                                    {historyStorage.getTimeAgo(item.timestamp)}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Remove Button */}
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleRemove(item.id);
                                            }}
                                            className="shrink-0 p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all"
                                            title="Remove"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Footer */}
                        <div className="p-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                            <p className="text-xs text-center text-gray-500 dark:text-gray-400">
                                Click on any item to reload
                            </p>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default DownloadHistory;
