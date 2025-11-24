"""
EgyDead Site Module
"""

from .scraper import EgyDeadScraper
from .parser import EgyDeadParser
from .config import SITE_NAME, BASE_URL, SUPPORTED_PATTERNS

__all__ = ['EgyDeadScraper', 'EgyDeadParser', 'SITE_NAME', 'BASE_URL', 'SUPPORTED_PATTERNS']
