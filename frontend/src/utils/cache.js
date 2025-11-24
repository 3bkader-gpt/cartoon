/**
 * IndexedDB Cache Manager for Seasons & Episodes
 * Provides instant loading for previously fetched seasons
 */

const DB_NAME = 'CartoonDownloaderDB';
const DB_VERSION = 2;
const SEASONS_STORE = 'seasons';
const EPISODES_STORE = 'episodes';

class CacheManager {
    constructor() {
        this.db = null;
    }

    /**
     * Initialize IndexedDB
     */
    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(DB_NAME, DB_VERSION);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // Create seasons store
                if (!db.objectStoreNames.contains(SEASONS_STORE)) {
                    const seasonsStore = db.createObjectStore(SEASONS_STORE, { keyPath: 'season_url' });
                    seasonsStore.createIndex('cached_at', 'cached_at', { unique: false });
                }

                // Recreate episodes store with correct schema
                if (db.objectStoreNames.contains(EPISODES_STORE)) {
                    db.deleteObjectStore(EPISODES_STORE);
                }
                const episodesStore = db.createObjectStore(EPISODES_STORE, {
                    autoIncrement: true
                });
                episodesStore.createIndex('season_url', 'season_url', { unique: false });
            };
        });
    }

    /**
     * Check if season exists in cache
     */
    async checkCache(seasonUrl) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([SEASONS_STORE], 'readonly');
            const store = transaction.objectStore(SEASONS_STORE);
            const request = store.get(seasonUrl);

            request.onsuccess = () => resolve(request.result || null);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Get all episodes for a season
     */
    async getEpisodes(seasonUrl) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([EPISODES_STORE], 'readonly');
            const store = transaction.objectStore(EPISODES_STORE);
            const index = store.index('season_url');
            const request = index.getAll(seasonUrl);

            request.onsuccess = () => resolve(request.result || []);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Save season metadata and episodes to cache
     */
    async saveSeason(seasonUrl, metadata, episodes) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([SEASONS_STORE, EPISODES_STORE], 'readwrite');

            // Save season metadata
            const seasonData = {
                season_url: seasonUrl,
                season_title: metadata.seriesName,
                poster_url: metadata.poster,
                episodes_count: metadata.totalEpisodes,
                total_size: metadata.totalSize,
                cached_at: new Date().toISOString()
            };

            const seasonsStore = transaction.objectStore(SEASONS_STORE);
            seasonsStore.put(seasonData);

            // Save episodes
            const episodesStore = transaction.objectStore(EPISODES_STORE);
            episodes.forEach((episode, index) => {
                const episodeData = {
                    season_url: seasonUrl,
                    episode_number: index,
                    episode_title: episode.title,
                    video_url: episode.video_url,
                    video_info: episode.video_info,
                    metadata: episode.metadata,
                    thumbnail: episode.thumbnail,
                    episode_url: episode.episode_url
                };
                episodesStore.put(episodeData);
            });

            transaction.oncomplete = () => resolve(true);
            transaction.onerror = () => reject(transaction.error);
        });
    }

    /**
     * Delete season and its episodes from cache
     */
    async deleteSeason(seasonUrl) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([SEASONS_STORE, EPISODES_STORE], 'readwrite');

            // Delete season
            const seasonsStore = transaction.objectStore(SEASONS_STORE);
            seasonsStore.delete(seasonUrl);

            // Delete episodes
            const episodesStore = transaction.objectStore(EPISODES_STORE);
            const index = episodesStore.index('season_url');
            const request = index.openCursor(IDBKeyRange.only(seasonUrl));

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    cursor.delete();
                    cursor.continue();
                }
            };

            transaction.oncomplete = () => resolve(true);
            transaction.onerror = () => reject(transaction.error);
        });
    }

    /**
     * Get full season data (metadata + episodes)
     */
    async getFullSeason(seasonUrl) {
        const metadata = await this.checkCache(seasonUrl);
        if (!metadata) return null;

        const episodes = await this.getEpisodes(seasonUrl);
        return {
            metadata,
            episodes
        };
    }

    /**
     * Clear all cache
     */
    async clearAll() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([SEASONS_STORE, EPISODES_STORE], 'readwrite');

            transaction.objectStore(SEASONS_STORE).clear();
            transaction.objectStore(EPISODES_STORE).clear();

            transaction.oncomplete = () => resolve(true);
            transaction.onerror = () => reject(transaction.error);
        });
    }

    /**
     * Get cache statistics
     */
    async getStats() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([SEASONS_STORE, EPISODES_STORE], 'readonly');

            const seasonsRequest = transaction.objectStore(SEASONS_STORE).count();
            const episodesRequest = transaction.objectStore(EPISODES_STORE).count();

            let stats = {};

            seasonsRequest.onsuccess = () => {
                stats.seasons = seasonsRequest.result;
            };

            episodesRequest.onsuccess = () => {
                stats.episodes = episodesRequest.result;
            };

            transaction.oncomplete = () => resolve(stats);
            transaction.onerror = () => reject(transaction.error);
        });
    }
}

// Singleton instance
const cacheManager = new CacheManager();

export default cacheManager;
