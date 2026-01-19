import sqlite3
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta
import json

DB_PATH = "cartoon.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
    return conn

def init_db():
    conn = get_db_connection()
    
    # Favorites table (existing)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            thumbnail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Series cache table (NEW) - with is_favorite for library
    conn.execute('''
        CREATE TABLE IF NOT EXISTS series (
            url TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            thumbnail TEXT,
            total_episodes INTEGER,
            is_favorite BOOLEAN DEFAULT 0,
            last_fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Episodes cache table (NEW) - with UNIQUE constraint to prevent duplicates
    conn.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_url TEXT NOT NULL,
            episode_number INTEGER NOT NULL,
            title TEXT,
            video_url TEXT,
            video_info TEXT,
            size_bytes INTEGER,
            thumbnail TEXT,
            episode_url TEXT,
            UNIQUE(series_url, episode_number),
            FOREIGN KEY(series_url) REFERENCES series(url) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# ============ FAVORITES FUNCTIONS (Existing) ============

def add_favorite(title: str, url: str, thumbnail: Optional[str] = None) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO favorites (title, url, thumbnail) VALUES (?, ?, ?)',
            (title, url, thumbnail)
        )
        conn.commit()
        fav_id = cursor.lastrowid
        conn.close()
        return {
            "id": fav_id,
            "title": title,
            "url": url,
            "thumbnail": thumbnail,
            "created_at": datetime.now().isoformat()
        }
    except sqlite3.IntegrityError:
        return get_favorite_by_url(url)
    except Exception as e:
        print(f"Error adding favorite: {e}")
        return None

def remove_favorite(url: str) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM favorites WHERE url = ?', (url,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        print(f"Error removing favorite: {e}")
        return False

def get_favorites() -> List[Dict]:
    conn = get_db_connection()
    favorites = conn.execute('SELECT * FROM favorites ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(ix) for ix in favorites]

def get_favorite_by_url(url: str) -> Optional[Dict]:
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM favorites WHERE url = ?', (url,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# ============ SERIES CACHE FUNCTIONS (NEW) ============

def upsert_series(url: str, title: str, thumbnail: Optional[str] = None, total_episodes: int = 0, is_favorite: bool = None) -> bool:
    """Insert or update series metadata. If is_favorite is None, preserve existing value."""
    try:
        conn = get_db_connection()
        if is_favorite is not None:
            conn.execute('''
                INSERT INTO series (url, title, thumbnail, total_episodes, is_favorite, last_fetched_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(url) DO UPDATE SET
                    title = excluded.title,
                    thumbnail = COALESCE(excluded.thumbnail, series.thumbnail),
                    total_episodes = excluded.total_episodes,
                    is_favorite = excluded.is_favorite,
                    last_fetched_at = CURRENT_TIMESTAMP
            ''', (url, title, thumbnail, total_episodes, is_favorite))
        else:
            conn.execute('''
                INSERT INTO series (url, title, thumbnail, total_episodes, last_fetched_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(url) DO UPDATE SET
                    title = excluded.title,
                    thumbnail = COALESCE(excluded.thumbnail, series.thumbnail),
                    total_episodes = excluded.total_episodes,
                    last_fetched_at = CURRENT_TIMESTAMP
            ''', (url, title, thumbnail, total_episodes))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error upserting series: {e}")
        return False

def get_series(url: str) -> Optional[Dict]:
    """Get series metadata by URL"""
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM series WHERE url = ?', (url,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def is_cache_fresh(series_url: str, max_age_hours: int = 24) -> bool:
    """Check if cached series data is still fresh"""
    series = get_series(series_url)
    if not series:
        return False
    
    last_fetched = datetime.fromisoformat(series['last_fetched_at'])
    age = datetime.now() - last_fetched
    return age < timedelta(hours=max_age_hours)

# ============ EPISODE CACHE FUNCTIONS (NEW) ============

def upsert_episode(series_url: str, episode_number: int, title: str, 
                   video_url: str, video_info: Dict, size_bytes: int,
                   thumbnail: str, episode_url: str) -> bool:
    """Insert or update a single episode"""
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO episodes (series_url, episode_number, title, video_url, video_info, size_bytes, thumbnail, episode_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(series_url, episode_number) DO UPDATE SET
                title = excluded.title,
                video_url = excluded.video_url,
                video_info = excluded.video_info,
                size_bytes = excluded.size_bytes,
                thumbnail = excluded.thumbnail,
                episode_url = excluded.episode_url
        ''', (series_url, episode_number, title, video_url, json.dumps(video_info), size_bytes, thumbnail, episode_url))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error upserting episode: {e}")
        return False

def get_cached_episodes(series_url: str) -> List[Dict]:
    """Get all cached episodes for a series"""
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT * FROM episodes WHERE series_url = ? ORDER BY episode_number ASC',
        (series_url,)
    ).fetchall()
    conn.close()
    
    episodes = []
    for row in rows:
        ep = dict(row)
        # Parse video_info JSON back to dict
        if ep.get('video_info'):
            try:
                ep['video_info'] = json.loads(ep['video_info'])
            except:
                ep['video_info'] = {}
        episodes.append(ep)
    return episodes

def clear_series_cache(series_url: str) -> bool:
    """Delete all cached data for a series"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM episodes WHERE series_url = ?', (series_url,))
        conn.execute('DELETE FROM series WHERE url = ?', (series_url,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing series cache: {e}")
        return False

# ============ LIBRARY/FAVORITES FUNCTIONS (v4.1) ============

def toggle_favorite(url: str, title: str = None, thumbnail: str = None) -> Dict:
    """Toggle favorite status for a series. Creates series if it doesn't exist."""
    try:
        conn = get_db_connection()
        
        # Check if series exists
        existing = conn.execute('SELECT * FROM series WHERE url = ?', (url,)).fetchone()
        
        if existing:
            # Toggle existing
            new_status = not existing['is_favorite']
            conn.execute('UPDATE series SET is_favorite = ? WHERE url = ?', (new_status, url))
            conn.commit()
            result = dict(existing)
            result['is_favorite'] = new_status
        else:
            # Create new series with favorite status
            conn.execute('''
                INSERT INTO series (url, title, thumbnail, total_episodes, is_favorite, last_fetched_at)
                VALUES (?, ?, ?, 0, 1, CURRENT_TIMESTAMP)
            ''', (url, title or 'Unknown Series', thumbnail))
            conn.commit()
            result = {
                'url': url,
                'title': title or 'Unknown Series',
                'thumbnail': thumbnail,
                'total_episodes': 0,
                'is_favorite': True
            }
        
        conn.close()
        return result
    except Exception as e:
        print(f"Error toggling favorite: {e}")
        return None

def is_favorite(url: str) -> bool:
    """Check if a series is marked as favorite"""
    conn = get_db_connection()
    row = conn.execute('SELECT is_favorite FROM series WHERE url = ?', (url,)).fetchone()
    conn.close()
    return bool(row and row['is_favorite'])

def get_favorite_series() -> List[Dict]:
    """Get all series marked as favorites"""
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT url, title, thumbnail, total_episodes, is_favorite, last_fetched_at
        FROM series 
        WHERE is_favorite = 1 
        ORDER BY last_fetched_at DESC
    ''').fetchall()
    conn.close()
    return [dict(row) for row in rows]
