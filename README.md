# 🤖 Bing Search Automation - Visible Browser Edition

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Selenium-4.0+-green.svg" alt="Selenium Version">
  <img src="https://img.shields.io/badge/Flask-2.0+-red.svg" alt="Flask Version">
  <img src="https://img.shields.io/badge/Browser-Microsoft_Edge-blue.svg" alt="Browser">
  <img src="https://img.shields.io/badge/Status-Working-brightgreen.svg" alt="Status">
</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Web Interface](#-web-interface)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

**Bing Search Automation** is a sophisticated web application that automatically performs searches on Bing.com using **Microsoft Edge WebDriver**. Unlike basic automation tools, this application simulates **realistic human typing behavior** with variable delays, natural pauses, and authentic search patterns.

### 🔑 Key Highlights

- **👀 100% Visible Browser**: Watch Edge perform searches in real-time
- **⌨️ Human-Like Typing**: Realistic character-by-character typing with natural delays
- **🎨 Modern Web Interface**: Beautiful dark-themed dashboard with live monitoring
- **📊 Real-Time Progress**: Live activity logs and progress tracking
- **⏸️ Full Control**: Start, pause, resume, and stop automation anytime
- **📅 Smart Scheduling**: Set up automated execution times
- **🔧 Highly Configurable**: Customize typing speed, delays, and search patterns

## ✨ Features

### 🤖 **Advanced Automation**
- **Visible Browser Operation**: Microsoft Edge opens in a maximized, visible window
- **Realistic Typing Simulation**: Variable character delays (50ms-400ms per character)
- **Natural Human Behavior**: Word pauses, punctuation delays, thinking pauses
- **Multiple Search Queries**: Built-in database of 25+ diverse search terms
- **Smart Cooldowns**: Configurable delays between searches (3-15 seconds)
- **Error Recovery**: Robust handling of network issues and page load failures

### 🎨 **Modern Web Interface**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Theme**: Professional blue/teal color scheme
- **Live Browser Preview**: Real-time visualization of browser activity
- **Activity Monitoring**: Detailed logs with timestamps and status indicators
- **Progress Tracking**: Visual progress bars and completion percentages
- **Status Indicators**: Color-coded system status with animations

### ⚙️ **Flexible Configuration**
- **Search Count**: 1-20 searches per session
- **Typing Speed**: Slow (human-like), Medium (balanced), Fast (demo)
- **Cooldown Time**: 3-15 seconds between searches
- **Random Delays**: Optional variation in timing
- **Realistic Typing**: Natural pauses and variations
- **Settings Persistence**: Your preferences are automatically saved

### 🔧 **Technical Features**
- **WebDriver Management**: Automatic EdgeDriver download and setup
- **Fallback Systems**: Multiple driver detection methods
- **Session Management**: Per-user automation sessions
- **API Endpoints**: RESTful API for external control
- **Background Threading**: Non-blocking automation execution
- **Resource Cleanup**: Proper browser closure and memory management

## 🎥 Demo

### What You'll See When Running:

```
🚀 Starting Automation...
👀 Edge Browser Opens (Visible Window)
🌐 Navigates to https://www.bing.com
🔍 Clicks on search box
⌨️  Types "latest technology news" (character by character)
🚀 Presses Enter
📊 Waits for results to load
⏳ 5-second cooldown
🔄 Repeats for next search...
```

### Web Interface Preview:

```
┌─────────────────────────────────────────────────────────┐
│  🤖 Bing Search Automation - Visible Browser Edition   │
├──────────────────┬──────────────────────────────────────┤
│ ⚙️ Settings       │  📊 Live Browser Preview             │
│ • Searches: 5    │  ┌─────────────────────────────────┐  │
│ • Speed: Medium  │  │ ●●● Microsoft Edge - Bing      │  │
│ • Cooldown: 5s   │  │ https://www.bing.com           │  │
│                  │  └─────────────────────────────────┘  │
│ 🎮 Controls       │  🔍 Typing: "weather today"         │
│ [▶️ Start]        │                                      │
│ [⏸️ Pause]        │  📝 Activity Log                     │
│ [⏹️ Stop]         │  [17:34:22] 🚀 Automation started   │
│                  │  [17:34:25] 🌐 Navigating to Bing    │
│ ⏰ Scheduler      │  [17:34:26] ⌨️ Typing query...       │
│ Time: 09:00      │  [17:34:30] ✅ Search completed      │
│ [➕ Add]          │                                      │
└──────────────────┴──────────────────────────────────────┤
│ 🟢 Status: Running │ 🕒 Time: 5:34:45 PM IST            │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: One-Command Start
```bash
python visible_browser_app.py
```

### Option 2: Step-by-Step
```bash
# 1. Install dependencies
pip install flask selenium webdriver-manager

# 2. Run the application
python visible_browser_app.py

# 3. Open browser to http://localhost:5000

# 4. Configure settings and click "Start"

# 5. Watch Edge browser perform searches!
```

## 📦 Installation

### Prerequisites
- **Python 3.7+** (recommended: Python 3.9+)
- **Microsoft Edge Browser** (latest version)
- **Internet Connection** (for WebDriver downloads)

### Method 1: Automatic Installation
```bash
# Clone or download the script
# Run directly - dependencies will be suggested if missing
python visible_browser_app.py
```

### Method 2: Manual Installation
```bash
# Install required packages
pip install flask>=2.0.0
pip install selenium>=4.15.0
pip install webdriver-manager>=4.0.0

# Run the application
python visible_browser_app.py
```

### Method 3: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv bing_automation
source bing_automation/bin/activate  # Linux/Mac
# or
bing_automation\Scripts\activate  # Windows

# Install dependencies
pip install flask selenium webdriver-manager

# Run application
python visible_browser_app.py
```

## 📖 Usage Guide

### 1. Starting the Application
```bash
python visible_browser_app.py
```

Expected output:
```
🌐 Starting Bing Search Automation - VISIBLE BROWSER Edition
👀 This version will open Edge in a VISIBLE window!
📱 Open http://localhost:5000 in your browser
==============================================================
Python version: 3.9.7
WebDriver Manager available: True
⚠️  HEADLESS MODE DISABLED - Browser will be visible!
==============================================================
 * Running on http://127.0.0.1:5000
```

### 2. Accessing the Web Interface
- Open your web browser
- Navigate to: **http://localhost:5000**
- You should see the modern dark-themed interface

### 3. Basic Configuration
1. **Set Search Count**: Use slider to choose 1-20 searches
2. **Adjust Typing Speed**: Select Slow/Medium/Fast
3. **Configure Cooldown**: Set delay between searches (3-15s)
4. **Enable Options**: Toggle realistic typing and random delays

### 4. Running Automation
1. Click the **"Start"** button
2. **Microsoft Edge window opens** (maximized and visible)
3. **Watch the automation happen**:
   - Browser navigates to Bing.com
   - Search box is clicked
   - Query typed character-by-character
   - Enter pressed, results loaded
   - Process repeats for each search

### 5. Controlling Automation
- **Pause**: Temporarily halt automation (resume later)
- **Resume**: Continue paused automation
- **Stop**: End automation and close browser

## ⚙️ Configuration

### Settings Overview

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Search Count** | 1-20 | 3 | Number of searches per session |
| **Cooldown Time** | 3-15 sec | 5 sec | Delay between searches |
| **Typing Speed** | Slow/Med/Fast | Medium | Character typing speed |
| **Random Delays** | On/Off | On | Adds natural variation |
| **Realistic Typing** | On/Off | On | Human-like pauses |

### Typing Speed Details

| Speed | Delay Range | Character Rate | Best For |
|-------|-------------|----------------|----------|
| **Slow** | 200-400ms | 2.5-5 chars/sec | Maximum realism |
| **Medium** | 100-200ms | 5-10 chars/sec | Balanced demo |
| **Fast** | 50-100ms | 10-20 chars/sec | Quick testing |

### Search Query Database
The application includes 25+ built-in search queries:
- Technology: "latest technology news", "artificial intelligence"
- General: "weather today", "healthy recipes"
- Educational: "how to learn programming", "science discoveries"
- Lifestyle: "travel destinations", "fitness tips"
- Current: "environmental news", "space exploration"

## 🖥️ Web Interface

### Main Dashboard Layout

#### Header Section
- **Application Title**: Bing Search Automation
- **Status Banner**: Real-time system status with animated indicators
- **System Status**: Ready/Running/Paused with color coding

#### Live Browser Preview
- **Visual Browser Window**: Simulated Edge browser interface
- **Current Action Display**: Shows what browser is doing
- **URL Bar**: Displays current page (bing.com)
- **Status Updates**: Real-time browser activity

#### Left Panel - Controls
1. **Settings Section** (Green border)
   - Search count slider
   - Cooldown time slider
   - Typing speed dropdown
   - Feature toggles

2. **Control Panel** (Green gradient)
   - Start/Pause/Stop buttons
   - Save settings button

3. **Scheduler** (Purple gradient)
   - Time picker for automation scheduling
   - Add/Clear schedule buttons

#### Right Panel - Monitoring
1. **Activity Log**
   - Real-time timestamped logs
   - Color-coded message types (Info/Success/Warning/Error)
   - Auto-scrolling with message history

2. **Progress Section**
   - Visual progress bar
   - Percentage completion
   - Current search status

#### Status Bar
- System status indicator
- Current time display

### Color Coding System
- 🟢 **Green**: Success, Ready, Normal operation
- 🔵 **Blue**: Information, Processing
- 🟡 **Yellow**: Warning, Paused
- 🔴 **Red**: Error, Stopped

## 🔌 API Reference

### Endpoints Overview

#### Settings Management
```http
GET  /api/settings
POST /api/settings
```

**GET /api/settings**
```json
{
  "num_searches": 3,
  "cooldown": 5,
  "typing_speed": "medium",
  "random_delay": true,
  "realistic_typing": true,
  "headless": false
}
```

**POST /api/settings**
```json
{
  "num_searches": 5,
  "cooldown": 7,
  "typing_speed": "slow",
  "random_delay": true,
  "realistic_typing": true
}
```

#### Automation Control
```http
POST /api/start    # Start automation
POST /api/pause    # Pause/Resume automation  
POST /api/stop     # Stop automation
GET  /api/status   # Get current status
```

**GET /api/status Response**
```json
{
  "is_running": true,
  "is_paused": false,
  "current_search": 2,
  "total_searches": 5,
  "progress": 40.0,
  "logs": [
    "[17:34:22] 🚀 Automation started",
    "[17:34:25] ✅ Search 1 completed"
  ]
}
```

#### Scheduling
```http
POST   /api/schedule     # Add scheduled task
GET    /api/schedules    # Get all schedules
DELETE /api/schedules    # Clear all schedules
```

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Could not reach host" Error
**Problem**: WebDriver can't download EdgeDriver
```
[ERROR] Error setting up Edge WebDriver: Could not reach host. Are you offline?
```

**Solutions**:
1. **Check Internet Connection**: Ensure stable internet
2. **Update WebDriver Manager**: `pip install --upgrade webdriver-manager`
3. **Firewall/Proxy**: Check if network blocks downloads
4. **Manual Driver**: Download EdgeDriver manually

#### ❌ "No WebDriver available" Error
**Problem**: EdgeDriver not found or incompatible

**Solutions**:
1. **Update Microsoft Edge**: Go to edge://settings/help
2. **Reinstall WebDriver Manager**: `pip uninstall webdriver-manager && pip install webdriver-manager`
3. **System Path**: Add EdgeDriver to system PATH
4. **Run as Admin**: Try running with administrator privileges

#### ❌ Edge Browser Doesn't Open
**Problem**: Browser starts but window not visible

**Solutions**:
1. **Check Task Manager**: Look for Edge processes
2. **Display Settings**: Check multiple monitor setup
3. **Window Focus**: Alt+Tab to find Edge window
4. **Restart Application**: Close and restart the app

#### ❌ Search Box Not Found
**Problem**: Bing page layout changed
```
[ERROR] Could not find Bing search box
```

**Solutions**:
1. **Check Internet**: Ensure Bing.com is accessible
2. **Clear Browser Data**: Reset Edge browser settings
3. **Update Application**: Check for newer version
4. **Manual Test**: Visit Bing.com manually in Edge

### Performance Issues

#### 🐌 Slow Performance
**Symptoms**: Long delays, slow typing
- **Solution**: Change typing speed to "Fast"
- **Solution**: Reduce cooldown time to minimum (3s)
- **Solution**: Disable "Realistic Typing"

#### 💾 High Memory Usage
**Symptoms**: Application uses lots of RAM
- **Solution**: Reduce number of searches per session
- **Solution**: Restart application periodically
- **Solution**: Close other browser windows

### Network Issues

#### 🌐 Proxy/Corporate Network
**Problem**: Corporate firewall blocks WebDriver
- **Solution**: Configure proxy settings
- **Solution**: Use manual EdgeDriver installation
- **Solution**: Contact IT department for permissions

#### 📶 Slow Internet
**Problem**: Timeouts during page loads
- **Solution**: Increase cooldown time
- **Solution**: Check internet speed
- **Solution**: Use wired connection instead of WiFi

### Advanced Troubleshooting

#### 🔍 Debug Mode
Enable detailed logging by modifying the script:
```python
# Add this at the start of visible_browser_app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 🧪 Test WebDriver Separately
```python
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Test EdgeDriver setup
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)
driver.get("https://www.google.com")
print("WebDriver test successful!")
driver.quit()
```

## ❓ FAQ

### General Questions

**Q: Is this safe to use?**
A: Yes! The application only performs searches on Bing.com and doesn't access personal data or modify system settings.

**Q: Will this work on Mac/Linux?**
A: The application works on Windows, Mac, and Linux. Microsoft Edge and EdgeDriver are available for all platforms.

**Q: Can I use this with other browsers?**
A: Currently designed for Microsoft Edge only. Chrome/Firefox versions would require code modifications.

**Q: How many searches can I do per day?**
A: No hard limit, but recommend reasonable usage (20-50 searches per session) to avoid potential rate limiting.

### Technical Questions

**Q: Why Microsoft Edge specifically?**
A: Edge provides excellent WebDriver support, is pre-installed on Windows, and has robust automation capabilities.

**Q: Can I run multiple instances?**
A: Yes, but each instance needs a different port. Modify the `app.run()` line to use different ports.

**Q: Does this require admin privileges?**
A: No admin privileges required for normal operation. Only needed if WebDriver installation fails.

**Q: Can I customize the search queries?**
A: Yes! Modify the `search_queries` list in the `AutomationSession` class to add your own queries.

### Usage Questions

**Q: What's the difference between typing speeds?**
- **Slow**: 200-400ms per character (very human-like)
- **Medium**: 100-200ms per character (balanced)
- **Fast**: 50-100ms per character (quick demo)

**Q: What does "Realistic Typing" do?**
A: Adds natural pauses after words (200-500ms) and punctuation (300-600ms), plus occasional thinking pauses.

**Q: Can I schedule automation for specific times?**
A: Yes! Use the Scheduler section to set specific times. The application checks every minute for scheduled tasks.

**Q: What happens if I close the web interface?**
A: The automation continues running in the background. Reopen http://localhost:5000 to regain control.

## 🤝 Contributing

We welcome contributions to improve the Bing Search Automation tool!

### Ways to Contribute

1. **Bug Reports**: Report issues via GitHub Issues
2. **Feature Requests**: Suggest new functionality
3. **Code Contributions**: Submit pull requests
4. **Documentation**: Improve README or add guides
5. **Testing**: Test on different platforms

### Development Setup

```bash
# Fork the repository
git clone https://github.com/yourusername/bing-search-automation.git
cd bing-search-automation

