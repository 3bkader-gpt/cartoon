// Download History Storage Utility
// Manages download history in localStorage

const HISTORY_KEY = 'download_history';
const MAX_HISTORY_ITEMS = 10;

export const historyStorage = {
    // Get all history items
    getHistory() {
        try {
            const history = localStorage.getItem(HISTORY_KEY);
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Error reading history:', error);
            return [];
        }
    },

    // Add new history item
    addHistory(item) {
        try {
            const history = this.getHistory();

            // Create history entry
            const entry = {
                id: Date.now(),
                seriesName: item.seriesName,
                url: item.url,
                episodeCount: item.episodeCount,
                totalSize: item.totalSize,
                totalSizeBytes: item.totalSizeBytes,
                selectedCount: item.selectedCount,
                timestamp: new Date().toISOString(),
                poster: item.poster || null,
            };

            // Check if URL already exists
            const existingIndex = history.findIndex(h => h.url === item.url);

            if (existingIndex !== -1) {
                // Update existing entry
                history[existingIndex] = entry;
            } else {
                // Add new entry at the beginning
                history.unshift(entry);

                // Keep only last MAX_HISTORY_ITEMS
                if (history.length > MAX_HISTORY_ITEMS) {
                    history.pop();
                }
            }

            localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
            return entry;
        } catch (error) {
            console.error('Error adding history:', error);
            return null;
        }
    },

    // Remove history item by id
    removeHistory(id) {
        try {
            const history = this.getHistory();
            const filtered = history.filter(item => item.id !== id);
            localStorage.setItem(HISTORY_KEY, JSON.stringify(filtered));
            return filtered;
        } catch (error) {
            console.error('Error removing history:', error);
            return this.getHistory();
        }
    },

    // Clear all history
    clearHistory() {
        try {
            localStorage.removeItem(HISTORY_KEY);
            return [];
        } catch (error) {
            console.error('Error clearing history:', error);
            return this.getHistory();
        }
    },

    // Get stats
    getStats() {
        const history = this.getHistory();
        const totalSizeBytes = history.reduce((sum, item) => sum + (item.totalSizeBytes || 0), 0);

        const formatSize = (bytes) => {
            if (bytes === 0) return '0 B';
            if (bytes >= 1024 * 1024 * 1024) {
                return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
            } else if (bytes >= 1024 * 1024) {
                return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
            } else {
                return `${(bytes / 1024).toFixed(2)} KB`;
            }
        };

        return {
            count: history.length,
            totalEpisodes: history.reduce((sum, item) => sum + (item.selectedCount || 0), 0),
            totalSize: formatSize(totalSizeBytes),
            lastUsed: history.length > 0 ? new Date(history[0].timestamp) : null,
        };
    },

    // Format time ago
    getTimeAgo(timestamp) {
        const now = new Date();
        const past = new Date(timestamp);
        const diffMs = now - past;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) > 1 ? 's' : ''} ago`;
        return `${Math.floor(diffDays / 30)} month${Math.floor(diffDays / 30) > 1 ? 's' : ''} ago`;
    },
};
