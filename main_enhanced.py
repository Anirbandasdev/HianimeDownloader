#!/usr/bin/env python3
"""
Enhanced main application for HiAnime Downloader
Provides smooth user experience with better error handling and progress tracking
"""

import sys
import os
import argparse
from typing import Optional

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.config_manager import ConfigManager, DownloadConfig
from tools.user_interface import UserInterface, ProgressTracker, NetworkStatusIndicator
from extractors.hianime import HianimeExtractor
from colorama import init

# Initialize colorama for Windows
init(autoreset=True)

class EnhancedHianimeApp:
    """Enhanced HiAnime Downloader with improved user experience"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        self.ui = UserInterface()
        self.progress = ProgressTracker()
        self.network_indicator = NetworkStatusIndicator()
        
    def parse_arguments(self):
        """Parse command line arguments with enhanced options"""
        parser = argparse.ArgumentParser(
            description="Enhanced HiAnime Downloader - Fast, Reliable, User-Friendly",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main_enhanced.py                                    # Interactive mode
  python main_enhanced.py -n "Demon Slayer"                 # Search for anime
  python main_enhanced.py -l "https://hianime.nz/watch/..." # Download from link
  python main_enhanced.py --config                          # Open configuration
            """
        )
        
        # Basic options
        parser.add_argument("-n", "--name", help="Name of the anime to search for")
        parser.add_argument("-l", "--link", help="Direct link to anime page")
        parser.add_argument("-o", "--output", help="Output directory", default=self.config.output_directory)
        
        # Quality and format options
        parser.add_argument("--quality", choices=["best", "worst", "720p", "1080p"], 
                          default=self.config.default_quality, help="Video quality preference")
        parser.add_argument("--no-subs", action="store_true", help="Skip subtitle download")
        parser.add_argument("--sub-lang", default=self.config.subtitle_language, help="Subtitle language")
        
        # Advanced options
        parser.add_argument("--server", help="Preferred server name")
        parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
        parser.add_argument("--config", action="store_true", help="Open configuration menu")
        parser.add_argument("--max-retries", type=int, default=self.config.max_retries, 
                          help="Maximum retry attempts")
        
        # Batch download options
        parser.add_argument("--batch", help="Batch download file (one anime per line)")
        parser.add_argument("--start-ep", type=int, help="Starting episode number")
        parser.add_argument("--end-ep", type=int, help="Ending episode number")
        
        return parser.parse_args()
    
    def show_configuration_menu(self):
        """Show interactive configuration menu"""
        self.ui.print_section_header("Configuration Settings")
        
        config_options = [
            f"Output Directory: {self.config.output_directory}",
            f"Default Quality: {self.config.default_quality}",
            f"Download Subtitles: {'Yes' if self.config.download_subtitles else 'No'}",
            f"Subtitle Language: {self.config.subtitle_language}",
            f"Max Concurrent Downloads: {self.config.max_concurrent_downloads}",
            f"Browser Headless Mode: {'Yes' if self.config.headless_browser else 'No'}",
            f"Max Retry Attempts: {self.config.max_retries}",
            f"SSL Verification: {'Yes' if self.config.verify_ssl else 'No'}",
            "Save and Exit"
        ]
        
        while True:
            print(f"\n{self.ui.Fore.LIGHTCYAN_EX}Current Configuration:")
            for i, option in enumerate(config_options, 1):
                print(f"{self.ui.Fore.LIGHTYELLOW_EX}  {i}. {option}")
            
            try:
                choice = input(f"\n{self.ui.Fore.LIGHTGREEN_EX}Select option to change (1-{len(config_options)}): ")
                choice_idx = int(choice) - 1
                
                if choice_idx == len(config_options) - 1:  # Save and Exit
                    self.config_manager.save_config(self.config)
                    self.ui.print_success("Configuration saved!")
                    break
                elif 0 <= choice_idx < len(config_options) - 1:
                    self._handle_config_change(choice_idx)
                    # Update the options display
                    config_options = [
                        f"Output Directory: {self.config.output_directory}",
                        f"Default Quality: {self.config.default_quality}",
                        f"Download Subtitles: {'Yes' if self.config.download_subtitles else 'No'}",
                        f"Subtitle Language: {self.config.subtitle_language}",
                        f"Max Concurrent Downloads: {self.config.max_concurrent_downloads}",
                        f"Browser Headless Mode: {'Yes' if self.config.headless_browser else 'No'}",
                        f"Max Retry Attempts: {self.config.max_retries}",
                        f"SSL Verification: {'Yes' if self.config.verify_ssl else 'No'}",
                        "Save and Exit"
                    ]
                else:
                    self.ui.print_error(f"Please enter a number between 1 and {len(config_options)}")
            
            except ValueError:
                self.ui.print_error("Please enter a valid number")
            except KeyboardInterrupt:
                print(f"\n{self.ui.Fore.LIGHTRED_EX}Configuration cancelled")
                break
    
    def _handle_config_change(self, option_idx: int):
        """Handle configuration option changes"""
        try:
            if option_idx == 0:  # Output Directory
                new_dir = input(f"Enter new output directory [{self.config.output_directory}]: ").strip()
                if new_dir:
                    self.config.output_directory = new_dir
            
            elif option_idx == 1:  # Default Quality
                qualities = ["best", "worst", "720p", "1080p"]
                quality = self.ui.get_user_choice("Select default quality:", qualities)
                self.config.default_quality = quality
            
            elif option_idx == 2:  # Download Subtitles
                self.config.download_subtitles = self.ui.confirm_action(
                    "Download subtitles by default?", self.config.download_subtitles
                )
            
            elif option_idx == 3:  # Subtitle Language
                new_lang = input(f"Enter subtitle language code [{self.config.subtitle_language}]: ").strip()
                if new_lang:
                    self.config.subtitle_language = new_lang
            
            elif option_idx == 4:  # Max Concurrent Downloads
                try:
                    new_max = int(input(f"Enter max concurrent downloads [{self.config.max_concurrent_downloads}]: "))
                    if 1 <= new_max <= 10:
                        self.config.max_concurrent_downloads = new_max
                    else:
                        self.ui.print_error("Please enter a number between 1 and 10")
                except ValueError:
                    self.ui.print_error("Please enter a valid number")
            
            elif option_idx == 5:  # Browser Headless Mode
                self.config.headless_browser = self.ui.confirm_action(
                    "Run browser in headless mode?", self.config.headless_browser
                )
            
            elif option_idx == 6:  # Max Retry Attempts
                try:
                    new_retries = int(input(f"Enter max retry attempts [{self.config.max_retries}]: "))
                    if 1 <= new_retries <= 20:
                        self.config.max_retries = new_retries
                    else:
                        self.ui.print_error("Please enter a number between 1 and 20")
                except ValueError:
                    self.ui.print_error("Please enter a valid number")
            
            elif option_idx == 7:  # SSL Verification
                self.config.verify_ssl = self.ui.confirm_action(
                    "Enable SSL verification?", self.config.verify_ssl
                )
            
        except KeyboardInterrupt:
            self.ui.print_info("Configuration change cancelled")
    
    def run_interactive_mode(self):
        """Run in interactive mode with enhanced UI"""
        self.ui.print_banner()
        
        # Get anime search query
        anime_name = input(f"\n{self.ui.Fore.LIGHTCYAN_EX}🔍 Enter anime name to search: {self.ui.Fore.LIGHTYELLOW_EX}")
        if not anime_name.strip():
            self.ui.print_error("Please enter a valid anime name")
            return
        
        return self._download_anime(anime_name=anime_name)
    
    def _download_anime(self, anime_name: Optional[str] = None, anime_link: Optional[str] = None):
        """Download anime with enhanced error handling and progress tracking"""
        try:
            # Create enhanced argument namespace
            args = argparse.Namespace()
            args.output_dir = self.config.output_directory
            args.server = None
            args.no_subtitles = not self.config.download_subtitles
            args.link = anime_link
            
            # Create extractor with enhanced configuration
            extractor = EnhancedHianimeExtractor(args, anime_name, self.config, self.progress, self.network_indicator)
            return extractor.run()
            
        except KeyboardInterrupt:
            self.ui.print_info("Download cancelled by user")
            return False
        except Exception as e:
            self.ui.print_error(f"Unexpected error: {e}")
            return False
    
    def run(self):
        """Main application entry point"""
        args = self.parse_arguments()
        
        # Handle configuration menu
        if args.config:
            self.show_configuration_menu()
            return
        
        # Update config with command line arguments
        if args.output:
            self.config.output_directory = args.output
        if args.max_retries:
            self.config.max_retries = args.max_retries
        if args.no_subs:
            self.config.download_subtitles = False
        if args.sub_lang:
            self.config.subtitle_language = args.sub_lang
        if args.headless:
            self.config.headless_browser = True
        
        # Handle different modes
        if args.batch:
            return self._run_batch_mode(args.batch)
        elif args.link:
            return self._download_anime(anime_link=args.link)
        elif args.name:
            return self._download_anime(anime_name=args.name)
        else:
            return self.run_interactive_mode()
    
    def _run_batch_mode(self, batch_file: str):
        """Run in batch mode for multiple anime"""
        self.ui.print_section_header("Batch Download Mode")
        
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                anime_list = [line.strip() for line in f.readlines() if line.strip()]
            
            if not anime_list:
                self.ui.print_error("Batch file is empty")
                return False
            
            self.ui.print_info(f"Found {len(anime_list)} anime in batch file")
            
            successful = 0
            failed = 0
            
            for i, anime_name in enumerate(anime_list, 1):
                print(f"\n{self.ui.Fore.LIGHTCYAN_EX}Processing {i}/{len(anime_list)}: {anime_name}")
                
                try:
                    if self._download_anime(anime_name=anime_name):
                        successful += 1
                    else:
                        failed += 1
                except Exception as e:
                    self.ui.print_error(f"Failed to download {anime_name}: {e}")
                    failed += 1
            
            # Summary
            self.ui.print_section_header("Batch Download Summary")
            print(f"{self.ui.Fore.LIGHTGREEN_EX}✅ Successful: {successful}")
            print(f"{self.ui.Fore.LIGHTRED_EX}❌ Failed: {failed}")
            print(f"{self.ui.Fore.LIGHTCYAN_EX}📊 Total: {len(anime_list)}")
            
            return successful > 0
            
        except FileNotFoundError:
            self.ui.print_error(f"Batch file not found: {batch_file}")
            return False
        except Exception as e:
            self.ui.print_error(f"Error processing batch file: {e}")
            return False

