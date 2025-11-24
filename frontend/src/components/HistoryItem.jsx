import React from 'react';
import { motion } from 'framer-motion';
import { Trash2, Clock, HardDrive, Film } from 'lucide-react';
import { historyStorage } from '../utils/historyStorage';

const HistoryItem = ({ item, onSelect, onRemove }) => {
    return (
        <div
            className="group relative p-4 bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer"
            onClick={() => onSelect(item)}
        >
            <div className="flex gap-4">
                {/* Poster */}
                <div className="shrink-0 relative">
                    {item.poster ? (
                        <img
                            src={item.poster}
                            alt={item.seriesName}
                            className="w-16 h-24 rounded-lg object-cover border border-gray-200 dark:border-gray-600 shadow-sm group-hover:shadow-md transition-shadow"
                        />
                    ) : (
                        <div className="w-16 h-24 rounded-lg bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center border border-gray-200 dark:border-gray-600 shadow-sm">
                            <Film className="w-8 h-8 text-white" />
                        </div>
                    )}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0 flex flex-col justify-center">
                    <h4 className="font-bold text-gray-900 dark:text-white text-base truncate mb-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                        {item.seriesName}
                    </h4>

                    <div className="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400 mb-2">
                        <span className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">
                            <Film size={12} />
                            {item.selectedCount} eps
                        </span>
                        <span className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">
                            <HardDrive size={12} />
                            {item.totalSize}
                        </span>
                    </div>

                    <div className="flex items-center gap-1 text-xs text-gray-400 dark:text-gray-500">
                        <Clock size={12} />
                        <span>{historyStorage.getTimeAgo(item.timestamp)}</span>
                    </div>
                </div>

                {/* Remove Button */}
                <motion.button
                    whileHover={{ scale: 1.1, color: '#ef4444' }}
                    whileTap={{ scale: 0.9 }}
                    onClick={(e) => {
                        e.stopPropagation();
                        onRemove(item.id);
                    }}
                    className="shrink-0 p-2 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity self-center"
                    title="Remove from history"
                >
                    <Trash2 size={20} />
                </motion.button>
            </div>
        </div>
    );
};

export default HistoryItem;
