import React, { useState, useEffect } from 'react';
import { History, X, Trash2, Clock, HardDrive, Film } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { historyStorage } from '../utils/historyStorage';
import AnimatedList from './AnimatedList';
import HistoryItem from './HistoryItem';

const DownloadHistory = ({ onSelectHistory }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [history, setHistory] = useState([]);
    const [stats, setStats] = useState({ count: 0, totalEpisodes: 0, totalSize: '0 B' });

    useEffect(() => {
        if (isOpen) {
            loadHistory();
        }
    }, [isOpen]);

    const loadHistory = () => {
        const data = historyStorage.getHistory();
        setHistory(data);
        setStats(historyStorage.getStats());
    };

    const handleRemove = (id) => {
        historyStorage.remove(id);
        loadHistory();
    };

    const handleClear = () => {
        if (window.confirm('Are you sure you want to clear all history?')) {
            historyStorage.clear();
            loadHistory();
        }
    };

    const handleSelect = (item) => {
        onSelectHistory(item.url);
        setIsOpen(false);
    };

    return (
        <>
            <motion.button
                onClick={() => setIsOpen(true)}
                className="relative p-2.5 rounded-xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-400 transition-all shadow-lg hover:shadow-xl group"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                title="Download History"
            >
                <History size={20} className="text-gray-700 dark:text-gray-300 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" />
                {history.length > 0 && (
                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-blue-600 text-white text-xs font-bold rounded-full flex items-center justify-center border-2 border-white dark:border-gray-900">
                        {history.length}
                    </span>
                )}
            </motion.button>

            <AnimatePresence>
                {isOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsOpen(false)}
                            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
                        />

                        {/* Popup */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            className="fixed top-20 right-4 md:right-20 w-96 bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 z-50 overflow-hidden flex flex-col max-h-[80vh]"
                        >
                            {/* Header */}
                            <div className="p-4 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50 backdrop-blur-md">
                                <h3 className="font-bold text-lg text-gray-900 dark:text-white flex items-center gap-2">
                                    <History className="text-blue-600" size={20} />
                                    History
                                </h3>
                                <div className="flex items-center gap-2">
                                    {history.length > 0 && (
                                        <button
                                            onClick={handleClear}
                                            className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                                            title="Clear All"
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    )}
                                    <button
                                        onClick={() => setIsOpen(false)}
                                        className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
                                    >
                                        <X size={20} />
                                    </button>
                                </div>
                            </div>

                            {/* Stats */}
                            <div className="grid grid-cols-3 gap-px bg-gray-100 dark:bg-gray-800 border-b border-gray-100 dark:border-gray-800">
                                <div className="bg-white dark:bg-gray-900 p-3 text-center">
                                    <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Series</div>
                                    <div className="font-bold text-gray-900 dark:text-white">{stats.count}</div>
                                </div>
                                <div className="bg-white dark:bg-gray-900 p-3 text-center">
                                    <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Episodes</div>
                                    <div className="font-bold text-gray-900 dark:text-white">{stats.totalEpisodes}</div>
                                </div>
                                <div className="bg-white dark:bg-gray-900 p-3 text-center">
                                    <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Size</div>
                                    <div className="font-bold text-gray-900 dark:text-white">{stats.totalSize}</div>
                                </div>
                            </div>

                            {/* List */}
                            <div className="overflow-y-auto custom-scrollbar flex-1 bg-gray-50 dark:bg-gray-900/50">
                                {history.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-48 text-gray-400 dark:text-gray-500">
                                        <History size={48} className="mb-3 opacity-20" />
                                        <p>No downloads yet</p>
                                    </div>
                                ) : (
                                    <AnimatedList
                                        items={history}
                                        renderItem={(item) => (
                                            <HistoryItem
                                                item={item}
                                                onSelect={handleSelect}
                                                onRemove={handleRemove}
                                            />
                                        )}
                                    />
                                )}
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
};

export default DownloadHistory;
