import argparse
import os
import time
import sys

from colorama import Fore, init

from extractors.general import GeneralExtractor
from extractors.hianime import HianimeExtractor
from extractors.instagram import InstagramExtractor

# Try to import enhanced features, fallback if not available
try:
    from tools.config_manager import ConfigManager
    from tools.user_interface import UserInterface
    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False

# Initialize colorama
init(autoreset=True)

class Main:
    def __init__(self):
        # Initialize enhanced features if available
        if ENHANCED_FEATURES:
            self.config_manager = ConfigManager()
            self.config = self.config_manager.get_config()
            self.ui = UserInterface()
            self.ui.print_banner()
        
        self.args = self.parse_args()
        extractor = self.get_extractor()
        
        if extractor:
            extractor.run()
        else:
            print(f"{Fore.LIGHTRED_EX}❌ Failed to initialize extractor")

    def get_extractor(self):
        if not self.args.link and not self.args.filename:
            os.system("cls" if os.name == "nt" else "clear")
            
            if ENHANCED_FEATURES:
                self.ui.print_section_header("Welcome to GDown Downloader")
                ans = input(
                    f"{Fore.LIGHTCYAN_EX}🔍 Provide a link or search for an anime:\n{Fore.LIGHTYELLOW_EX}"
                )
            else:
                ans = input(
                    f"{Fore.LIGHTGREEN_EX}GDown {Fore.LIGHTCYAN_EX}Downloader\n\nProvide a link or search for an anime:\n{Fore.LIGHTYELLOW_EX}"
                )
            
            if "http" in ans.lower():
                self.args.link = ans
            else:
                return HianimeExtractor(args=self.args, name=ans)

        if not self.args.link and self.args.filename:
            return HianimeExtractor(args=self.args, name=self.args.filename)
            return HianimeExtractor(args=self.args, name=self.args.filename)

        if "hianime" in self.args.link:
            return HianimeExtractor(args=self.args)
        if "instagram.com" in self.args.link:
            return InstagramExtractor(args=self.args)
        return GeneralExtractor(args=self.args)

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Anime downloader options")

        parser.add_argument(
            "--no-subtitles",
            action="store_true",
            help="Skip downloading subtitle files (.vtt)",
        )

        parser.add_argument(
            "-o",
            "--output-dir",
            type=str,
            default="output",
            help="Directory to save downloaded files",
        )

        parser.add_argument(
            "-n",
            "--filename",
            type=str,
            default="",
            help="Used for name of anime, or name of output file when using other extractor",
        )

        parser.add_argument(
            "--aria",
            action="store_true",
            default=False,
            help="Use aria2c as external downloader",
        )

        parser.add_argument(
            "-l",
            "--link",
            type=str,
            default=None,
            help="Provide link to desired content",
        )

        parser.add_argument(
            "--server", type=str, default=None, help="Streaming Server to download from"
        )

        return parser.parse_args()


if __name__ == "__main__":
    start = time.time()
    Main()
    elapsed = time.time() - start
    print(f"Took {int(elapsed / 60)}:{int((elapsed % 60))} to finish")
