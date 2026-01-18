import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const resolveUrl = async (url) => {
    try {
        const response = await axios.get(`${API_URL}/resolve`, { params: { url } });
        return response.data;
    } catch (error) {
        console.error("Error resolving URL:", error);
        throw error;
    }
};

export const getSeries = async (url) => {
    try {
        const response = await axios.get(`${API_URL}/series`, { params: { url } });
        return response.data;
    } catch (error) {
        console.error("Error getting series:", error);
        throw error;
    }
};

export const getSeason = async (url) => {
    try {
        const response = await axios.get(`${API_URL}/season`, { params: { url } });
        return response.data;
    } catch (error) {
        console.error("Error getting season:", error);
        throw error;
    }
};

export const streamSeason = async (url, onEvent) => {
    const fullUrl = `${API_URL}/season/stream?url=${encodeURIComponent(url)}`;

    try {
        const response = await fetch(fullUrl);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';


        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                break;
            }

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');

            // Process all complete lines
            buffer = lines.pop(); // Keep the last incomplete line in buffer

            for (const line of lines) {
                if (line.trim()) {
                    try {
                        const event = JSON.parse(line);
                        onEvent(event);
                    } catch (e) {
                        console.error("Error parsing JSON line:", e, "Line:", line);
                    }
                }
            }
        }
    } catch (error) {
        console.error("Error streaming season:", error);
        throw error;
    }
};

export const searchCartoons = async (query) => {
    try {
        const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error('Search failed');
        }
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error("Error searching cartoons:", error);
        throw error;
    }
};
