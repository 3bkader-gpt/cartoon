import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

const SimplePlayer = ({ videoUrl, title, onClose }) => {
    return (
        <AnimatePresence>
            {videoUrl && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4"
                    onClick={onClose}
                >
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        className="relative w-full max-w-5xl bg-black rounded-2xl overflow-hidden shadow-2xl border border-gray-800"
                        onClick={(e) => e.stopPropagation()}
                    >
                        {/* Header */}
                        <div className="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/80 to-transparent z-10 flex justify-between items-start">
                            <h3 className="text-white font-medium text-lg drop-shadow-md px-2">
                                {title}
                            </h3>
                            <button
                                onClick={onClose}
                                className="p-2 bg-black/50 hover:bg-white/20 rounded-full text-white transition-colors backdrop-blur-md"
                            >
                                <X size={24} />
                            </button>
                        </div>

                        {/* Video Player */}
                        <div className="aspect-video bg-black">
                            <video
                                src={videoUrl}
                                controls
                                autoPlay
                                className="w-full h-full"
                                controlsList="nodownload"
                            >
                                Your browser does not support the video tag.
                            </video>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default SimplePlayer;
