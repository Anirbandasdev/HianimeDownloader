#!/usr/bin/env python3
"""
Smart Download Manager with parallel processing and resume capabilities
"""

import os
import json
import time
import asyncio
import aiohttp
import aiofiles
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
from colorama import Fore

@dataclass
class DownloadTask:
    """Represents a download task"""
    url: str
    filename: str
    headers: Dict[str, str]
    episode_number: int
    episode_title: str
    file_size: int = 0
    downloaded: int = 0
    status: str = "pending"  # pending, downloading, completed, failed, paused
    retry_count: int = 0
    max_retries: int = 3

class SmartDownloadManager:
    """Enhanced download manager with smart features"""
    
    def __init__(self, max_concurrent: int = 3, chunk_size: int = 1024*1024):
        self.max_concurrent = max_concurrent
        self.chunk_size = chunk_size
        self.download_tasks: List[DownloadTask] = []
        self.progress_callbacks: List[Callable] = []
        self.resume_data_file = "download_resume.json"
        
    def add_progress_callback(self, callback: Callable):
        """Add a progress callback function"""
        self.progress_callbacks.append(callback)
    
    def add_download(self, url: str, filename: str, headers: Dict[str, str], 
                    episode_number: int, episode_title: str) -> DownloadTask:
        """Add a download task"""
        task = DownloadTask(
            url=url,
            filename=filename,
            headers=headers,
            episode_number=episode_number,
            episode_title=episode_title
        )
        self.download_tasks.append(task)
        return task
    
    def save_resume_data(self):
        """Save download progress for resume capability"""
        resume_data = {
            "tasks": [asdict(task) for task in self.download_tasks if task.status in ["downloading", "paused"]]
        }
        
        try:
            with open(self.resume_data_file, 'w') as f:
                json.dump(resume_data, f, indent=2)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Failed to save resume data: {e}")
    
    def load_resume_data(self) -> bool:
        """Load previous download progress"""
        if not os.path.exists(self.resume_data_file):
            return False
        
        try:
            with open(self.resume_data_file, 'r') as f:
                resume_data = json.load(f)
            
            resumed_count = 0
            for task_data in resume_data.get("tasks", []):
                # Check if file exists and has partial content
                filename = task_data["filename"]
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    if file_size > 0:
                        task = DownloadTask(**task_data)
                        task.downloaded = file_size
                        task.status = "paused"
                        self.download_tasks.append(task)
                        resumed_count += 1
            
            if resumed_count > 0:
                print(f"{Fore.LIGHTGREEN_EX}📂 Resumed {resumed_count} partial downloads")
                return True
            
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Failed to load resume data: {e}")
        
        return False
    
    async def download_with_progress(self, task: DownloadTask, session: aiohttp.ClientSession):
        """Download a file with progress tracking and resume support"""
        try:
            headers = task.headers.copy()
            
            # Check if we can resume
            if task.downloaded > 0 and os.path.exists(task.filename):
                headers['Range'] = f'bytes={task.downloaded}-'
                mode = 'ab'  # Append binary
            else:
                task.downloaded = 0
                mode = 'wb'  # Write binary
            
            task.status = "downloading"
            
            async with session.get(task.url, headers=headers) as response:
                if response.status not in [200, 206]:  # 206 = Partial Content
                    raise Exception(f"HTTP {response.status}")
                
                # Get total file size
                if task.file_size == 0:
                    content_length = response.headers.get('Content-Length')
                    if content_length:
                        if response.status == 206:
                            # For resume, add current downloaded size
                            task.file_size = int(content_length) + task.downloaded
                        else:
                            task.file_size = int(content_length)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(task.filename), exist_ok=True)
                
                # Download with progress
                async with aiofiles.open(task.filename, mode) as f:
                    async for chunk in response.content.iter_chunked(self.chunk_size):
                        await f.write(chunk)
                        task.downloaded += len(chunk)
                        
                        # Call progress callbacks
                        for callback in self.progress_callbacks:
                            callback(task)
            
            task.status = "completed"
            print(f"{Fore.LIGHTGREEN_EX}✅ Completed: Episode {task.episode_number}")
            
        except asyncio.CancelledError:
            task.status = "paused"
            self.save_resume_data()
            raise
        except Exception as e:
            task.status = "failed"
            task.retry_count += 1
            print(f"{Fore.LIGHTRED_EX}❌ Failed: Episode {task.episode_number} - {e}")
            
            if task.retry_count < task.max_retries:
                print(f"{Fore.LIGHTYELLOW_EX}🔄 Will retry ({task.retry_count}/{task.max_retries})")
                task.status = "pending"
    
    async def download_all(self):
        """Download all tasks with concurrency control"""
        if not self.download_tasks:
            print(f"{Fore.LIGHTYELLOW_EX}No downloads to process")
            return
        
        print(f"{Fore.LIGHTCYAN_EX}🚀 Starting downloads ({self.max_concurrent} concurrent)")
        
        # Create aiohttp session with custom settings
        timeout = aiohttp.ClientTimeout(total=None, connect=30)
        connector = aiohttp.TCPConnector(limit=self.max_concurrent, limit_per_host=self.max_concurrent)
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            # Create semaphore to limit concurrent downloads
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def download_with_semaphore(task):
                async with semaphore:
                    return await self.download_with_progress(task, session)
            
            # Start all downloads
            pending_tasks = [task for task in self.download_tasks if task.status in ["pending", "paused"]]
            
            while pending_tasks:
                # Create async tasks for pending downloads
                async_tasks = [download_with_semaphore(task) for task in pending_tasks]
                
                try:
                    # Wait for all downloads to complete
                    await asyncio.gather(*async_tasks, return_exceptions=True)
                except KeyboardInterrupt:
                    print(f"\n{Fore.LIGHTYELLOW_EX}⏸️ Pausing downloads...")
                    for async_task in async_tasks:
                        async_task.cancel()
                    
                    # Wait for cancellation to complete
                    await asyncio.gather(*async_tasks, return_exceptions=True)
                    self.save_resume_data()
                    raise
                
                # Check for failed tasks that can be retried
                pending_tasks = [task for task in self.download_tasks 
                               if task.status == "pending" and task.retry_count < task.max_retries]
                
                if pending_tasks:
                    print(f"{Fore.LIGHTYELLOW_EX}🔄 Retrying {len(pending_tasks)} failed downloads...")
                    await asyncio.sleep(2)  # Brief pause before retry
    
    def get_download_summary(self) -> Dict[str, int]:
        """Get download statistics"""
        summary = {
            "total": len(self.download_tasks),
            "completed": 0,
            "failed": 0,
            "pending": 0,
            "downloading": 0
        }
        
        for task in self.download_tasks:
            if task.status in summary:
                summary[task.status] += 1
        
        return summary
    
    def cleanup_resume_data(self):
        """Clean up resume data after successful completion"""
        try:
            if os.path.exists(self.resume_data_file):
                os.remove(self.resume_data_file)
        except Exception:
            pass  # Ignore cleanup errors