# Import the enhanced extractor (we'll create this next)
class EnhancedHianimeExtractor(HianimeExtractor):
    """Enhanced version of HianimeExtractor with better UX"""
    
    def __init__(self, args, name: str | None = None, config: DownloadConfig = None, 
                 progress: ProgressTracker = None, network_indicator: NetworkStatusIndicator = None):
        super().__init__(args, name)
        self.config = config or DownloadConfig()
        self.progress = progress or ProgressTracker()
        self.network_indicator = network_indicator or NetworkStatusIndicator()
        self.ui = UserInterface()
    
    def make_request_with_retry(self, url: str, max_retries: int = None, timeout: int = None, delay: float = None):
        """Enhanced request method with better user feedback"""
        max_retries = max_retries or self.config.max_retries
        timeout = timeout or self.config.timeout
        delay = delay or self.config.delay_between_retries
        
        self.network_indicator.show_connecting(url)
        
        response = super().make_request_with_retry(url, max_retries, timeout, delay)
        
        if response:
            self.network_indicator.show_success()
        else:
            self.network_indicator.show_failure("Connection failed after all retries")
            self.network_indicator.show_network_tips()
        
        return response

if __name__ == "__main__":
    app = EnhancedHianimeApp()
    try:
        success = app.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{UserInterface.Fore.LIGHTRED_EX}Application interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{UserInterface.Fore.LIGHTRED_EX}Fatal error: {e}")
        sys.exit(1)