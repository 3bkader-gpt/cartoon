import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Play, Download as DownloadIcon } from 'lucide-react';

const EpisodeCard = ({ episode, index, isSelected, onToggle, onPlay }) => {
    const { title, video_url, video_info } = episode;

    // Generate a unique gradient for each episode
    const gradients = [
        'from-blue-500 to-purple-600',
        'from-purple-500 to-pink-600',
        'from-pink-500 to-red-600',
        'from-red-500 to-orange-600',
        'from-orange-500 to-yellow-600',
        'from-green-500 to-teal-600',
        'from-teal-500 to-cyan-600',
        'from-cyan-500 to-blue-600',
    ];

    const gradient = gradients[index % gradients.length];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isSelected ? 1 : 0.6, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className={`group relative bg-white dark:bg-gray-900 rounded-xl overflow-hidden border-2 transition-all duration-300 ${isSelected
                    ? 'border-blue-500 dark:border-blue-400 shadow-lg shadow-blue-500/20'
                    : 'border-gray-200 dark:border-gray-800 hover:border-gray-300 dark:hover:border-gray-700'
                }`}
        >
            {/* Checkbox */}
            <div className="absolute top-3 left-3 z-10">
                <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={onToggle}
                    className="w-5 h-5 rounded border-2 border-white dark:border-gray-700 bg-white/90 dark:bg-gray-800/90 text-blue-600 focus:ring-2 focus:ring-blue-500 cursor-pointer"
                />
            </div>

            {/* Status Badge */}
            {video_url && (
                <div className="absolute top-3 right-3 z-10">
                    <div className="bg-green-500 text-white text-xs px-2 py-1 rounded-full flex items-center gap-1">
                        <CheckCircle size={12} />
                        <span>Ready</span>
                    </div>
                </div>
            )}

            {/* Thumbnail */}
            <div className={`relative h-40 bg-gradient-to-br ${gradient} flex items-center justify-center overflow-hidden`}>
                {/* Episode Number Overlay */}
                <div className="absolute inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center">
                    <div className="text-center">
                        <div className="text-6xl font-bold text-white/90 drop-shadow-lg">
                            {index + 1}
                        </div>
                        <div className="text-sm text-white/80 mt-1">Episode</div>
                    </div>
                </div>

                {/* Play Button Overlay (on hover) */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileHover={{ opacity: 1, scale: 1 }}
                    className="absolute inset-0 bg-black/40 flex items-center justify-center cursor-pointer"
                    onClick={onPlay}
                >
                    <motion.div
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                        className="bg-white/90 dark:bg-gray-900/90 rounded-full p-4 shadow-xl"
                    >
                        <Play size={32} className="text-blue-600 dark:text-blue-400" fill="currentColor" />
                    </motion.div>
                </motion.div>
            </div>

            {/* Content */}
            <div className="p-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                    {title || `Episode ${index + 1}`}
                </h3>

                {/* File Info */}
                {video_info?.filename && (
                    <div className="text-xs text-gray-500 dark:text-gray-400 mb-2 font-mono truncate">
                        {video_info.filename}
                    </div>
                )}

                {/* Actions */}
                {video_url && (
                    <div className="flex gap-2 mt-3">
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={onPlay}
                            className="flex-1 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white text-sm py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition-colors"
                        >
                            <Play size={14} />
                            Play
                        </motion.button>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => {
                                navigator.clipboard.writeText(video_url);
                            }}
                            className="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-900 dark:text-white text-sm py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition-colors"
                        >
                            <DownloadIcon size={14} />
                            Copy
                        </motion.button>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default EpisodeCard;
