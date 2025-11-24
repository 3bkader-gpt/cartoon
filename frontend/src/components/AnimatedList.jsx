import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const container = {
    hidden: { opacity: 0 },
    show: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1
        }
    }
};

const itemAnimation = {
    hidden: { opacity: 0, y: 20, scale: 0.95 },
    show: {
        opacity: 1,
        y: 0,
        scale: 1,
        transition: {
            type: "spring",
            stiffness: 300,
            damping: 24
        }
    },
    exit: {
        opacity: 0,
        x: -20,
        transition: { duration: 0.2 }
    }
};

const AnimatedList = ({ items, renderItem, className = "" }) => {
    return (
        <motion.div
            variants={container}
            initial="hidden"
            animate="show"
            className={`flex flex-col ${className}`}
        >
            <AnimatePresence mode='popLayout'>
                {items.map((item, index) => (
                    <motion.div
                        key={item.id || index}
                        variants={itemAnimation}
                        layout
                        custom={index}
                    >
                        {renderItem(item, index)}
                    </motion.div>
                ))}
            </AnimatePresence>
        </motion.div>
    );
};

export default AnimatedList;
