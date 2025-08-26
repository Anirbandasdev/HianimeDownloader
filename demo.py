#!/usr/bin/env python3
"""
Demo script to showcase the enhanced features
"""

import sys
import time
import os
from tools.user_interface import UserInterface, ProgressTracker, NetworkStatusIndicator
from tools.config_manager import ConfigManager
from colorama import Fore

def demo_user_interface():
    """Demonstrate the enhanced user interface"""
    ui = UserInterface()
    
    # Banner
    ui.print_banner()
    
    # Section headers
    ui.print_section_header("User Interface Demo")
    
    # Different message types
    ui.print_info("This is an informational message")
    time.sleep(1)
    
    ui.print_success("This is a success message!")
    time.sleep(1)
    
    ui.print_warning("This is a warning message")
    time.sleep(1)
    
    ui.print_error("This is an error message")
    time.sleep(1)

def demo_progress_tracking():
    """Demonstrate progress tracking"""
    ui = UserInterface()
    ui.print_section_header("Progress Tracking Demo")
    
    progress = ProgressTracker()
    progress.set_total_episodes(5)
    
    episodes = [
        "The Beginning",
        "First Challenge", 
        "Turning Point",
        "The Battle",
        "Victory"
    ]
    
    for i, episode_title in enumerate(episodes, 1):
        progress.start_episode(i, episode_title)
        
        # Simulate download time
        for _ in range(20):
            time.sleep(0.1)
            # progress.update_status(f"Downloading... {_*5}%")
        
        progress.complete_episode()
        time.sleep(0.5)
    
    progress.finish()

def demo_configuration():
    """Demonstrate configuration management"""
    ui = UserInterface()
    ui.print_section_header("Configuration Demo")
    
    print(f"{Fore.LIGHTCYAN_EX}Creating and loading configuration...")
    
    config_manager = ConfigManager("demo_config.json")
    config = config_manager.get_config()
    
    print(f"{Fore.LIGHTGREEN_EX}✅ Configuration loaded:")
    print(f"{Fore.LIGHTCYAN_EX}  - Max Retries: {config.max_retries}")
    print(f"{Fore.LIGHTCYAN_EX}  - Timeout: {config.timeout}s")
    print(f"{Fore.LIGHTCYAN_EX}  - Output Dir: {config.output_directory}")
    print(f"{Fore.LIGHTCYAN_EX}  - Quality: {config.default_quality}")
    print(f"{Fore.LIGHTCYAN_EX}  - Concurrent Downloads: {config.max_concurrent_downloads}")
    
    # Clean up demo config
    if os.path.exists("demo_config.json"):
        os.remove("demo_config.json")
    
    ui.print_success("Configuration demo completed!")

def demo_network_status():
    """Demonstrate network status indicators"""
    ui = UserInterface()
    ui.print_section_header("Network Status Demo")
    
    network = NetworkStatusIndicator()
    
    # Simulate connection attempts
    test_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200", 
        "https://httpbin.org/status/404"
    ]
    
    for url in test_urls:
        network.show_connecting(url)
        time.sleep(1)
        
        if "404" in url:
            network.show_failure("HTTP 404 Not Found")
        else:
            network.show_success()
        
        time.sleep(1)
    
    network.show_network_tips()

def main():
    """Run the demo"""
    print(f"{Fore.LIGHTGREEN_EX}🎌 Enhanced HiAnime Downloader - Feature Demo")
    print(f"{Fore.LIGHTCYAN_EX}{'='*60}")
    
    demos = [
        ("User Interface", demo_user_interface),
        ("Progress Tracking", demo_progress_tracking), 
        ("Configuration System", demo_configuration),
        ("Network Status", demo_network_status)
    ]
    
    for name, demo_func in demos:
        try:
            print(f"\n{Fore.LIGHTYELLOW_EX}🔄 Running {name} demo...")
            demo_func()
            time.sleep(2)
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTRED_EX}Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n{Fore.LIGHTRED_EX}Error in {name} demo: {e}")
    
    print(f"\n{Fore.LIGHTGREEN_EX}✨ Demo completed! Try running:")
    print(f"{Fore.LIGHTCYAN_EX}  python main_enhanced.py")
    print(f"{Fore.LIGHTCYAN_EX}  python quick_start.py")

if __name__ == "__main__":
    main()