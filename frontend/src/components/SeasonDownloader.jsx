import React, { useState, useEffect, useMemo } from 'react';
import { streamSeason } from '../api';

const SeasonDownloader = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [episodes, setEpisodes] = useState([]);
    const [progress, setProgress] = useState(null);
    const [copied, setCopied] = useState(null);
    const [selectedEpisodes, setSelectedEpisodes] = useState(new Set());

    // Sorting & Filtering
    const [sortBy, setSortBy] = useState('episode');
    const [sortOrder, setSortOrder] = useState('asc');
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        const savedUrl = localStorage.getItem('temp_season_url');
        if (savedUrl) {
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

        // Extract series name from first episode
        const firstTitle = episodes[0]?.title || '';
        const seriesName = firstTitle
            .replace(/\s*-?\s*(الحلقة|Episode|E|الموسم|Season|S)\s*\d+.*$/i, '')
            .replace(/\s*-?\s*\d+.*$/i, '')
            .trim() || 'Unknown Series';

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

    const handleFetch = async () => {
        if (!url) return;

        setLoading(true);
        setError(null);
        setEpisodes([]);
        setProgress(null);
        setSelectedEpisodes(new Set());

        try {
            await streamSeason(url, (data) => {
                if (data.type === 'start') {
                    setProgress({ current: 0, total: data.total, title: 'Starting...' });
                } else if (data.type === 'progress') {
                    setProgress({
                        current: data.current,
                        total: data.total,
                        title: `Processing: ${data.title}`
                    });
                } else if (data.type === 'result') {
                    setEpisodes(prev => [...prev, data.data]);
                } else if (data.type === 'error') {
                    console.error("Episode error:", data);
                }
            });
        } catch (err) {
            setError(err.message || 'Failed to fetch episodes');
        } finally {
            setLoading(false);
            setProgress(null);
        }
    };

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

    const downloadAll = () => {
        const selected = getSelectedEpisodes();
        if (selected.length === 0) return;

        const text = selected.map(ep => ep.video_url).join('\n');
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'episodes_list.txt';
        a.click();
        URL.revokeObjectURL(url);
    };

    const downloadIDM = () => {
        const selected = getSelectedEpisodes();
        if (selected.length === 0) return;

        let content = '';
        selected.forEach((ep) => {
            if (ep.video_url) {
                const index = episodes.indexOf(ep);
                content += `<\r\n${ep.video_url}\r\nfilename=${ep.video_info?.filename || `episode_${index + 1}.mp4`}\r\n>\r\n`;
            }
        });

        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'season_export.ef2';
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl transition-colors duration-200">

            <div className="flex flex-col md:flex-row gap-4 mb-8">
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Paste series or episode URL here..."
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
                                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4 truncate">
                                            {seasonMetadata.seriesName}
                                        </h2>

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
                                                onClick={downloadAll}
                                                disabled={selectedEpisodes.size === 0}
                                                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold shadow-lg shadow-blue-600/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2"
                                            >
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                                </svg>
                                                Save List
                                            </button>

                                            <button
                                                onClick={downloadIDM}
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
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 max-h-[800px] overflow-y-auto pr-2 custom-scrollbar">
                        {filteredAndSortedEpisodes.map((ep, idx) => (
                            <div
                                key={idx}
                                className={`group relative bg-white dark:bg-gray-800 rounded-2xl border-2 border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 overflow-hidden shadow-lg hover:shadow-2xl hover:scale-105 transform animate-fade-in ${idx < 8 ? `stagger-${(idx % 8) + 1}` : ''}`}
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
                                    {ep.thumbnail ? (
                                        <img
                                            src={ep.thumbnail}
                                            alt={ep.title}
                                            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
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
                                    <h4 className="font-bold text-gray-900 dark:text-white text-sm line-clamp-2 min-h-[2.5rem]" title={ep.title}>
                                        {ep.title}
                                    </h4>

                                    {/* Metadata */}
                                    <div className="space-y-2">
                                        {/* Filename */}
                                        <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                            </svg>
                                            <span className="truncate font-mono">{ep.video_info?.filename || 'video.mp4'}</span>
                                        </div>

                                        {/* File Size */}
                                        {ep.metadata?.size_formatted && (
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
                                    <div className="flex gap-2 pt-2">
                                        <button
                                            onClick={() => copyToClipboard(ep.video_url, idx)}
                                            className="flex-1 px-3 py-2 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 rounded-lg text-xs font-medium transition-colors flex items-center justify-center gap-1"
                                            title="Copy URL"
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
                                            title="Download"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                            </svg>
                                            Download
                                        </a>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default SeasonDownloader;
