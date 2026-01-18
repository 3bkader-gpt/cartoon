"""
Extractor Factory
Routes URLs to appropriate extractor instances
"""

import logging
from typing import Dict, Type
from urllib.parse import urlparse
from playwright.sync_api import BrowserContext

from .base import BaseExtractor
from .generic import GenericExtractor
from .servers.forafile import ForafileExtractor
from .servers.uqload import UqloadExtractor
from .servers.multi_server import MultiServerExtractor

logger = logging.getLogger(__name__)

class ExtractorFactory:
    """
    Factory for creating appropriate extractor instances based on URL
    
    Maintains a registry of server patterns and their extractor classes
    """
    
    # Registry mapping server domain patterns to extractor classes
    _registry: Dict[str, Type[BaseExtractor]] = {
        "forafile": ForafileExtractor,
        "forafile.com": ForafileExtractor,
        "uqload": UqloadExtractor,
        "uqload.co": UqloadExtractor,
        "uqload.io": UqloadExtractor,
        "uqload.com": UqloadExtractor,
        # Multi Download servers
        "haxloppd": MultiServerExtractor,
        "haxloppd.com": MultiServerExtractor,
        "premilkyway": MultiServerExtractor,
        "hglink": MultiServerExtractor,
        "hglink.to": MultiServerExtractor,
        "cavanhabg": MultiServerExtractor,
        "cavanhabg.com": MultiServerExtractor,
        # "doodstream": DoodStreamExtractor,
        # "vidbom": VidBomExtractor,
    }
    
    @classmethod
    def get_extractor(cls, url: str, browser_context: BrowserContext) -> BaseExtractor:
        """
        Get appropriate extractor for the given URL
        
        Args:
            url: Server URL to extract from
            browser_context: Playwright BrowserContext for extractor
            
        Returns:
            BaseExtractor instance (specific extractor or GenericExtractor)
        """
        # Parse URL to get domain
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Check registry for matching server
            for pattern, extractor_class in cls._registry.items():
                if pattern in domain or pattern in path:
                    logger.info(f"Matched {pattern} extractor for URL: {url}")
                    return extractor_class(browser_context)
            
            # No match found, use generic extractor
            logger.info(f"No specific extractor found for {url}, using GenericExtractor")
            return GenericExtractor(browser_context)
            
        except Exception as e:
            logger.warning(f"Error parsing URL {url}: {e}, using GenericExtractor")
            return GenericExtractor(browser_context)
    
    @classmethod
    def needs_extraction(cls, url: str) -> bool:
        """
        Check if a URL needs extraction (matches a known server pattern)
        
        Args:
            url: URL to check
            
        Returns:
            True if URL matches a known server pattern
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Check registry for matching server
            for pattern in cls._registry.keys():
                if pattern in domain or pattern in path:
                    return True
            
            return False
        except Exception:
            return False
    
    @classmethod
    def register_extractor(cls, pattern: str, extractor_class: Type[BaseExtractor]):
        """
        Register a new extractor pattern (for future use)
        
        Args:
            pattern: Domain or URL pattern to match
            extractor_class: Extractor class to use
        """
        cls._registry[pattern] = extractor_class
        logger.info(f"Registered extractor {extractor_class.__name__} for pattern: {pattern}")

