import React from 'react';
import SeasonDownloader from './components/SeasonDownloader';
import { ThemeProvider } from './contexts/ThemeContext';
import { ColorThemeProvider } from './contexts/ColorThemeContext';
import ThemeToggle from './components/ThemeToggle';
import ThemePicker from './components/ThemePicker';

function App() {
  return (
    <ThemeProvider>
      <ColorThemeProvider>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
          <div className="container mx-auto px-4 py-8">
            <header className="flex justify-between items-center mb-12">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-600/20">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                </div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">
                  Arabic Toons <span className="text-blue-600">Downloader</span>
                </h1>
              </div>
              <div className="flex items-center gap-3">
                <ThemePicker />
                <ThemeToggle />
              </div>
            </header>

            <main className="max-w-4xl mx-auto">
              <div className="text-center mb-10">
                <h2 className="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
                  Download Full Series & Episodes
                </h2>
                <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                  Paste the series or episode link from Arabic Toons here to download in high quality and at lightning speed.
                </p>
              </div>

              <SeasonDownloader />
            </main>

            <footer className="mt-20 text-center text-gray-500 dark:text-gray-400 text-sm">
              <p>© 2025 Arabic Toons Downloader. Built for speed.</p>
            </footer>
          </div>
        </div>
      </ColorThemeProvider>
    </ThemeProvider>
  );
}

export default App;
