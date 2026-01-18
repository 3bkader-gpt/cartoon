import React, { useState, useEffect, useMemo, forwardRef, useImperativeHandle } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { streamSeason } from '../api';
import { historyStorage } from '../utils/historyStorage';
import { fadeIn, slideUp, staggerContainer, cardAnimation } from '../utils/animations';
import cacheManager from '../utils/cache';
import axios from 'axios';

const SeasonDownloader = forwardRef((props, ref) => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [episodes, setEpisodes] = useState([]);
    const [progress, setProgress] = useState(null);
    const [seriesTitle, setSeriesTitle] = useState('');
    const [copied, setCopied] = useState(null);
    const [selectedEpisodes, setSelectedEpisodes] = useState(new Set());
    const [isCached, setIsCached] = useState(false);
    const [showToast, setShowToast] = useState(false);

    // Sorting & Filtering
    const [sortBy, setSortBy] = useState('episode');
    const [sortOrder, setSortOrder] = useState('asc');
    const [searchQuery, setSearchQuery] = useState('');

    // Favorites State
    const [isFavorited, setIsFavorited] = useState(false);
    const [favoriteId, setFavoriteId] = useState(null);

    // Check favorite status when series title changes
    useEffect(() => {
        if (!seriesTitle || seriesTitle === 'Unknown Series') return;
        checkFavoriteStatus();
    }, [seriesTitle]);

    const checkFavoriteStatus = async () => {
        if (!seriesTitle) return;
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/library/');
            const found = response.data.find(f => f.url === url);
            if (found) {
                setIsFavorited(true);
                setFavoriteId(found.id);
            } else {
                setIsFavorited(false);
                setFavoriteId(null);
            }
        } catch (err) {
            console.error('Error checking favorite:', err);
        }
    };

    const toggleFavorite = async () => {
        // Safety check: ensure we have metadata before trying to save
        if (!seriesTitle || !seasonMetadata) {
            console.warn("Cannot toggle favorite: Missing metadata");
            return;
        }

        try {
            if (isFavorited) {
                await axios.delete('http://127.0.0.1:8000/api/library/', { params: { url } });
                setIsFavorited(false);
                setFavoriteId(null);
            } else {
                const response = await axios.post('http://127.0.0.1:8000/api/library/', {
                    title: seriesTitle,
                    url: url,
                    thumbnail: seasonMetadata.poster
                });
                setIsFavorited(true);
                setFavoriteId(response.data.id);
            }
        } catch (err) {
            console.error('Error toggling favorite:', err);
            alert('Failed to update library');
        }
    };

    useEffect(() => {
        // Check for URL in query params (e.g., from Library)
        const params = new URLSearchParams(window.location.search);
        const queryUrl = params.get('url');

        // Check for URL in localStorage (legacy)
        const savedUrl = localStorage.getItem('temp_season_url');

        if (queryUrl) {
            setUrl(queryUrl);
            // Directly call handleFetch with the new URL
            // Pass the URL explicitly to avoid state timing issues
            handleFetch(false, queryUrl);
        } else if (savedUrl) {
            setUrl(savedUrl);
            localStorage.removeItem('temp_season_url');
        }
    }, []);

    // Auto-select all episodes when loaded
    useEffect(() => {
        if (episodes.length > 0) {
            setSelectedEpisodes(new Set(episodes.map((_, idx) => idx)));
        }
    }, [episodes.length]);

    // Filtered and sorted episodes
    const filteredAndSortedEpisodes = useMemo(() => {
        let result = [...episodes];

        if (searchQuery) {
            result = result.filter(ep =>
                ep.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                ep.video_info?.filename?.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        result.sort((a, b) => {
            let comparison = 0;

            if (sortBy === 'episode') {
                const aNum = parseInt(a.title?.match(/\d+/)?.[0] || '0');
                const bNum = parseInt(b.title?.match(/\d+/)?.[0] || '0');
                comparison = aNum - bNum;
            } else if (sortBy === 'name') {
                comparison = (a.title || '').localeCompare(b.title || '');
            } else if (sortBy === 'size') {
                const aSize = a.metadata?.size_bytes || 0;
                const bSize = b.metadata?.size_bytes || 0;
                comparison = aSize - bSize;
            }

            return sortOrder === 'asc' ? comparison : -comparison;
        });

        return result;
    }, [episodes, searchQuery, sortBy, sortOrder]);

    // Calculate season metadata
    const seasonMetadata = useMemo(() => {
        if (episodes.length === 0) return null;

        // Extract series name from first episode or use state from backend
        const firstTitle = episodes[0]?.title || '';
        const derivedSeriesName = firstTitle
            .replace(/\s*-?\s*(الحلقة|Episode|E|الموسم|Season|S)\s*\d+.*$/i, '')
            .replace(/\s*-?\s*\d+.*$/i, '')
            .trim();

        const seriesName = seriesTitle || derivedSeriesName || 'Unknown Series';

        // Calculate total size
        const totalSizeBytes = episodes.reduce((sum, ep) => sum + (ep.metadata?.size_bytes || 0), 0);
        const avgSizeBytes = episodes.length > 0 ? totalSizeBytes / episodes.length : 0;

        // Format size helper
        const formatSize = (bytes) => {
            if (bytes >= 1024 * 1024 * 1024) {
                return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
            } else if (bytes >= 1024 * 1024) {
                return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
            } else {
                return `${(bytes / 1024).toFixed(2)} KB`;
            }
        };

        // Get poster/thumbnail (use first episode's thumbnail or placeholder)
        const poster = episodes[0]?.thumbnail || null;

        return {
            seriesName,
            totalEpisodes: episodes.length,
            totalSize: formatSize(totalSizeBytes),
            totalSizeBytes,
            avgSize: formatSize(avgSizeBytes),
            avgSizeBytes,
            poster
        };
    }, [episodes]);

    // Expose methods to parent via ref
    useImperativeHandle(ref, () => ({
        loadFromHistory: (historyUrl) => {
            setUrl(historyUrl);
            // Trigger fetch automatically
            setTimeout(() => {
                const fetchButton = document.querySelector('button[type="submit"]');
                if (fetchButton) {
                    fetchButton.click();
                }
            }, 100);
        }
    }));

    const handleFetch = async (forceRefresh = false, overrideUrl = null) => {
        // Use override URL if provided, otherwise using existing state URL
        const urlToUse = overrideUrl || url;
        if (!urlToUse) return;

        setLoading(true);
        setError(null);
        setEpisodes([]);
        setProgress(null);
        setSelectedEpisodes(new Set());
        setIsCached(false);

        try {
            // Check cache first (unless force refresh)
            if (!forceRefresh) {
                const cachedData = await cacheManager.getFullSeason(urlToUse);
                if (cachedData && cachedData.episodes.length > 0) {
                    // Check if cached metadata has valid title
                    if (cachedData.metadata?.seriesName === "Unknown Series") {
                        console.log("Cached Series Title is 'Unknown', forcing refresh...");
                        // Do NOT return here, let it fall through to backend fetch
                    } else {
                        // Load from cache instantly
                        setEpisodes(cachedData.episodes);
                        setSeriesTitle(cachedData.metadata?.seriesName || '');
                        setIsCached(true);
                        setLoading(false);

                        // Show toast
                        setShowToast(true);
                        setTimeout(() => setShowToast(false), 3000);

                        return;
                    }
                }
            }

            // Fetch from backend
            const fetchedEpisodes = [];
            await streamSeason(urlToUse, (data) => {
                if (data.type === 'start') {
                    setProgress({ current: 0, total: data.total, title: 'Starting...' });
                    if (data.series_title) {
                        setSeriesTitle(data.series_title);
                    }
                } else if (data.type === 'progress') {
                    setProgress({
                        current: data.current,
                        total: data.total,
                        title: `Processing: ${data.title}`
                    });
                } else if (data.type === 'result') {
                    fetchedEpisodes.push(data.data);
                    setEpisodes(prev => [...prev, data.data]);
                } else if (data.type === 'error') {
                    console.error("Episode error:", data);
                }
            });

            // Save to cache after successful fetch
            if (fetchedEpisodes.length > 0) {
                // Calculate metadata for cache
                const firstTitle = fetchedEpisodes[0]?.title || '';
                const derivedSeriesName = firstTitle
                    .replace(/\s*-?\s*(الحلقة|Episode|E|الموسم|Season|S)\s*\d+.*$/i, '')
                    .replace(/\s*-?\s*\d+.*$/i, '')
                    .trim();
                const seriesName = seriesTitle || derivedSeriesName || 'Unknown Series';

                const totalSizeBytes = fetchedEpisodes.reduce((sum, ep) => sum + (ep.metadata?.size_bytes || 0), 0);
                const formatSize = (bytes) => {
                    if (bytes >= 1024 * 1024 * 1024) {
                        return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
                    } else if (bytes >= 1024 * 1024) {
                        return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
                    } else {
                        return `${(bytes / 1024).toFixed(2)} KB`;
                    }
                };

                const metadata = {
                    seriesName,
                    totalEpisodes: fetchedEpisodes.length,
                    totalSize: formatSize(totalSizeBytes),
                    totalSizeBytes,
                    poster: fetchedEpisodes[0]?.thumbnail || null
                };

                await cacheManager.saveSeason(url, metadata, fetchedEpisodes);
            }
        } catch (err) {
            setError(err.message || 'Failed to fetch episodes');
        } finally {
            setLoading(false);
            setProgress(null);
        }
    };

    const handleRefresh = async () => {
        if (!url) return;
        await cacheManager.deleteSeason(url);
        await handleFetch(true);
    };

    // Save to history when episodes are loaded
    useEffect(() => {
        if (episodes.length > 0 && seasonMetadata && url) {
            historyStorage.addHistory({
                seriesName: seasonMetadata.seriesName,
                url: url,
                episodeCount: seasonMetadata.totalEpisodes,
                totalSize: seasonMetadata.totalSize,
                totalSizeBytes: seasonMetadata.totalSizeBytes,
                selectedCount: selectedEpisodes.size,
                poster: seasonMetadata.poster,
            });
        }
    }, [episodes.length, seasonMetadata, url, selectedEpisodes.size]);

    const toggleSelection = (idx) => {
        setSelectedEpisodes(prev => {
            const newSet = new Set(prev);
            if (newSet.has(idx)) {
                newSet.delete(idx);
            } else {
                newSet.add(idx);
            }
            return newSet;
        });
    };

    const toggleSelectAll = () => {
        if (selectedEpisodes.size === filteredAndSortedEpisodes.length) {
            setSelectedEpisodes(new Set());
        } else {
            setSelectedEpisodes(new Set(filteredAndSortedEpisodes.map((_, idx) => idx)));
        }
    };

    const getSelectedEpisodes = () => {
        return filteredAndSortedEpisodes.filter((_, idx) => selectedEpisodes.has(idx));
    };

    const copyToClipboard = (text, id) => {
        navigator.clipboard.writeText(text);
        setCopied(id);
        setTimeout(() => setCopied(null), 2000);
    };

    const getFilename = (ep, index) => {
        const isPlexNaming = localStorage.getItem('plex_naming') === 'true';
        if (isPlexNaming && seasonMetadata?.seriesName) {
            // Pattern: Series Name - S01E01 - Title.mp4
            const epNum = (index + 1).toString().padStart(2, '0');
            // Assuming S01 for now as we don't strictly track season number per episode yet without parsing
            // But we can try to extract or default to S01
            const safeSeries = seasonMetadata.seriesName.replace(/[\\/:*?"<>|]/g, '');
            const safeTitle = ep.title.replace(/[\\/:*?"<>|]/g, '');
            return `${safeSeries} - S01E${epNum} - ${safeTitle}.mp4`;
        }
        return ep.filename || `episode_${index + 1}.mp4`;
    };

    const handleSaveList = () => {
        const episodesToExport = filteredAndSortedEpisodes.filter((_, idx) =>
            selectedEpisodes.size === 0 || selectedEpisodes.has(idx)
        );

        if (episodesToExport.length === 0) {
            alert('No episodes selected');
            return;
        }

        const content = episodesToExport
            .map((ep, index) => {
                const originalIndex = filteredAndSortedEpisodes.indexOf(ep); // Get original index for filename generation
                const filename = getFilename(ep, originalIndex);
                return `${ep.video_url} | ${filename}`;
            })
            .join('\n');

        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'episodes_list.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleExportIDM = () => {
        const episodesToExport = filteredAndSortedEpisodes.filter((_, idx) =>
            selectedEpisodes.size === 0 || selectedEpisodes.has(idx)
        );

        if (episodesToExport.length === 0) {
            alert('No episodes selected');
            return;
        }

        let ef2Content = '';
        episodesToExport.forEach((ep) => {
            if (ep.video_url) {
                const originalIndex = filteredAndSortedEpisodes.indexOf(ep); // Get original index for filename generation
                const filename = getFilename(ep, originalIndex);
                ef2Content += `<\r\n${ep.video_url}\r\nfilename=${filename}\r\n>\r\n`;
            }
        });

        const blob = new Blob([ef2Content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'exported_list.ef2';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl transition-colors duration-200">
            {/* Toast Notification */}
            <AnimatePresence>
                {showToast && (
                    <motion.div
                        initial={{ opacity: 0, y: -50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -50 }}
                        className="fixed top-4 right-4 z-50 bg-green-600 text-white px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        <span className="font-semibold">Loaded from cache ⚡</span>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="flex flex-col md:flex-row gap-4 mb-8">
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Paste Arabic Toons series or episode URL here..."
                    className="flex-1 p-4 rounded-xl border-2 border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all outline-none text-lg"
                    dir="ltr"
                />
                <button
                    onClick={handleFetch}
                    disabled={loading || !url}
                    className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-lg shadow-lg shadow-blue-600/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95"
                >
                    {loading ? (
                        <span className="flex items-center gap-2">
                            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Fetching...
                        </span>
                    ) : 'Fetch'}
                </button>
            </div>

            {progress && (
                <div className="mb-8 p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-100 dark:border-blue-800">
                    <div className="flex justify-between text-sm font-medium text-blue-800 dark:text-blue-300 mb-2">
                        <span>{progress.title}</span>
                        <span>{Math.round((progress.current / progress.total) * 100)}%</span>
                    </div>
                    <div className="w-full bg-blue-200 dark:bg-blue-800 rounded-full h-3 overflow-hidden">
                        <div
                            className="bg-blue-600 h-3 rounded-full transition-all duration-300 ease-out shadow-[0_0_10px_rgba(37,99,235,0.5)]"
                            style={{ width: `${(progress.current / progress.total) * 100}%` }}
                        />
                    </div>
                    <div className="mt-2 text-center text-xs text-blue-600 dark:text-blue-400 font-mono">
                        {progress.current} / {progress.total} Episodes Processed
                    </div>

                    {/* Loading Skeleton Cards */}
                    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {[...Array(8)].map((_, idx) => (
                            <div key={idx} className="bg-white dark:bg-gray-800 rounded-2xl border-2 border-gray-200 dark:border-gray-700 overflow-hidden shadow-lg">
                                {/* Skeleton Thumbnail */}
                                <div className="aspect-video w-full skeleton"></div>

                                {/* Skeleton Content */}
                                <div className="p-4 space-y-3">
                                    {/* Skeleton Title */}
                                    <div className="h-4 skeleton rounded w-3/4"></div>
                                    <div className="h-4 skeleton rounded w-1/2"></div>

                                    {/* Skeleton Metadata */}
                                    <div className="space-y-2">
                                        <div className="h-3 skeleton rounded w-full"></div>
                                        <div className="h-3 skeleton rounded w-2/3"></div>
                                    </div>

                                    {/* Skeleton Buttons */}
                                    <div className="flex gap-2 pt-2">
                                        <div className="flex-1 h-8 skeleton rounded-lg"></div>
                                        <div className="flex-1 h-8 skeleton rounded-lg"></div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {error && (
                <div className="mb-8 p-4 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-xl border border-red-100 dark:border-red-800 flex items-center gap-3">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {error}
                </div>
            )}

            {episodes.length > 0 && (
                <div className="space-y-6">
                    {/* Season Header */}
                    {seasonMetadata && (
                        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800 border border-gray-200 dark:border-gray-700 shadow-xl">
                            {/* Background Pattern */}
                            <div className="absolute inset-0 opacity-10">
                                <div className="absolute inset-0 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500"></div>
                            </div>

                            <div className="relative p-8">
                                <div className="flex flex-col md:flex-row gap-6 items-start">
                                    {/* Poster */}
                                    <div className="shrink-0">
                                        {seasonMetadata.poster ? (
                                            <img
                                                src={seasonMetadata.poster}
                                                alt={seasonMetadata.seriesName}
                                                className="w-32 h-48 md:w-40 md:h-60 rounded-xl object-cover shadow-2xl border-4 border-white dark:border-gray-700"
                                            />
                                        ) : (
                                            <div className="w-32 h-48 md:w-40 md:h-60 rounded-xl bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center shadow-2xl border-4 border-white dark:border-gray-700">
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-20 w-20 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                                                </svg>
                                            </div>
                                        )}
                                    </div>

                                    {/* Info */}
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center justify-between mb-4">
                                            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white truncate">
                                                {seasonMetadata.seriesName}
                                            </h2>
                                            {/* Favorite Button */}
                                            <button
                                                onClick={toggleFavorite}
                                                className={`p-3 rounded-full transition-all ${isFavorited
                                                    ? 'bg-pink-50 text-pink-500 hover:bg-pink-100'
                                                    : 'bg-gray-100 dark:bg-gray-700 text-gray-400 hover:text-pink-500 hover:bg-pink-50 dark:hover:bg-gray-600'
                                                    }`}
                                                title={isFavorited ? "Remove from Library" : "Add to Library"}
                                            >
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    className={`h-6 w-6 ${isFavorited ? 'fill-current' : 'fill-none'}`}
                                                    viewBox="0 0 24 24"
                                                    stroke="currentColor"
                                                    strokeWidth={2}
                                                >
                                                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                                </svg>
                                            </button>
                                        </div>

                                        {/* Stats Grid */}
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                                            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200 dark:border-gray-700">
                                                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Episodes</div>
                                                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                                                    {seasonMetadata.totalEpisodes}
                                                </div>
                                            </div>

                                            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200 dark:border-gray-700">
                                                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Total Size</div>
                                                <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                                                    {seasonMetadata.totalSize}
                                                </div>
                                            </div>

                                            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200 dark:border-gray-700">
                                                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Avg Size</div>
                                                <div className="text-2xl font-bold text-pink-600 dark:text-pink-400">
                                                    {seasonMetadata.avgSize}
                                                </div>
                                            </div>

                                            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200 dark:border-gray-700">
                                                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Selected</div>
                                                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                                                    {selectedEpisodes.size}
                                                </div>
                                            </div>
                                        </div>

                                        {/* Action Buttons */}
                                        <div className="flex flex-wrap gap-3">
                                            <button
                                                onClick={handleSaveList}
                                                disabled={selectedEpisodes.size === 0}
                                                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold shadow-lg shadow-blue-600/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2"
                                            >
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                                </svg>
                                                Save List
                                            </button>

                                            <button
                                                onClick={handleExportIDM}
                                                disabled={selectedEpisodes.size === 0}
                                                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl font-semibold shadow-lg shadow-green-600/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2"
                                            >
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                                                </svg>
                                                Export to IDM
                                            </button>

                                            <button
                                                onClick={toggleSelectAll}
                                                className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-semibold shadow-lg shadow-purple-600/30 transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2"
                                            >
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                                                </svg>
                                                {selectedEpisodes.size === filteredAndSortedEpisodes.length ? 'Deselect All' : 'Select All'}
                                            </button>

                                            {isCached && (
                                                <button
                                                    onClick={handleRefresh}
                                                    className="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-xl font-semibold shadow-lg shadow-orange-600/30 transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2"
                                                    title="Refresh from server"
                                                >
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                                    </svg>
                                                    Refresh
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="flex flex-col md:flex-row gap-3">
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Search episodes..."
                            className="flex-1 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                        <select
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value)}
                            className="px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                        >
                            <option value="episode">Sort by Episode</option>
                            <option value="name">Sort by Name</option>
                            <option value="size">Sort by Size</option>
                        </select>
                        <button
                            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                            className="px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 text-sm hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                        >
                            {sortOrder === 'asc' ? '↑ Asc' : '↓ Desc'}
                        </button>
                    </div>


                    {/* Episodes Grid */}
                    <motion.div
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 max-h-[800px] overflow-y-auto pr-2 custom-scrollbar"
                        variants={staggerContainer}
                        initial="hidden"
                        animate="visible"
                    >
                        <AnimatePresence mode='popLayout'>
                            {filteredAndSortedEpisodes.map((ep, idx) => (
                                <motion.div
                                    key={idx}
                                    variants={cardAnimation}
                                    initial="hidden"
                                    animate="visible"
                                    exit="hidden"
                                    whileHover="hover"
                                    whileTap="tap"
                                    className="group relative bg-white dark:bg-gray-800 rounded-2xl border-2 border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500 transition-colors duration-300 overflow-hidden shadow-lg hover:shadow-2xl"
                                >
                                    {/* Checkbox - Top Left Corner */}
                                    <div className="absolute top-3 left-3 z-10">
                                        <input
                                            type="checkbox"
                                            checked={selectedEpisodes.has(idx)}
                                            onChange={() => toggleSelection(idx)}
                                            className="w-6 h-6 rounded-lg border-2 border-white bg-white/90 backdrop-blur-sm text-blue-600 focus:ring-blue-500 cursor-pointer shadow-lg"
                                        />
                                    </div>

                                    {/* Episode Number Badge - Top Right Corner */}
                                    <div className="absolute top-3 right-3 z-10 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg">
                                        #{idx + 1}
                                    </div>

                                    {/* Thumbnail */}
                                    <div className="relative aspect-video w-full overflow-hidden bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30">
                                        {ep?.thumbnail ? (
                                            <motion.img
                                                src={ep.thumbnail}
                                                alt={ep.title || 'Episode'}
                                                className="w-full h-full object-cover"
                                                whileHover={{ scale: 1.1 }}
                                                transition={{ duration: 0.3 }}
                                                onError={(e) => e.target.style.display = 'none'}
                                            />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center">
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-blue-400 dark:text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                                </svg>
                                            </div>
                                        )}

                                        {/* Gradient Overlay */}
                                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                                    </div>

                                    {/* Card Content */}
                                    <div className="p-4 space-y-3">
                                        {/* Title */}
                                        <h4 className="font-bold text-gray-900 dark:text-white text-sm line-clamp-2 min-h-[2.5rem]" title={ep?.title}>
                                            {ep?.title || 'Unknown Title'}
                                        </h4>

                                        {/* Metadata */}
                                        <div className="space-y-2">
                                            {/* Filename */}
                                            <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                                </svg>
                                                <span className="truncate font-mono">{ep?.video_info?.filename || 'video.mp4'}</span>
                                            </div>

                                            {/* File Size */}
                                            {ep?.metadata?.size_formatted && (
                                                <div className="flex items-center gap-2 text-xs">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-purple-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                                                    </svg>
                                                    <span className="font-semibold text-purple-600 dark:text-purple-400">
                                                        {ep.metadata.size_formatted}
                                                    </span>
                                                </div>
                                            )}
                                        </div>

                                        {/* Action Buttons */}
                                        <div className="flex flex-col gap-2 pt-2">
                                            {/* Primary Actions */}
                                            <div className="flex gap-2">
                                                <button
                                                    onClick={() => copyToClipboard(ep?.video_url, idx)}
                                                    className="flex-1 px-3 py-2 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 rounded-lg text-xs font-medium transition-colors flex items-center justify-center gap-1"
                                                    title="Copy Default URL"
                                                >
                                                    {copied === idx ? (
                                                        <>
                                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                                            </svg>
                                                            Copied
                                                        </>
                                                    ) : (
                                                        <>
                                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                                            </svg>
                                                            Copy
                                                        </>
                                                    )}
                                                </button>

                                                <a
                                                    href={`http://127.0.0.1:8000/api/proxy?url=${encodeURIComponent(ep.video_url)}&filename=${encodeURIComponent(ep.video_info?.filename || 'episode.mp4')}`}
                                                    download
                                                    className="flex-1 px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xs font-medium transition-colors flex items-center justify-center gap-1 shadow-lg shadow-green-600/20"
                                                    title="Download Default"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                                    </svg>
                                                    Download
                                                </a>
                                            </div>

                                            {/* Qualities Dropdown / List */}
                                            {ep.sources && ep.sources.length > 1 && (
                                                <div className="relative group/qualities z-20">
                                                    <button className="w-full px-3 py-2 bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 hover:bg-purple-100 dark:hover:bg-purple-900/50 rounded-lg text-xs font-medium transition-colors flex items-center justify-center gap-1">
                                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                                                        </svg>
                                                        {ep.sources.length} Qualities Available
                                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                                        </svg>
                                                    </button>

                                                    {/* Dropdown Menu */}
                                                    <div className="absolute bottom-full left-0 w-full mb-1 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden hidden group-hover/qualities:block">
                                                        <div className="max-h-48 overflow-y-auto custom-scrollbar">
                                                            {ep.sources.map((source, sIdx) => (
                                                                <a
                                                                    key={sIdx}
                                                                    href={`http://127.0.0.1:8000/api/proxy?url=${encodeURIComponent(source.url)}&filename=${encodeURIComponent(ep.video_info?.filename?.replace('.mp4', `_${source.quality}.mp4`) || 'episode.mp4')}`}
                                                                    target="_blank"
                                                                    rel="noopener noreferrer"
                                                                    className="flex items-center justify-between px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 text-xs text-gray-700 dark:text-gray-200 border-b border-gray-100 dark:border-gray-700 last:border-0"
                                                                >
                                                                    <div className="flex flex-col">
                                                                        <span className="font-bold">{source.quality}</span>
                                                                        <span className="text-[10px] text-gray-400">{source.server}</span>
                                                                    </div>
                                                                    <div className="flex items-center gap-1">
                                                                        {source.metadata?.size && <span className="text-[10px] bg-gray-100 dark:bg-gray-600 px-1 rounded">{source.metadata.size}</span>}
                                                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                                                        </svg>
                                                                    </div>
                                                                </a>
                                                            ))}
                                                        </div>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </motion.div>
                </div>
            )}
        </div>
    );
});

export default SeasonDownloader;
