import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Download, Info } from 'lucide-react';

const VideoPlayer = ({ data, onBack }) => {
    const { video_url, video_info } = data;

    return (
        <div className="min-h-screen flex flex-col p-4 md:p-8 max-w-7xl mx-auto">
            <button
                onClick={onBack}
                className="self-start flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition-colors"
            >
                <ArrowLeft size={20} />
                <span>Back to Search</span>
            </button>

            <div className="w-full aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl border border-gray-800 relative group">
                <video
                    src={video_url}
                    controls
                    autoPlay
                    className="w-full h-full object-contain"
                />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-8"
            >
                <div className="md:col-span-2 space-y-6">
                    <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                        {video_info?.series_name || 'Unknown Series'}
                    </h2>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-400">
                        <span className="bg-gray-800 px-3 py-1 rounded-full border border-gray-700">
                            Season {video_info?.season || '?'}
                        </span>
                        <span className="bg-gray-800 px-3 py-1 rounded-full border border-gray-700">
                            Episode {video_info?.episode || '?'}
                        </span>
                    </div>

                    <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-800">
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                            <Info size={18} className="text-blue-400" />
                            Video Information
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-gray-400">
                            <div className="flex flex-col">
                                <span className="text-gray-500">Filename</span>
                                <span className="text-white truncate" title={video_info?.suggested_filename || video_info?.filename}>
                                    {video_info?.suggested_filename || video_info?.filename}
                                </span>
                            </div>
                            <div className="flex flex-col">
                                <span className="text-gray-500">Series ID</span>
                                <span className="text-white">{video_info?.series_id}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-800 h-fit">
                    <h3 className="text-lg font-semibold mb-4">Actions</h3>
                    <a
                        href={`http://127.0.0.1:8000/api/proxy?url=${encodeURIComponent(video_url)}&filename=${encodeURIComponent(video_info?.suggested_filename || '')}`}
                        download
                        className="flex items-center justify-center gap-2 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors"
                    >
                        <Download size={18} />
                        Download Video
                    </a>
                    <p className="text-xs text-gray-500 mt-4 text-center">
                        Right click the button and choose "Save Link As" if download doesn't start automatically.
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default VideoPlayer;