# Create development environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python visible_browser_app.py
```

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add comments for complex logic
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed  
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability accepted

## 🙏 Acknowledgments

- **Selenium Project**: For providing excellent WebDriver automation
- **Microsoft Edge Team**: For robust WebDriver implementation
- **Flask Community**: For the lightweight web framework
- **WebDriver Manager**: For automatic driver management
- **Font Awesome**: For beautiful icons in the web interface

## 📞 Support

If you encounter issues or need help:

1. **Check Troubleshooting Section**: Most common issues are covered above
2. **GitHub Issues**: Report bugs or request features
3. **Discussions**: Ask questions in GitHub Discussions
4. **Documentation**: Review this README thoroughly

## 🚀 Roadmap

### Upcoming Features
- [ ] Chrome browser support
- [ ] Custom search query lists
- [ ] Export automation reports
- [ ] Advanced scheduling options
- [ ] Multi-language support
- [ ] Performance analytics
- [ ] Browser extension version

### Planned Improvements
- [ ] Enhanced error recovery
- [ ] Mobile-responsive design improvements
- [ ] Docker containerization
- [ ] Configuration file support
- [ ] Automated testing suite

---

<div align="center">
  <strong>⭐ If you found this helpful, please star the repository! ⭐</strong>
  <br><br>
  Made with ❤️ for automation enthusiasts
  <br>
  Last updated: October 15, 2025
</div>