class AdvancedProgressTracker:
    """Advanced progress tracker for multiple downloads"""
    
    def __init__(self):
        self.tasks: Dict[str, DownloadTask] = {}
        self.start_time = time.time()
        self.last_update = 0
        
    def update_task_progress(self, task: DownloadTask):
        """Update progress for a specific task"""
        self.tasks[task.filename] = task
        
        # Throttle updates to avoid spam
        current_time = time.time()
        if current_time - self.last_update < 0.5:  # Update max every 0.5 seconds
            return
        
        self.last_update = current_time
        self._display_progress()
    
    def _display_progress(self):
        """Display current progress"""
        if not self.tasks:
            return
        
        # Calculate overall progress
        total_size = sum(task.file_size for task in self.tasks.values())
        total_downloaded = sum(task.downloaded for task in self.tasks.values())
        
        if total_size > 0:
            overall_progress = (total_downloaded / total_size) * 100
        else:
            overall_progress = 0
        
        # Calculate speed
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            speed = total_downloaded / elapsed_time  # bytes per second
            speed_str = self._format_speed(speed)
        else:
            speed_str = "Calculating..."
        
        # Count statuses
        completed = sum(1 for task in self.tasks.values() if task.status == "completed")
        total = len(self.tasks)
        
        # Clear line and display progress
        print(f"\r{Fore.LIGHTGREEN_EX}📊 Progress: {overall_progress:.1f}% "
              f"{Fore.LIGHTCYAN_EX}({completed}/{total}) "
              f"{Fore.LIGHTYELLOW_EX}{speed_str} "
              f"{Fore.LIGHTWHITE_EX}| {self._format_size(total_downloaded)}/{self._format_size(total_size)}", 
              end="", flush=True)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024*1024:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024*1024*1024:
            return f"{size_bytes/(1024*1024):.1f} MB"
        else:
            return f"{size_bytes/(1024*1024*1024):.1f} GB"
    
    def _format_speed(self, speed: float) -> str:
        """Format download speed"""
        if speed < 1024:
            return f"{speed:.1f} B/s"
        elif speed < 1024*1024:
            return f"{speed/1024:.1f} KB/s"
        else:
            return f"{speed/(1024*1024):.1f} MB/s"
    
    def finish(self):
        """Finish progress tracking"""
        print(f"\n{Fore.LIGHTGREEN_EX}✅ All downloads completed!")

# Example usage function for integration
def create_smart_downloader(config) -> SmartDownloadManager:
    """Create a configured smart download manager"""
    manager = SmartDownloadManager(
        max_concurrent=config.max_concurrent_downloads,
        chunk_size=1024*1024  # 1MB chunks
    )
    
    # Set up progress tracking
    progress_tracker = AdvancedProgressTracker()
    manager.add_progress_callback(progress_tracker.update_task_progress)
    
    return manager