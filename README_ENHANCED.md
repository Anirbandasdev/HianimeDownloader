# 🎌 Enhanced HiAnime Downloader

A fast, reliable, and user-friendly anime downloader with advanced features like parallel downloads, resume capability, and smart error handling.

## ✨ Key Features

### 🚀 **Performance & Reliability**
- **Robust Error Handling** - Advanced retry logic with exponential backoff
- **Parallel Downloads** - Download multiple episodes simultaneously
- **Resume Capability** - Automatically resume interrupted downloads
- **Smart Connection Management** - Optimized for unreliable networks

### 🎯 **User Experience**
- **Interactive UI** - Beautiful command-line interface with progress bars
- **Configuration System** - Easy customization through config files
- **Batch Downloads** - Download multiple anime from a list
- **Real-time Progress** - Live download speed and ETA tracking

### 🛡️ **Advanced Features**
- **Anti-Detection** - Bypasses common blocking mechanisms
- **SSL Flexibility** - Handles certificate issues automatically
- **User Agent Rotation** - Prevents detection and blocking
- **Network Diagnostics** - Built-in troubleshooting guidance

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Chrome or Chromium browser
- ChromeDriver (automatically managed)

### Quick Install
```bash
# Clone the repository
git clone https://github.com/your-username/HianimeDownloader.git
cd HianimeDownloader

# Install dependencies
pip install -r requirements.txt

# Run the enhanced version
python main_enhanced.py
```

## 🚀 Usage

### Basic Usage

#### Interactive Mode (Recommended for beginners)
```bash
python main_enhanced.py
```

#### Quick Download
```bash
# Search and download
python main_enhanced.py -n "Demon Slayer"

# Download from direct link
python main_enhanced.py -l "https://hianime.nz/watch/demon-slayer-12343"
```

### Advanced Usage

#### Batch Downloads
```bash
# Create anime_list.txt with one anime name per line
echo "Demon Slayer" > anime_list.txt
echo "Attack on Titan" >> anime_list.txt
echo "One Piece" >> anime_list.txt

# Run batch download
python main_enhanced.py --batch anime_list.txt
```

#### Custom Configuration
```bash
# Open configuration menu
python main_enhanced.py --config

# Quick options
python main_enhanced.py -n "Naruto" --quality 1080p --no-subs --output "D:/Anime"
```

#### Advanced Options
```bash
python main_enhanced.py \\
  --name "Your Anime Name" \\
  --quality best \\
  --output "./downloads" \\
  --server "HD-1" \\
  --max-retries 5 \\
  --start-ep 1 \\
  --end-ep 24 \\
  --headless
```

## ⚙️ Configuration

### Configuration File (`config.json`)
The application creates a `config.json` file with these settings:

```json
{
  "max_retries": 5,
  "timeout": 30,
  "delay_between_retries": 2.0,
  "verify_ssl": false,
  "default_quality": "best",
  "download_subtitles": true,
  "subtitle_language": "en",
  "max_concurrent_downloads": 3,
  "headless_browser": true,
  "browser_timeout": 30,
  "page_load_wait": 5,
  "output_directory": "downloads",
  "create_season_folders": true,
  "filename_template": "{anime_name} - S{season:02d}E{episode:02d} - {episode_title}",
  "rotate_user_agents": true
}
```

### Environment Variables
```bash
# Alternative configuration through environment
export HIANIME_OUTPUT_DIR="./downloads"
export HIANIME_MAX_RETRIES="10"
export HIANIME_CONCURRENT_DOWNLOADS="5"
export HIANIME_HEADLESS="true"
```

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-n, --name` | Anime name to search | Interactive prompt |
| `-l, --link` | Direct anime page URL | None |
| `-o, --output` | Output directory | `./downloads` |
| `--quality` | Video quality (best/worst/720p/1080p) | `best` |
| `--no-subs` | Skip subtitle download | Download subs |
| `--sub-lang` | Subtitle language code | `en` |
| `--server` | Preferred server name | Auto-select |
| `--headless` | Run browser in headless mode | False |
| `--config` | Open configuration menu | False |
| `--max-retries` | Maximum retry attempts | 5 |
| `--batch` | Batch file with anime list | None |
| `--start-ep` | Starting episode number | 1 |
| `--end-ep` | Ending episode number | Last episode |

## 🛠️ Troubleshooting

### Common Issues

#### Connection Problems
```bash
# Test connectivity
python -c "import requests; print(requests.get('https://httpbin.org/ip').json())"

# Check if site is accessible
python -c "import requests; print(requests.get('https://hianime.nz', timeout=10).status_code)"
```

#### Solutions:
1. **Use VPN** if the site is geo-blocked
2. **Disable antivirus** temporarily (may block Python requests)
3. **Check firewall settings** (allow Python network access)
4. **Try different DNS** (8.8.8.8, 1.1.1.1)

#### Browser Issues
- **Chrome not found**: Install Chrome or set CHROME_PATH environment variable
- **ChromeDriver issues**: The app auto-manages ChromeDriver
- **Selenium timeouts**: Increase `browser_timeout` in config

### Network Optimization

#### For Slow Connections
```json
{
  "max_retries": 10,
  "timeout": 60,
  "delay_between_retries": 5.0,
  "max_concurrent_downloads": 1
}
```

#### For Fast Connections
```json
{
  "max_retries": 3,
  "timeout": 15,
  "delay_between_retries": 1.0,
  "max_concurrent_downloads": 5
}
```

## 📊 Performance Features

### Resume Downloads
- Automatically detects partial downloads
- Resumes from exact byte position
- Handles network interruptions gracefully

### Parallel Processing
- Downloads multiple episodes simultaneously
- Smart bandwidth management
- Automatic retry for failed segments

### Progress Tracking
- Real-time download speed
- Accurate ETA calculations
- Visual progress bars
- Episode completion status

## 🔒 Privacy & Security

- **No data collection** - Everything runs locally
- **Secure connections** - HTTPS with certificate validation options
- **User agent rotation** - Prevents tracking
- **Local storage only** - No cloud dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit: `git commit -m "Add amazing feature"`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect copyright laws and the terms of service of the websites you interact with. The developers are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video download capabilities
- [Selenium](https://selenium-python.readthedocs.io/) for web automation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Colorama](https://github.com/tartley/colorama) for colored terminal output

---

**Made with ❤️ by the HiAnime Downloader Team**

For support, create an issue on GitHub or join our community discussions!