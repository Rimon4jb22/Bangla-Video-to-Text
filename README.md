# Bangla-Video-to-Text


This Python project extracts audio from a video file, splits it into manageable chunks, converts each chunk to text in Bengali, and combines the results into a final transcript. The script uses `moviepy` for video processing, `pydub` for audio splitting, and Google's Speech Recognition API for transcription.

## Provide Inputs
After running the script, it'll want the following inputs:

1. Path to the Video File: Enter the path or filename (e.g., input_video.mp4).
2. Name for the Output Text File: Specify the name for the final transcript (e.g., output.txt).

## Features

- Extracts audio from a video file
- Splits audio into 60-second chunks to handle long files
- Converts audio to Bengali text using Google Speech Recognition
- Cleans up temporary files after processing

## Requirements

To install the required dependencies, use:

```bash
pip install -r requirements.txt
