# VideoAudio-to-Text

A lightweight Python-based transcription tool that converts local video files, local audio files, and supported online video URLs into text.

This project supports multiple languages and uses FFmpeg streaming to process audio in small chunks, helping reduce RAM usage when processing long media files.

## Features

- Convert local video files to text
- Convert local audio files to text
- Convert supported online video URLs to text
- Support for YouTube, Facebook, and other platforms supported by yt-dlp
- Multi-language speech recognition
- Built-in support for:
  - Bangla
  - English
  - Hindi
  - Urdu
  - Chinese
  - Arabic
  - Japanese
  - Korean
- Custom language code support
- FFmpeg-based streaming audio processing
- Processes audio in 30-second chunks
- Reduced RAM usage for long media files
- Automatic output file naming
- Optional deletion of downloaded videos

## How It Works

```text
Local Video ───┐
Local Audio ───┼──> FFmpeg Audio Stream ──> Speech Recognition ──> Text File
Online URL ────┘
