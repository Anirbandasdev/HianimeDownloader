#!/usr/bin/env python3
"""
Progress tracking and user interface improvements for HiAnime Downloader
"""

import sys
import time
from typing import Optional, List, Dict, Any
from colorama import Fore, Style, init
from threading import Lock
import os

# Initialize colorama
init(autoreset=True)

class ProgressTracker:
    """Enhanced progress tracking with better visual feedback"""
    
    def __init__(self):
        self.lock = Lock()
        self.current_task = ""
        self.total_episodes = 0
        self.completed_episodes = 0
        self.current_episode = 0
        self.start_time = time.time()
        
    def set_total_episodes(self, total: int):
        """Set total number of episodes to download"""
        with self.lock:
            self.total_episodes = total
            self.completed_episodes = 0
    
    def start_episode(self, episode_num: int, episode_title: str):
        """Start downloading a new episode"""
        with self.lock:
            self.current_episode = episode_num
            self.current_task = f"Episode {episode_num}: {episode_title}"
            self._update_display()
    
    def complete_episode(self):
        """Mark current episode as complete"""
        with self.lock:
            self.completed_episodes += 1
            self._update_display()
    
    def update_status(self, status: str):
        """Update current status message"""
        with self.lock:
            self.current_task = status
            self._update_display()
    
    def _update_display(self):
        """Update the progress display"""
        if self.total_episodes > 0:
            progress = (self.completed_episodes / self.total_episodes) * 100
            elapsed = time.time() - self.start_time
            
            if self.completed_episodes > 0:
                avg_time = elapsed / self.completed_episodes
                eta = avg_time * (self.total_episodes - self.completed_episodes)
                eta_str = self._format_time(eta)
            else:
                eta_str = "Calculating..."
            
            # Create progress bar
            bar_length = 30
            filled_length = int(bar_length * progress // 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            # Clear line and print progress
            sys.stdout.write('\r' + ' ' * 100)  # Clear line
            sys.stdout.write(f'\r{Fore.LIGHTGREEN_EX}[{bar}] {progress:.1f}% '
                           f'{Fore.LIGHTCYAN_EX}({self.completed_episodes}/{self.total_episodes}) '
                           f'{Fore.LIGHTYELLOW_EX}ETA: {eta_str} '
                           f'{Fore.LIGHTWHITE_EX}| {self.current_task}')
            sys.stdout.flush()
    
    def _format_time(self, seconds: float) -> str:
        """Format time in human readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def finish(self):
        """Complete the progress tracking"""
        with self.lock:
            total_time = time.time() - self.start_time
            print(f"\n{Fore.LIGHTGREEN_EX}✅ Download completed! "
                  f"{Fore.LIGHTCYAN_EX}Total time: {self._format_time(total_time)}")

class UserInterface:
    """Enhanced user interface for better interaction"""
    
    @staticmethod
    def print_banner():
        """Print application banner"""
        banner = f"""
{Fore.LIGHTCYAN_EX}╔══════════════════════════════════════════════════════════════╗
{Fore.LIGHTCYAN_EX}║                                                              ║
{Fore.LIGHTCYAN_EX}║        {Fore.LIGHTGREEN_EX}🎌 HiAnime Downloader - Enhanced Edition{Fore.LIGHTCYAN_EX}        ║
{Fore.LIGHTCYAN_EX}║                                                              ║
{Fore.LIGHTCYAN_EX}║        {Fore.LIGHTYELLOW_EX}Fast • Reliable • User-Friendly{Fore.LIGHTCYAN_EX}                ║
{Fore.LIGHTCYAN_EX}╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    @staticmethod
    def print_section_header(title: str):
        """Print a section header"""
        print(f"\n{Fore.LIGHTBLUE_EX}{'='*60}")
        print(f"{Fore.LIGHTGREEN_EX} 📺 {title}")
        print(f"{Fore.LIGHTBLUE_EX}{'='*60}")
    
    @staticmethod
    def print_anime_info(anime):
        """Print anime information in a formatted way"""
        print(f"\n{Fore.LIGHTGREEN_EX}📋 Selected Anime:")
        print(f"{Fore.LIGHTCYAN_EX}   Name: {Fore.LIGHTWHITE_EX}{anime.name}")
        print(f"{Fore.LIGHTCYAN_EX}   URL:  {Fore.LIGHTBLUE_EX}{anime.url}")
        print(f"{Fore.LIGHTCYAN_EX}   Sub Episodes: {Fore.LIGHTYELLOW_EX}{anime.sub_episodes}")
        print(f"{Fore.LIGHTCYAN_EX}   Dub Episodes: {Fore.LIGHTYELLOW_EX}{anime.dub_episodes}")
    
    @staticmethod
    def print_download_info(anime, start_ep: int, end_ep: int, download_type: str):
        """Print download information"""
        print(f"\n{Fore.LIGHTGREEN_EX}📥 Download Settings:")
        print(f"{Fore.LIGHTCYAN_EX}   Type: {Fore.LIGHTYELLOW_EX}{download_type.upper()}")
        print(f"{Fore.LIGHTCYAN_EX}   Episodes: {Fore.LIGHTYELLOW_EX}{start_ep} - {end_ep}")
        print(f"{Fore.LIGHTCYAN_EX}   Total: {Fore.LIGHTYELLOW_EX}{end_ep - start_ep + 1} episodes")
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(f"\n{Fore.LIGHTRED_EX}❌ Error: {message}")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        print(f"\n{Fore.LIGHTYELLOW_EX}⚠️  Warning: {message}")
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(f"\n{Fore.LIGHTGREEN_EX}✅ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(f"\n{Fore.LIGHTCYAN_EX}ℹ️  {message}")
    
    @staticmethod
    def get_user_choice(prompt: str, options: List[str]) -> str:
        """Get user choice with validation"""
        while True:
            print(f"\n{Fore.LIGHTCYAN_EX}{prompt}")
            for i, option in enumerate(options, 1):
                print(f"{Fore.LIGHTYELLOW_EX}  {i}. {option}")
            
            try:
                choice = input(f"\n{Fore.LIGHTGREEN_EX}Enter your choice (1-{len(options)}): {Fore.LIGHTYELLOW_EX}")
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(options):
                    return options[choice_idx]
                else:
                    UserInterface.print_error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                UserInterface.print_error("Please enter a valid number")
            except KeyboardInterrupt:
                print(f"\n{Fore.LIGHTRED_EX}Operation cancelled by user")
                sys.exit(0)
    
    @staticmethod
    def confirm_action(message: str, default: bool = True) -> bool:
        """Get user confirmation"""
        default_text = "Y/n" if default else "y/N"
        while True:
            try:
                response = input(f"\n{Fore.LIGHTCYAN_EX}{message} ({default_text}): {Fore.LIGHTYELLOW_EX}").strip().lower()
                if not response:
                    return default
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                else:
                    UserInterface.print_error("Please enter 'y' for yes or 'n' for no")
            except KeyboardInterrupt:
                print(f"\n{Fore.LIGHTRED_EX}Operation cancelled by user")
                sys.exit(0)

class NetworkStatusIndicator:
    """Show network status and connection health"""
    
    def __init__(self):
        self.connection_healthy = True
        self.retry_count = 0
    
    def show_connecting(self, url: str):
        """Show connecting status"""
        print(f"{Fore.LIGHTYELLOW_EX}🔄 Connecting to {url[:50]}{'...' if len(url) > 50 else ''}")
    
    def show_retry(self, attempt: int, max_attempts: int, error: str):
        """Show retry attempt"""
        print(f"{Fore.LIGHTYELLOW_EX}🔄 Retry {attempt}/{max_attempts} - {error}")
    
    def show_success(self):
        """Show successful connection"""
        print(f"{Fore.LIGHTGREEN_EX}✅ Connected successfully")
    
    def show_failure(self, error: str):
        """Show connection failure"""
        print(f"{Fore.LIGHTRED_EX}❌ Connection failed: {error}")
    
    def show_network_tips(self):
        """Show network troubleshooting tips"""
        tips = [
            "Check your internet connection",
            "Try using a VPN if the site is blocked",
            "Disable antivirus/firewall temporarily",
            "Check if the website is accessible in browser"
        ]
        
        print(f"\n{Fore.LIGHTYELLOW_EX}💡 Network Troubleshooting Tips:")
        for i, tip in enumerate(tips, 1):
            print(f"{Fore.LIGHTCYAN_EX}   {i}. {tip}")