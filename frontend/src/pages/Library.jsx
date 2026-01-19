import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Heart, Play, Trash2, Film, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = 'http://127.0.0.1:8000';

const Library = () => {
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchFavorites();
    }, []);

    const fetchFavorites = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`${API_BASE_URL}/api/library/`);
            setFavorites(response.data);
            setError(null);
        } catch (err) {
            console.error('Error fetching library:', err);
            setError('Failed to load library');
        } finally {
            setLoading(false);
        }
    };

    const handleRemove = async (url, e) => {
        e.stopPropagation();
        if (!window.confirm('Remove from library?')) return;

        try {
            // Use toggle endpoint to remove favorite
            await axios.post(`${API_BASE_URL}/api/library/toggle`, { url });
            setFavorites(prev => prev.filter(item => item.url !== url));
        } catch (err) {
            alert('Failed to remove favorite');
        }
    };

    const handleCardClick = (url) => {
        window.location.href = `/?url=${encodeURIComponent(url)}`;
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[50vh]">
                <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-20 bg-red-50 dark:bg-red-900/10 rounded-xl border border-red-100 dark:border-red-900/30">
                <p className="text-red-600 dark:text-red-400 font-medium">{error}</p>
                <button
                    onClick={fetchFavorites}
                    className="mt-4 px-4 py-2 bg-white dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:shadow-md transition-all text-sm font-bold border border-red-100 dark:border-red-800"
                >
                    Try Again
                </button>
            </div>
        );
    }

    if (favorites.length === 0) {
        return (
            <div className="text-center py-32 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700">
                <div className="w-16 h-16 mx-auto bg-gray-100 dark:bg-gray-700/50 rounded-full flex items-center justify-center mb-6">
                    <Heart className="w-8 h-8 text-gray-400 dark:text-gray-500" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Your library is empty</h3>
                <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
                    Start adding shows to your favorites by clicking the heart icon on any series page.
                </p>
                <a
                    href="/"
                    className="inline-block mt-8 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-600/20"
                >
                    Browse Shows
                </a>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                    <Heart className="text-pink-500 fill-pink-500" />
                    My Library
                    <span className="text-sm font-normal text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full ml-2">
                        {favorites.length}
                    </span>
                </h2>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                <AnimatePresence>
                    {favorites.map((show) => (
                        <motion.div
                            key={show.url}
                            layout
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            whileHover={{ y: -5 }}
                            className="bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow-lg border border-gray-100 dark:border-gray-700 group cursor-pointer"
                            onClick={() => handleCardClick(show.url)}
                        >
                            <div className="relative aspect-[2/3] overflow-hidden bg-gray-100 dark:bg-gray-700">
                                {show.thumbnail ? (
                                    <img
                                        src={show.thumbnail}
                                        alt={show.title}
                                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center">
                                        <Film className="w-12 h-12 text-gray-300 dark:text-gray-600" />
                                    </div>
                                )}

                                {/* Overlay */}
                                <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-3">
                                    <span className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-lg transform scale-0 group-hover:scale-100 transition-transform duration-300 delay-75">
                                        <Play className="ml-1 fill-white" size={24} />
                                    </span>
                                </div>

                                <button
                                    onClick={(e) => handleRemove(show.url, e)}
                                    className="absolute top-2 right-2 p-2 bg-black/50 hover:bg-red-500/80 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                                    title="Remove from library"
                                >
                                    <Trash2 size={16} />
                                </button>
                            </div>

                            <div className="p-4">
                                <h3 className="font-bold text-gray-900 dark:text-white truncate" title={show.title}>
                                    {show.title}
                                </h3>
                                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                    {show.total_episodes > 0 ? `${show.total_episodes} episodes` : 'Click to load'}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </div>
    );
};

export default Library;
