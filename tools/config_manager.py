#!/usr/bin/env python3
"""
Configuration management for HiAnime Downloader
Provides easy customization and settings management
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class DownloadConfig:
    """Configuration settings for the downloader"""
    # Network settings
    max_retries: int = 5
    timeout: int = 30
    delay_between_retries: float = 2.0
    verify_ssl: bool = False
    
    # Download settings
    default_quality: str = "best"
    download_subtitles: bool = True
    subtitle_language: str = "en"
    max_concurrent_downloads: int = 3
    
    # Browser settings
    headless_browser: bool = True
    browser_timeout: int = 30
    page_load_wait: int = 5
    
    # Output settings
    output_directory: str = "downloads"
    create_season_folders: bool = True
    filename_template: str = "{anime_name} - S{season:02d}E{episode:02d} - {episode_title}"
    
    # User agent rotation
    rotate_user_agents: bool = True
    user_agents: list = None
    
    def __post_init__(self):
        if self.user_agents is None:
            self.user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]

class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> DownloadConfig:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                return DownloadConfig(**config_dict)
            except Exception as e:
                print(f"Error loading config: {e}")
                print("Using default configuration...")
        
        # Create default config
        config = DownloadConfig()
        self.save_config(config)
        return config
    
    def save_config(self, config: DownloadConfig) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_config(self) -> DownloadConfig:
        """Get current configuration"""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration with new values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save_config(self.config)