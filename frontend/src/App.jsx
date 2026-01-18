import React, { useRef, useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SeasonDownloader from './components/SeasonDownloader';
import Navbar from './components/Navbar';
import Library from './pages/Library';
import Settings from './pages/Settings';
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  const seasonDownloaderRef = useRef(null);
  const [isDark, setIsDark] = useState(true);

  // Initialize dark mode
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setIsDark(savedTheme === 'dark');
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = isDark ? 'light' : 'dark';
    setIsDark(!isDark);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  const handleSelectHistory = (url) => {
    // This prop might need refactoring if it needs to work across routes
    // For now, if we are on Home, we can direct it
    if (seasonDownloaderRef.current) {
      seasonDownloaderRef.current.loadFromHistory(url);
    } else {
      // If not on home, native Home navigation with state?
      // For simplicity v3.1, assuming history is mainly used on Home
      window.location.href = `/?url=${encodeURIComponent(url)}`;
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200 font-sans">
        <Navbar isDark={isDark} onToggleTheme={toggleTheme} />

        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={
              <div className="max-w-4xl mx-auto">
                <div className="text-center mb-10">
                  <h2 className="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
                    Download Full Series & Episodes
                  </h2>
                  <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                    Paste the series or episode link from Arabic Toons here to download in high quality and at lightning speed.
                  </p>
                </div>
                <ErrorBoundary>
                  <SeasonDownloader ref={seasonDownloaderRef} />
                </ErrorBoundary>
              </div>
            } />
            <Route path="/library" element={<Library />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>

        <footer className="mt-20 text-center text-gray-500 dark:text-gray-400 text-sm pb-8">
          <p>© 2025 Arabic Toons Downloader (v3.1). Built for speed.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
