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
                    <div className="flex justify-between items-center pb-4 border-b border-gray-100 dark:border-gray-700">
                        <h3 className="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
                            <span className="bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 px-3 py-1 rounded-full text-sm">
                                {filteredAndSortedEpisodes.length}
                            </span>
                            Episodes
                            <span className="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">
                                ({selectedEpisodes.size} selected)
                            </span>
                        </h3>
                        <div className="flex gap-3">
                            <button
                                onClick={downloadAll}
                                disabled={selectedEpisodes.size === 0}
                                className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                Save List
                            </button>
                            <button
                                onClick={downloadIDM}
                                disabled={selectedEpisodes.size === 0}
                                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors flex items-center gap-2 shadow-lg shadow-green-600/20 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                Export to IDM
                            </button>
                        </div>
                    </div>

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

                    <div className="flex items-center gap-2 px-2">
                        <input
                            type="checkbox"
                            checked={selectedEpisodes.size === filteredAndSortedEpisodes.length && filteredAndSortedEpisodes.length > 0}
                            onChange={toggleSelectAll}
                            className="w-5 h-5 rounded border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-blue-600 focus:ring-blue-500 cursor-pointer"
                        />
                        <span className="text-gray-700 dark:text-gray-300 text-sm font-medium">
                            Select All
                        </span>
                    </div>

                    <div className="grid gap-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                        {filteredAndSortedEpisodes.map((ep, idx) => (
                            <div
                                key={idx}
                                className="group flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-white dark:hover:bg-gray-700 rounded-xl border border-transparent hover:border-gray-200 dark:hover:border-gray-600 transition-all duration-200"
                            >
                                <div className="flex items-center gap-4 overflow-hidden">
                                    <input
                                        type="checkbox"
                                        checked={selectedEpisodes.has(idx)}
                                        onChange={() => toggleSelection(idx)}
                                        className="w-5 h-5 rounded border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-blue-600 focus:ring-blue-500 cursor-pointer shrink-0"
                                    />

                                    {ep.thumbnail ? (
                                        <img
                                            src={ep.thumbnail}
                                            alt={ep.title}
                                            className="w-16 h-16 rounded-lg object-cover shrink-0 border border-gray-200 dark:border-gray-600"
                                        />
                                    ) : (
                                        <div className="w-16 h-16 rounded-lg bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 flex items-center justify-center shrink-0 border border-gray-200 dark:border-gray-600">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-400 dark:text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                            </svg>
                                        </div>
                                    )}

                                    <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-sm shrink-0">
                                        {idx + 1}
                                    </div>
                                    <div className="min-w-0">
                                        <h4 className="font-medium text-gray-900 dark:text-white truncate" title={ep.title}>
                                            {ep.title}
                                        </h4>
                                        <div className="flex items-center gap-2 mt-0.5">
                                            <p className="text-xs text-gray-500 dark:text-gray-400 truncate font-mono">
                                                {ep.video_info?.filename || 'video.mp4'}
                                            </p>
                                            {ep.metadata?.size_formatted && (
                                                <>
                                                    <span className="text-xs text-gray-400 dark:text-gray-500">•</span>
                                                    <span className="text-xs text-blue-600 dark:text-blue-400 font-medium">
                                                        {ep.metadata.size_formatted}
                                                    </span>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                <div className="flex items-center gap-2 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button
                                        onClick={() => copyToClipboard(ep.video_url, idx)}
                                        className="p-2 text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors relative"
                                        title="Copy URL"
                                    >
                                        {copied === idx ? (
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-500" viewBox="0 0 20 20" fill="currentColor">
                                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                            </svg>
                                        ) : (
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                            </svg>
                                        )}
                                    </button>
                                    <a
                                        href={`http://127.0.0.1:8000/api/proxy?url=${encodeURIComponent(ep.video_url)}&filename=${encodeURIComponent(ep.video_info?.filename || 'episode.mp4')}`}
                                        download
                                        className="p-2 text-gray-500 hover:text-green-600 dark:text-gray-400 dark:hover:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 rounded-lg transition-colors"
                                        title="Download Direct (Fixes 403 Error)"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                        </svg>
                                    </a>
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
