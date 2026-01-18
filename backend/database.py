import sqlite3
from typing import List, Dict, Optional
import os
from datetime import datetime

DB_PATH = "cartoon.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            thumbnail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

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
        # Already exists
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
