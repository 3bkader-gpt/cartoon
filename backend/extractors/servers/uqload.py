from ..base import BaseExtractor, ExtractionResult
import re

class UqloadExtractor(BaseExtractor):
    def extract(self, url: str) -> ExtractionResult:
        self.logger.info(f"UqloadExtractor processing: {url}")
        
        # 1. Navigate to page
        self.page.goto(url, wait_until="domcontentloaded")
        
        # 2. Check for Overlay/Click to play
        # Uqload usually needs a click to start logic or remove overlay
        try:
            # Try specific play button mask often used by Uqload
            play_mask = self.page.locator("div.vjs-poster, div.vjs-big-play-button")
            if play_mask.count() > 0 and play_mask.first.is_visible():
                self.logger.info("Clicking play mask/button to trigger video...")
                # Handling generic popup if it occurs on click
                with self.handle_popups():
                    play_mask.first.click(timeout=5000)
                self.page.wait_for_timeout(1000)
        except Exception as e:
            self.logger.debug(f"Handling play button failed (might not exist): {e}")

        # 3. Extract Video URL
        # Method A: Direct Video Source in DOM
        video_url = self.find_video_tag_source()
        if video_url:
            return ExtractionResult(
                video_url=video_url,
                quality="720p", # Uqload is usually 720p
                server="Uqload"
            )

        # Method B: Regex in Script tags (Packer or simple var)
        content = self.page.content()
        sources = re.findall(r'sources:\s*\["([^"]+)"\]', content)
        if sources and sources[0].endswith(".mp4"):
             return ExtractionResult(
                video_url=sources[0],
                quality="720p",
                server="Uqload"
            )

        # Method C: Generic Fallback logic from Base
        # Usually base extractors are good at finding hidden sources
        
        return None
