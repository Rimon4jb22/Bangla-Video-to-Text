# Bangla-Video-to-Text


This Python project extracts audio from a video file, splits it into manageable chunks, converts each chunk to text in Bengali, and combines the results into a final transcript. The script uses `moviepy` for video processing, `pydub` for audio splitting, and Google's Speech Recognition API for transcription.

## Features

- Extracts audio from a video file
- Splits audio into 60-second chunks to handle long files
- Converts audio to Bengali text using Google Speech Recognition
- Cleans up temporary files after processing

## Requirements

To install the required dependencies, use:

```bash
pip install -r requirements.txt
