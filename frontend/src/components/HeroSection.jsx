import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Play, Loader2, Download, Film, Tv } from 'lucide-react';
import { searchCartoons } from '../api';

const HeroSection = ({ onResolve, onSeasonMode, onSelectResult }) => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!url) return;

        // Check if it's a URL
        if (url.startsWith('http')) {
            setLoading(true);
            setError('');
            try {
                await onResolve(url);
            } catch (err) {
                setError('Could not resolve URL. Please check the link and try again.');
            } finally {
                setLoading(false);
            }
        } else {
            // It's a search query
            setLoading(true);
            setError('');
            setSearchResults([]);
            setIsSearching(true);
            try {
                const results = await searchCartoons(url);
                setSearchResults(results);
                if (results.length === 0) {
                    setError('No results found.');
                }
            } catch (err) {
                setError('Search failed. Please try again.');
            } finally {
                setLoading(false);
            }
        }
    };

    const handleResultClick = (result) => {
        if (onSelectResult) {
            onSelectResult(result);
        }
    };

    return (
        <div className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden py-20">
            {/* Background Blobs */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
                <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
                <div className="absolute top-[-10%] right-[-10%] w-96 h-96 bg-yellow-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
                <div className="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center z-10 px-4 w-full max-w-6xl"
            >
                <h1 className="text-6xl md:text-8xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600 mb-6">
                    Arabic Toons
                </h1>
                <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto">
                    Watch your favorite cartoons in high quality. Paste a link or search for a show.
                </p>

                <motion.form
                    onSubmit={handleSubmit}
                    className="relative max-w-3xl mx-auto w-full mb-12"
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 0.3, duration: 0.5 }}
                >
                    <div className="relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
                        <div className="relative flex items-center bg-darker rounded-xl p-2 border border-gray-700 bg-gray-900">
                            <Search className="w-6 h-6 text-gray-400 ml-3" />
                            <input
                                type="text"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="Paste URL or search (e.g., Conan, Gumball)..."
                                className="w-full bg-transparent text-white px-4 py-3 focus:outline-none text-lg placeholder-gray-500"
                            />
                            <button
                                type="submit"
                                disabled={loading}
                                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                {loading ? <Loader2 className="animate-spin" /> : <Search size={20} />}
                                <span>{url.startsWith('http') ? 'Watch' : 'Search'}</span>
                            </button>
                        </div>
                    </div>
                    {error && (
                        <motion.p
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-red-400 mt-4"
                        >
                            {error}
                        </motion.p>
                    )}
                </motion.form>

                {/* Search Results */}
                <AnimatePresence>
                    {searchResults.length > 0 && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 text-left"
                        >
                            {searchResults.map((result, index) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: index * 0.05 }}
                                    onClick={() => handleResultClick(result)}
                                    className="bg-gray-900/80 border border-gray-800 rounded-xl overflow-hidden cursor-pointer hover:border-purple-500 hover:shadow-purple-500/20 hover:shadow-xl transition-all group"
                                >
                                    <div className="aspect-[2/3] relative overflow-hidden bg-gray-800">
                                        {result.image ? (
                                            <img
                                                src={result.image}
                                                alt={result.title}
                                                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                            />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
                                                <Film size={48} className="text-gray-700" />
                                            </div>
                                        )}
                                        <div className="absolute top-2 right-2 bg-black/70 backdrop-blur-sm px-2 py-1 rounded text-xs font-medium text-white border border-white/10">
                                            {result.type === 'series' ? 'Series' : 'Episode'}
                                        </div>
                                    </div>
                                    <div className="p-4">
                                        <h3 className="text-white font-medium line-clamp-2 group-hover:text-purple-400 transition-colors">
                                            {result.title}
                                        </h3>
                                    </div>
                                </motion.div>
                            ))}
                        </motion.div>
                    )}
                </AnimatePresence>

                {!isSearching && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.5 }}
                        className="text-center mt-12"
                    >
                        <p className="text-gray-400 mb-4">Or download an entire season directly:</p>
                        <button
                            onClick={onSeasonMode}
                            className="inline-flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 border border-gray-700 hover:border-gray-600"
                        >
                            <Download size={20} />
                            <span>Season Downloader</span>
                        </button>
                    </motion.div>
                )}
            </motion.div>
        </div>
    );
};

export default HeroSection;
