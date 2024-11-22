# NeoPod
ReadME
NeoPod/
├── main.py
├── ui_manager.py       # Placeholder for future GUI implementation
├── feed_parser.py
├── audio_manager.py
├── database_manager.py
├── config.py
├── requirements.txt
└── assets/             # For future GUI assets (CSS, icons, fonts)

NeoPod
NeoPod is a command-line podcast manager and player written in Python. It allows you to subscribe to podcasts via RSS feeds or website URLs, manage your subscriptions, and play podcast episodes directly from the terminal. Additionally, NeoPod supports playing individual MP3 files from URLs.

## Table of Contents
- Features
- Installation
    - Prerequisites
    - Setup
- Usage
    - Main Menu Options
    - Subscribing to Podcasts
    - Viewing Subscriptions
    - Playing Episodes
    - Unsubscribing from Podcasts
    - Playing MP3 from URL
- Controls During Playback
- Dependencies
- Contributing
- License
## Features
- Subscribe to Podcasts: Add podcasts using RSS feed URLs or website URLs.
- Automatic Feed Discovery: Use Feedfinder to locate RSS feeds from website URLs.
- View Subscriptions: List all subscribed podcasts.
- Play Episodes: Stream podcast episodes directly from the terminal.
- Playback Controls: Pause, resume, and stop playback using keyboard inputs.
- Unsubscribe: Remove podcasts from your subscriptions.
- Play MP3 from URL: Stream individual MP3 files by providing their URLs.
## Installation
- Prerequisites
- Python 3.6 or higher
- pip (Python package manager)
- VLC Media Player (with libvlc bindings)

## Setup
1. Clone the Repository
- git clone https://github.com/yourusername/NeoPod.git
- cd NeoPod

2. Create a Virtual Environment
- python3 -m venv venv
- source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

3. Install Dependencies
- pip install -r requirements.txt

4. Install VLC and Development Libraries
- On Ubuntu/Debian:
    - sudo apt-get update
    - sudo apt-get install vlc libvlc-dev
- On macOS:
    - brew update
    - brew cask install vlc
- On Windows:
    - Download and install VLC from the official website.
    - Ensure VLC is added to your system's PATH

## Usage
- Run the application from the terminal:
    - python main.py
