"""
Server Extractors Module
Provides plugin-based architecture for extracting direct video links from file hosting servers
"""

from .factory import ExtractorFactory

__all__ = ["ExtractorFactory"]

